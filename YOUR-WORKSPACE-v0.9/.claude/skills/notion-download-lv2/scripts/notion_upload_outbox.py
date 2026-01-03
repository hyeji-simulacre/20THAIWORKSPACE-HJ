from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


DEFAULT_UPLOAD_READY_REL = Path("02_outbox") / "01_ready"
DEFAULT_UPLOAD_INPROGRESS_REL = Path("02_outbox") / "02_inprogress"
DEFAULT_UPLOAD_COMPLETE_REL = Path("02_outbox") / "03_complete"
DEFAULT_UPLOAD_FAILED_REL = Path("02_outbox") / "04_failed"


def _now_ms_compact() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]


def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "AGENTS.md").exists() or (candidate / ".python-version").exists():
            return candidate
    return start


def _load_dotenv(repo_root: Path) -> None:
    dotenv_path = repo_root / ".env"
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv(dotenv_path)
    except ImportError:
        if dotenv_path.exists():
            print("NOTE: python-dotenv is not installed; skipping .env auto-load.")


def _resolve_dir(repo_root: Path, value: str | None, default_rel: Path) -> Path:
    raw = (value or "").strip() or str(default_rel)
    p = Path(raw)
    if not p.is_absolute():
        p = repo_root / p
    return p.resolve()


def _read_text_file(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rich_text_plain(text: str) -> list[dict[str, Any]]:
    if not text:
        return []
    return [{"type": "text", "text": {"content": chunk}} for chunk in _split_2000(text)]


def _split_2000(text: str) -> list[str]:
    chunks: list[str] = []
    remaining = text
    while remaining:
        chunks.append(remaining[:2000])
        remaining = remaining[2000:]
    return chunks


def _make_paragraph(text: str) -> dict[str, Any]:
    return {"type": "paragraph", "paragraph": {"rich_text": _rich_text_plain(text)}}


def _make_heading(level: int, text: str) -> dict[str, Any]:
    if level <= 1:
        block_type = "heading_1"
    elif level == 2:
        block_type = "heading_2"
    else:
        block_type = "heading_3"
    return {  # type: ignore[return-value]
        "type": block_type,
        block_type: {"rich_text": _rich_text_plain(text)},
    }


def _make_divider() -> dict[str, Any]:
    return {"type": "divider", "divider": {}}


def _make_quote(text: str) -> dict[str, Any]:
    return {"type": "quote", "quote": {"rich_text": _rich_text_plain(text)}}


def _make_code(code: str, language: str | None) -> dict[str, Any]:
    normalized_language = (language or "").strip().lower() or "plain text"
    language_map = {
        "ps": "powershell",
        "pwsh": "powershell",
        "powershell": "powershell",
        "bash": "bash",
        "sh": "bash",
        "python": "python",
        "py": "python",
        "json": "json",
        "yaml": "yaml",
        "yml": "yaml",
        "md": "markdown",
        "markdown": "markdown",
        "text": "plain text",
        "plain": "plain text",
        "plain text": "plain text",
    }
    notion_language = language_map.get(normalized_language, "plain text")
    return {"type": "code", "code": {"rich_text": _rich_text_plain(code), "language": notion_language}}


def _make_list_item(text: str, numbered: bool) -> dict[str, Any]:
    if numbered:
        return {"type": "numbered_list_item", "numbered_list_item": {"rich_text": _rich_text_plain(text)}}
    return {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": _rich_text_plain(text)}}


def _make_todo(text: str, checked: bool) -> dict[str, Any]:
    return {"type": "to_do", "to_do": {"rich_text": _rich_text_plain(text), "checked": checked}}


def _drop_first_h1(markdown: str) -> str:
    lines = markdown.splitlines()
    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        if re.match(r"^#\s+.+$", line.strip()):
            return "\n".join([*lines[:idx], *lines[idx + 1 :]]).lstrip("\n")
        break
    return markdown


def markdown_to_notion_blocks(markdown: str) -> list[dict[str, Any]]:
    lines = markdown.splitlines()
    blocks: list[dict[str, Any]] = []
    i = 0

    def is_divider(line: str) -> bool:
        return line.strip() in {"---", "***", "___"}

    def is_code_fence(line: str) -> bool:
        return bool(re.match(r"^```\s*(\S+)?\s*$", line.strip()))

    def is_heading(line: str) -> bool:
        return bool(re.match(r"^#{1,6}\s+.+$", line.strip()))

    def is_quote(line: str) -> bool:
        return line.strip().startswith(">")

    def is_todo(line: str) -> bool:
        return bool(re.match(r"^[-*]\s+\[[ xX]\]\s+.+$", line.strip()))

    def is_bullet(line: str) -> bool:
        return bool(re.match(r"^[-*]\s+.+$", line.strip()))

    def is_numbered(line: str) -> bool:
        return bool(re.match(r"^\d+\.\s+.+$", line.strip()))

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if is_divider(line):
            blocks.append(_make_divider())
            i += 1
            continue

        fence = re.match(r"^```\s*(\S+)?\s*$", line.strip())
        if fence:
            language = fence.group(1) if fence.group(1) else None
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines) and lines[i].strip().startswith("```"):
                i += 1
            blocks.append(_make_code("\n".join(code_lines).rstrip("\n"), language))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if heading:
            level = len(heading.group(1))
            text = heading.group(2).strip()
            blocks.append(_make_heading(level, text))
            i += 1
            continue

        if is_quote(line):
            quote_lines: list[str] = []
            while i < len(lines) and is_quote(lines[i]):
                quote_lines.append(lines[i].strip()[1:].lstrip())
                i += 1
            blocks.append(_make_quote("\n".join(quote_lines).strip()))
            continue

        todo = re.match(r"^[-*]\s+\[([ xX])\]\s+(.+)$", line.strip())
        if todo:
            checked = todo.group(1).lower() == "x"
            text = todo.group(2).strip()
            blocks.append(_make_todo(text, checked))
            i += 1
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", line.strip())
        if bullet:
            blocks.append(_make_list_item(bullet.group(1).strip(), numbered=False))
            i += 1
            continue

        numbered = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if numbered:
            blocks.append(_make_list_item(numbered.group(1).strip(), numbered=True))
            i += 1
            continue

        paragraph_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip():
            if (
                is_divider(lines[i])
                or is_code_fence(lines[i])
                or is_heading(lines[i])
                or is_quote(lines[i])
                or is_todo(lines[i])
                or is_bullet(lines[i])
                or is_numbered(lines[i])
            ):
                break
            paragraph_lines.append(lines[i])
            i += 1
        blocks.append(_make_paragraph("\n".join(paragraph_lines).strip()))

    return blocks


def _chunked(items: list[dict[str, Any]], chunk_size: int) -> Iterable[list[dict[str, Any]]]:
    for i in range(0, len(items), chunk_size):
        yield items[i : i + chunk_size]


@dataclass(frozen=True)
class UploadItem:
    source_path: Path
    rel_path: Path
    title: str
    sha256: str
    blocks: list[dict[str, Any]]


def _iter_upload_items(ready_dir: Path, include_ext: set[str]) -> list[UploadItem]:
    items: list[UploadItem] = []
    # lv2는 "단일 폴더(Flat)"만 지원합니다. (하위 폴더/재귀 탐색 없음)
    for path in sorted(ready_dir.iterdir()):
        if path.is_dir():
            continue
        if path.name.startswith("."):
            continue
        rel = path.relative_to(ready_dir)
        ext = path.suffix.lower().lstrip(".")
        if ext not in include_ext:
            continue

        title = path.stem  # 확장자 제외
        content = _read_text_file(path)
        content = _drop_first_h1(content) if ext == "md" else content
        blocks = markdown_to_notion_blocks(content)
        if not blocks:
            blocks = [_make_paragraph("")]

        items.append(
            UploadItem(
                source_path=path,
                rel_path=rel,
                title=title,
                sha256=_sha256(path),
                blocks=blocks,
            )
        )
    return items


def _safe_move(src: Path, src_root: Path, dest_root: Path) -> Path:
    rel = src.relative_to(src_root)
    dest = dest_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        dest = dest.with_name(f"{dest.stem}_{_now_ms_compact()}{dest.suffix}")

    shutil.move(str(src), str(dest))
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="(lv2) Outbox(01_ready)의 파일을 Notion으로 단방향 업로드하고 단계 폴더로 자동 이동합니다. (단일 폴더/하위폴더 미지원)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without moving files or calling Notion API.")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to process (0 = no limit).")
    parser.add_argument(
        "--include-ext",
        nargs="+",
        default=["md", "txt"],
        help="Include text file extensions (default: md txt). (주의: pdf/docx/xlsx/pptx 등 바이너리/오피스 파일은 업로드 불가)",
    )
    parser.add_argument(
        "--select-uploadpage-id",
        dest="upload_page_id",
        default=None,
        help="업로드 대상 Notion 부모 페이지 ID override (기본: NOTION_UPLOAD_DEFAULT_PAGE_ID)",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output.")
    args = parser.parse_args()

    repo_root = _find_repo_root(Path.cwd())
    _load_dotenv(repo_root)

    include_ext = {ext.lower().lstrip(".") for ext in args.include_ext}

    ready_dir = _resolve_dir(repo_root, os.getenv("NOTION_UPLOAD_READY_DIR"), DEFAULT_UPLOAD_READY_REL)
    inprogress_dir = _resolve_dir(repo_root, os.getenv("NOTION_UPLOAD_INPROGRESS_DIR"), DEFAULT_UPLOAD_INPROGRESS_REL)
    complete_dir = _resolve_dir(repo_root, os.getenv("NOTION_UPLOAD_COMPLETE_DIR"), DEFAULT_UPLOAD_COMPLETE_REL)
    failed_dir = _resolve_dir(repo_root, os.getenv("NOTION_UPLOAD_FAILED_DIR"), DEFAULT_UPLOAD_FAILED_REL)

    for d in (ready_dir, inprogress_dir, complete_dir, failed_dir):
        d.mkdir(parents=True, exist_ok=True)

    # 단일 폴더 운영 가이드(초보자 보호): 하위 폴더가 있으면 경고(내용은 처리하지 않음)
    subdirs = sorted([p.name for p in ready_dir.iterdir() if p.is_dir() and not p.name.startswith(".")])
    if subdirs:
        print(
            f"[warn] ready_dir에 하위 폴더가 있습니다(lv2는 단일 폴더만 지원). 하위 폴더는 무시됩니다: {', '.join(subdirs)}",
            file=sys.stderr,
        )

    unsupported = sorted(
        [
            p.name
            for p in ready_dir.iterdir()
            if p.is_file() and not p.name.startswith(".") and p.suffix.lower().lstrip(".") not in include_ext
        ]
    )
    if unsupported:
        shown = ", ".join(unsupported[:10])
        more = f" (+{len(unsupported) - 10} more)" if len(unsupported) > 10 else ""
        print(f"[warn] ready_dir에 지원하지 않는 확장자 파일이 있어 무시됩니다: {shown}{more}", file=sys.stderr)

    items = _iter_upload_items(ready_dir, include_ext=include_ext)
    if args.limit and args.limit > 0:
        items = items[: args.limit]

    print(f"repo_root: {repo_root}")
    print(f"ready_dir: {ready_dir}")
    print(f"files: {len(items)}")

    if not items:
        return 0

    notion_token = os.getenv("NOTION_TOKEN", "").strip()
    parent_page_id = (args.upload_page_id or os.getenv("NOTION_UPLOAD_DEFAULT_PAGE_ID", "")).strip()

    if args.dry_run:
        print(f"notion_upload_root_page_id: {parent_page_id or '(missing)'}")
        for item in items:
            print(f"[dry-run] upload: {item.rel_path} -> title='{item.title}' (blocks={len(item.blocks)})")
        print("[dry-run] no file moves, no API calls")
        return 0

    if not notion_token:
        print("Missing NOTION_TOKEN in .env", file=sys.stderr)
        return 2
    if not parent_page_id:
        print("[ERROR] .env에 NOTION_UPLOAD_DEFAULT_PAGE_ID가 없습니다.", file=sys.stderr)
        return 2

    try:
        from notion_client import Client  # type: ignore
    except ImportError:
        print("Missing dependency: notion-client", file=sys.stderr)
        print("Install: python -m pip install -r .claude/skills/notion-download-lv2/requirements.txt", file=sys.stderr)
        return 2

    client = Client(auth=notion_token, notion_version="2022-06-28")

    for item in items:
        print(f"[start] {item.rel_path}")
        inprogress_path = _safe_move(item.source_path, src_root=ready_dir, dest_root=inprogress_dir)
        try:
            page = client.pages.create(
                parent={"page_id": parent_page_id},
                properties={
                    "title": {
                        "title": [
                            {"type": "text", "text": {"content": item.title[:2000]}},
                        ]
                    }
                },
            )
            page_id = page.get("id")
            if not page_id:
                raise RuntimeError("Notion API returned page without id")

            for chunk in _chunked(item.blocks, chunk_size=100):
                client.blocks.children.append(block_id=page_id, children=chunk)

            # Metadata Injection
            page_url = page.get("url")
            upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            frontmatter = f"""---
title: "{item.title}"
notion_url: "{page_url}"
uploaded_at: "{upload_time}"
notion_page_id: "{page_id}"
notion_parent_page_id: "{parent_page_id}"
---

"""
            original_content = _read_text_file(inprogress_path)
            inprogress_path.write_text(frontmatter + original_content, encoding="utf-8")

            complete_path = _safe_move(inprogress_path, src_root=inprogress_dir, dest_root=complete_dir)
            print(f"[done]  {item.rel_path} -> {complete_path.relative_to(complete_dir)}")
            if args.verbose:
                print(f"        page_id={page_id} url={page_url}")
        except Exception as e:
            failed_path = _safe_move(inprogress_path, src_root=inprogress_dir, dest_root=failed_dir)
            err_path = failed_path.with_suffix(failed_path.suffix + ".error.txt")
            err_text = "\n".join(
                [
                    f"time_ms={_now_ms_compact()}",
                    f"rel_path={item.rel_path}",
                    f"error={type(e).__name__}: {e}",
                    "traceback:",
                    traceback.format_exc(),
                ]
            )
            err_path.write_text(err_text, encoding="utf-8")
            print(f"[fail]  {item.rel_path} -> {failed_path.relative_to(failed_dir)}", file=sys.stderr)
            continue

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
