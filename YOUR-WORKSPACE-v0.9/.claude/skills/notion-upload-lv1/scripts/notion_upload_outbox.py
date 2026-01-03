from __future__ import annotations

import argparse
import hashlib
import os
import re
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


# ------------------------------------------------------------------------------
# 1. 환경 설정 및 상수
# ------------------------------------------------------------------------------

# 환경 설정 파일 로드 (.env)
def _load_config(repo_root: Path) -> None:
    env_path = repo_root / ".env"
    try:
        from dotenv import load_dotenv  # type: ignore
        # override=False: 이미 로드된 환경변수보존 (시스템 환경변수 우선)
        # 덮어쓰기 여부는 상황에 따라 다르지만 보통 .env가 우선 적용되길 원하면 load_dotenv(override=True)
        # 여기서는 기본 동작(기존 env 유지) 따름
        load_dotenv(env_path) 
        if env_path.exists():
            print(f"[INFO] Loaded configuration from .env")
    except ImportError:
        print("[WARN] python-dotenv is not installed. Environment variables might not be loaded.")

def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "AGENTS.md").exists() or (candidate / ".python-version").exists():
            return candidate
    return start

# ------------------------------------------------------------------------------
# 2. Notion 변환 유틸리티 (마크다운 -> 블록)
# ------------------------------------------------------------------------------

def _read_text_file(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")

def _rich_text_plain(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    # Notion API 제한: 텍스트 청크당 2000자
    return [{"type": "text", "text": {"content": chunk}} for chunk in [text[i:i+2000] for i in range(0, len(text), 2000)]]

def _make_paragraph(text: str) -> dict[str, Any]:
    return {"type": "paragraph", "paragraph": {"rich_text": _rich_text_plain(text)}}

def _make_heading(level: int, text: str) -> dict[str, Any]:
    block_type = f"heading_{min(level, 3)}" # 1, 2, 3 지원
    return {"type": block_type, block_type: {"rich_text": _rich_text_plain(text)}}

def _make_code(code: str, language: str | None) -> dict[str, Any]:
    return {"type": "code", "code": {"rich_text": _rich_text_plain(code), "language": language or "plain text"}}

def _make_list_item(text: str, numbered: bool) -> dict[str, Any]:
    t = "numbered_list_item" if numbered else "bulleted_list_item"
    return {"type": t, t: {"rich_text": _rich_text_plain(text)}}

def markdown_to_notion_blocks(markdown: str) -> list[dict[str, Any]]:
    # Markdown to Notion 블록 변환기 (Core): 줄 단위 처리
    lines = markdown.splitlines()
    blocks = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:
            i += 1
            continue
            
        # Code Block (```)
        if stripped.startswith("```"):
            lang = stripped.lstrip("`").strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines): i += 1 # skip closing ```
            blocks.append(_make_code("\n".join(code_lines), lang))
            continue
            
        # Heading (#, ##, ###)
        if stripped.startswith("#"):
            level = len(stripped.split()[0])
            text = stripped.lstrip("#").strip()
            blocks.append(_make_heading(level, text))
            i += 1
            continue
            
        # List Item (-, *, 1.)
        if stripped.startswith("- ") or stripped.startswith("* "):
            blocks.append(_make_list_item(stripped[2:], numbered=False))
            i += 1
            continue
        if re.match(r"^\d+\. ", stripped):
            text = re.sub(r"^\d+\.\s+", "", stripped)
            blocks.append(_make_list_item(text, numbered=True))
            i += 1
            continue
            
        # Paragraph (기본)
        blocks.append(_make_paragraph(stripped))
        i += 1
        
    return blocks

# ------------------------------------------------------------------------------
# 3. 메인 로직
# ------------------------------------------------------------------------------

@dataclass
class UploadItem:
    path: Path
    title: str
    content: str
    blocks: list[dict[str, Any]]

def main() -> int:
    parser = argparse.ArgumentParser(description="Notion 단방향 업로드 (파일명 기반 상태 관리)")
    parser.add_argument("--dry-run", action="store_true", help="실제 업로드를 수행하지 않고 로그만 출력")
    parser.add_argument("--files", nargs="+", default=None, help="특정 파일만 업로드 (파일명, 확장자 포함)")
    args = parser.parse_args()

    # 1. 환경 설정 로드
    repo_root = _find_repo_root(Path.cwd())
    _load_config(repo_root)

    notion_token = os.getenv("NOTION_TOKEN")
    parent_page_id = os.getenv("NOTION_UPLOAD_DEFAULT_PAGE_ID")
    target_dir_name = os.getenv("NOTION_UPLOAD_DIR", "02_outbox") # 기본값 02_outbox
    
    target_dir = repo_root / target_dir_name

    # 2. 필수 설정 확인
    if not notion_token:
        print("[ERROR] .env에 NOTION_TOKEN이 없습니다.")
        return 1
    if not parent_page_id:
        print("[ERROR] .env에 NOTION_UPLOAD_DEFAULT_PAGE_ID가 없습니다.")
        return 1
    if not target_dir.exists():
        print(f"[ERROR] 업로드 대상 폴더를 찾을 수 없습니다: {target_dir}")
        return 1

    # 3. Notion 클라이언트 준비
    try:
        from notion_client import Client
        client = Client(auth=notion_token)
    except ImportError:
        print("[ERROR] notion-client 패키지가 설치되지 않았습니다. python -m pip install -r .claude/skills/notion-upload-lv1/requirements.txt")
        return 1

    print(f"Target Directory: {target_dir}")
    
    # 4. 파일 처리 (파일명에 (done)_, (fail)_ 이 없는 파일 대상)
    files_to_process = list(target_dir.glob("*.md"))
    
    if args.files:
        target_names = set(args.files)
        files_to_process = [f for f in files_to_process if f.name in target_names]
        if len(files_to_process) < len(target_names):
            print(f"[INFO] 요청한 파일 중 일부만 찾았습니다 ({len(files_to_process)}/{len(target_names)}).")

    count = 0
    for file_path in files_to_process:
        filename = file_path.name
        
        # 이미 처리된 파일 건너뛰기 ({done}, {fail} 포함)
        if (filename.startswith("(done)_") or filename.startswith("(fail)_") or 
            filename.startswith("{done}_") or filename.startswith("{fail}_")):
            continue
            
        print(f"\n[Processing] {filename}...")
        count += 1
        
        try:
            content = _read_text_file(file_path)
            # Markdown 제목(# )이 있다면, 본문에서 제목 제거 로직은 여기서는 생략 (Core Logic: 파일명 우선)
            # 파일명을 제목으로 사용
            title = file_path.stem
            
            blocks = markdown_to_notion_blocks(content)
            
            # Dry Run
            if args.dry_run:
                print(f"  -> [Dry-Run] Would upload '{title}' ({len(blocks)} blocks)")
                continue

            # API Call
            new_page = client.pages.create(
                parent={"page_id": parent_page_id},
                properties={
                    "title": {"title": [{"text": {"content": title}}]}
                },
                children=blocks[:100] # 안정성: 처리 블록 수 제한 (Safety Config)
            )
            
            page_id = new_page["id"]
            page_url = new_page["url"]
            print(f"  -> Upload Success! Page ID: {page_id}")
            
            # 5. 메타데이터(Frontmatter) 주입
            upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            frontmatter = f"""---
title: "{title}"
notion_url: "{page_url}"
uploaded_at: "{upload_time}"
notion_page_id: "{page_id}"
---

"""
            # 원본 내용 앞에 삽입
            new_content = frontmatter + content
            file_path.write_text(new_content, encoding="utf-8")
            
            # 6. 상태 변경 (파일명 변경: (done)_파일명.md)
            new_name = f"(done)_{filename}"
            new_path = file_path.with_name(new_name)
            file_path.rename(new_path)
            print(f"  -> Renamed to: {new_name}")
            
        except Exception as e:
            print(f"  -> [ERROR] Upload Failed: {e}")
            traceback.print_exc()
            
            # 실패 시 파일명 변경: (fail)_파일명.md
            if not args.dry_run:
                new_name = f"(fail)_{filename}"
                new_path = file_path.with_name(new_name)
                try:
                    file_path.rename(new_path)
                    print(f"  -> Renamed to: {new_name}")
                except OSError:
                    pass

    if count == 0:
        print("\n[INFO] 처리할 새로운 파일(.md)이 없습니다.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
