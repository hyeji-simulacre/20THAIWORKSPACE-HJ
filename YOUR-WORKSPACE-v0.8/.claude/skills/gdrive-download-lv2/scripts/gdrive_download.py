#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google Drive 파일/폴더 다운로드 모듈 (Lv2 - Inbox Workflow)
- Workflow Mode: Inbox(01_inbox/05_gdrive) 자동 다운로드
- Legacy Mode: 단일 폴더 수동 다운로드
"""

import os
import sys
import re
import argparse
import fnmatch
import io
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# 같은 폴더의 인증 모듈 import
try:
    from gdrive_auth import get_drive_service, PROJECT_ROOT
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from gdrive_auth import get_drive_service, PROJECT_ROOT

# .env 로드
load_dotenv(PROJECT_ROOT / '.env')


def parse_gdrive_url(url: str) -> str:
    """
    Google Drive URL에서 폴더 ID 추출
    Args:
        url: Google Drive 폴더 URL
    Returns:
        str: 폴더 ID 또는 None
    """
    # 패턴 1: 폴더 (folders/ID)
    folder_match = re.search(r'folders/([a-zA-Z0-9_-]+)', url)
    if folder_match:
        return folder_match.group(1)
        
    # 패턴 2: 파일 (/d/ID, /file/d/ID, open?id=ID)
    file_match = re.search(r'(?:/d/|id=)([a-zA-Z0-9_-]+)', url)
    if file_match:
        return file_match.group(1)
        
    return None


def get_folder_info(service, folder_id: str) -> dict:
    """폴더 정보 조회 (이름, 경로, 파일 수)"""
    try:
        folder = service.files().get(
            fileId=folder_id,
            fields='id, name, parents, webViewLink'
        ).execute()

        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query, fields='files(id, mimeType)', pageSize=100
        ).execute()

        files = results.get('files', [])
        file_count = sum(1 for f in files if f['mimeType'] != 'application/vnd.google-apps.folder')
        folder_count = sum(1 for f in files if f['mimeType'] == 'application/vnd.google-apps.folder')

        return {
            'id': folder['id'],
            'name': folder['name'],
            'link': folder.get('webViewLink', ''),
            'file_count': file_count,
            'folder_count': folder_count
        }
    except HttpError as e:
        print(f"[ERROR] 폴더 정보 조회 실패: {e}")
        return None


def confirm_folder(folder_info: dict, action: str = "다운로드") -> bool:
    """사용자에게 폴더 확인 요청"""
    print("\n" + "="*50)
    print(f"📁 소스 폴더 확인")
    print("="*50)
    print(f"  폴더명: {folder_info['name']}")
    print(f"  폴더 ID: {folder_info['id']}")
    print(f"  링크: {folder_info['link']}")
    print(f"  파일: {folder_info['file_count']}개")
    if folder_info['folder_count'] > 0:
        print(f"  하위 폴더: {folder_info['folder_count']}개 (무시됨)")
    print("="*50)

    response = input(f"\n이 폴더에서 {action}하시겠습니까? (y/n): ").strip().lower()
    return response in ['y', 'yes', '예']


# Google Workspace 파일 내보내기 형식
EXPORT_MIME_TYPES = {
    'application/vnd.google-apps.document': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'),
    'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
    'application/vnd.google-apps.presentation': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx'),
    'application/vnd.google-apps.drawing': ('application/pdf', '.pdf'),
}


def find_folder_by_name(service, folder_name: str, parent_id: str = None) -> str:
    """
    폴더 이름으로 ID 찾기 (중복 시 사용자 선택)
    """
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name, createdTime, parents, webViewLink)',
        pageSize=10
    ).execute()

    files = results.get('files', [])
    if not files:
        return None

    if len(files) == 1:
        return files[0]['id']

    # 중복 발견 시 사용자 선택
    print(f"\n⚠️ '{folder_name}' 폴더가 {len(files)}개 발견되었습니다.")
    print("-" * 60)
    print(f"{'No':<3} | {'Created':<20} | {'Parent':<20} | {'ID'}")
    print("-" * 60)

    for i, f in enumerate(files):
        parent_name = "Unknown"
        if 'parents' in f:
             try:
                 p_info = service.files().get(fileId=f['parents'][0], fields='name').execute()
                 parent_name = p_info.get('name', 'Unknown')
             except:
                 pass
        
        c_time = f.get('createdTime', '')[:16].replace('T', ' ')
        print(f"{i+1:<3} | {c_time:<20} | {parent_name:<20} | {f['id']}")
    print("-" * 60)

    while True:
        try:
            sel = input(f"다운로드할 폴더 번호를 선택하세요 (1-{len(files)}, 0: 취소): ").strip()
            if not sel.isdigit():
                continue
            idx = int(sel)
            if idx == 0:
                print("선택 취소됨.")
                return None
            if 1 <= idx <= len(files):
                return files[idx-1]['id']
        except ValueError:
            pass
            
    return None


def list_files_in_folder(service, folder_id: str) -> list:
    """폴더 내 모든 파일/폴더 목록 조회"""
    items = []
    page_token = None

    while True:
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType, size)',
            pageToken=page_token,
            pageSize=100
        ).execute()

        items.extend(results.get('files', []))

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return items


def download_file(service, file_id: str, file_name: str, mime_type: str,
                  local_path: Path, overwrite: bool = False) -> bool:
    """단일 파일 다운로드 (충돌 시 타임스탬프 저장)"""
    
    # 중복 처리 로직
    if local_path.exists() and not overwrite:
        timestamp = datetime.now().strftime("_%Y%m%d%H%M%S%f")[:-3]
        suffix = local_path.suffix
        stem = local_path.stem
        new_name = f"{stem}{timestamp}{suffix}"
        local_path = local_path.parent / new_name
        print(f"  [CONFLICT] 이름 중복 -> 변경 저장: {new_name}")

    try:
        # Google Workspace 파일은 내보내기
        if mime_type in EXPORT_MIME_TYPES:
            export_mime, ext = EXPORT_MIME_TYPES[mime_type]
            if not file_name.endswith(ext):
                file_name = file_name + ext
                local_path = local_path.parent / file_name

            request = service.files().export_media(
                fileId=file_id,
                mimeType=export_mime
            )
            print(f"  [EXPORT] {file_name}")
        else:
            request = service.files().get_media(fileId=file_id)
            print(f"  [DOWNLOAD] {file_name}")

        # 다운로드 실행
        file_handle = io.BytesIO()
        downloader = MediaIoBaseDownload(file_handle, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # 파일 저장
        local_path.parent.mkdir(parents=True, exist_ok=True)
        with open(local_path, 'wb') as f:
            f.write(file_handle.getvalue())

        return True

    except HttpError as e:
        print(f"  [ERROR] {file_name}: {e}")
        return False


def download_folder(service, folder_id: str, local_folder: Path,
                    file_filter: str = None, overwrite: bool = False,
                    limit: int = 0, dry_run: bool = False) -> dict:
    """단일 폴더 내 파일만 다운로드 (하위 폴더 제외)
    
    Args:
        limit: 다운로드할 최대 파일 수 (0 = 무제한)
        dry_run: True면 실제 다운로드 없이 대상 파일만 출력
    """
    local_folder.mkdir(parents=True, exist_ok=True)

    stats = {'downloaded': 0, 'skipped': 0, 'errors': 0}

    items = list_files_in_folder(service, folder_id)
    
    # 하위 폴더 제외한 파일만 필터링
    file_items = [item for item in items if item['mimeType'] != 'application/vnd.google-apps.folder']
    
    # limit 적용
    if limit and limit > 0:
        file_items = file_items[:limit]

    for item in file_items:
        item_name = item['name']
        item_id = item['id']
        mime_type = item['mimeType']

        # 필터 적용
        if file_filter and not fnmatch.fnmatch(item_name, file_filter):
            continue

        local_path = local_folder / item_name
        
        if dry_run:
            print(f"  [DRY-RUN] {item_name} -> {local_path}")
            stats['downloaded'] += 1
            continue
            
        success = download_file(
            service, item_id, item_name, mime_type,
            local_path, overwrite=overwrite
        )

        if success:
            if local_path.exists():
                stats['downloaded'] += 1
            else:
                stats['skipped'] += 1
        else:
            stats['errors'] += 1

    return stats


def run_workflow_mode(service, target_folder=None, dry_run: bool = False, limit: int = 0, verbose: bool = False):
    """Inbox 워크플로우 모드 실행"""
    print("="*50)
    print("Google Drive 다운로드 (Inbox Workflow Mode)")
    print("="*50)

    # 설정 로드
    download_dir = Path(os.getenv('GDRIVE_DOWNLOAD_DIR', '01_inbox/05_gdrive/01_ready')).resolve()
    
    root_folder_id = None
    
    if target_folder:
        root_folder_id = target_folder
        print(f"  [CONFIG] Target Overridden: {target_folder}")
    else:
        root_folder_id = os.getenv('GDRIVE_DOWNLOAD_DEFAULT_FOLDER_ID')
        print(f"  [CONFIG] Using Default Folder")

    if not root_folder_id:
        print("  [ERROR] GDRIVE_DOWNLOAD_DEFAULT_FOLDER_ID 환경변수가 설정되지 않았습니다.")
        return

    # ID가 URL 형식이면 파싱
    if 'drive.google.com' in root_folder_id:
        parsed_id = parse_gdrive_url(root_folder_id)
        if parsed_id:
             print(f"  [INFO] URL에서 ID 추출: {parsed_id}")
             root_folder_id = parsed_id
        else:
             print(f"  [WARN] URL 파싱 실패, 원본 값 사용: {root_folder_id}")

    # 대상 확인 (파일 vs 폴더)
    is_file = False
    try:
        file_meta = service.files().get(fileId=root_folder_id, fields='id, name, mimeType').execute()
        if file_meta['mimeType'] != 'application/vnd.google-apps.folder':
            is_file = True
            print(f"  [TARGET] Single File Detected: {file_meta['name']}")
    except HttpError:
        pass

    if is_file:
         download_file(
            service, file_meta['id'], file_meta['name'], file_meta['mimeType'],
            download_dir / file_meta['name'], overwrite=True
         )
         print(f"  [DOWNLOAD] Single file downloaded to {download_dir}")
         return

    # 폴더인 경우 기존 로직 수행
    folder_info = get_folder_info(service, root_folder_id)
    if not folder_info:
        print(f"  [ERROR] 소스 폴더(ID: {root_folder_id})를 찾을 수 없습니다.")
        return
    
    print(f"  [SOURCE] {folder_info['name']} (ID: {root_folder_id})")
    print(f"  [INBOX ] {download_dir}")
    if dry_run:
        print(f"  [MODE  ] DRY-RUN (실제 다운로드 없음)")
    if limit:
        print(f"  [LIMIT ] 최대 {limit}개 파일")
    if verbose:
        print(f"  [VERBOSE] 상세 출력 활성화")

    start_time = datetime.now()

    stats = download_folder(service, root_folder_id, download_dir, overwrite=False, limit=limit, dry_run=dry_run)

    elapsed = (datetime.now() - start_time).total_seconds()

    print("\n" + "="*50)
    print("다운로드 완료!")
    print(f"  다운로드: {stats['downloaded']}개")
    print(f"  건너뜀: {stats['skipped']}개")
    print(f"  오류: {stats['errors']}개")
    print(f"  소요 시간: {elapsed:.1f}초")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(
        description='Google Drive에서 파일/폴더 다운로드 (Lv2 - Inbox Workflow)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # [권장] Inbox 워크플로우 실행 (.env 설정 필요)
  python gdrive_download.py

  # 드라이브 URL로 다운로드
  python gdrive_download.py --url "https://drive.google.com/drive/folders/1ABC123xyz" "D:\\Downloads"

  # 폴더 이름으로 다운로드
  python gdrive_download.py "SharedDocs" "D:\\Downloads\\shared"
        """
    )

    parser.add_argument('--select-downloadpage-id', dest='select_download_id', help='[Workflow] 다운로드할 구글 드라이브 폴더 지정 (URL 또는 ID)')
    parser.add_argument('--dry-run', action='store_true', help='[Workflow] 실제 다운로드 없이 대상 파일 목록만 출력')
    parser.add_argument('--limit', type=int, default=0, help='[Workflow] 다운로드할 최대 파일 수 (0 = 무제한)')
    parser.add_argument('--select-name', dest='select_name', help='[Workflow] 특정 파일명 필터 (예: *.pdf, *.docx)')
    parser.add_argument('--verbose', '-v', action='store_true', help='[Workflow] 상세 출력')
    # Legacy 옵션 (하위 호환성)
    parser.add_argument('--target-download', dest='target_download_legacy', help='--select-downloadpage-id와 동일')
    parser.add_argument('--targetfolder', help='--select-downloadpage-id와 동일 (하위 호환)')

    parser.add_argument('source', nargs='?', help='드라이브 폴더 이름')
    parser.add_argument('destination', nargs='?', help='로컬 저장 경로')
    parser.add_argument('--url', help='드라이브 폴더 URL')
    parser.add_argument('--folder-id', help='드라이브 폴더 ID (이름 대신 사용)')
    parser.add_argument('--filter', help='--select-name과 동일')
    parser.add_argument('--overwrite', action='store_true', help='기존 파일 덮어쓰기')
    parser.add_argument('--yes', '-y', action='store_true', help='확인 없이 바로 진행')

    args = parser.parse_args()
    service = get_drive_service()

    target = args.select_download_id or args.target_download_legacy or args.targetfolder
    file_filter = args.select_name or args.filter

    # 1. 워크플로우 모드 (인자가 없는 경우)
    if not args.source and not args.url and not args.folder_id:
        run_workflow_mode(
            service, 
            target_folder=target, 
            dry_run=args.dry_run, 
            limit=args.limit,
            verbose=args.verbose
        )
        return

    # 2. 레거시 모드
    if not args.destination:
        print("[ERROR] Legacy 모드에서는 저장 경로(destination)가 필수입니다.")
        sys.exit(1)

    local_path = Path(args.destination).resolve()

    print("="*50)
    print("Google Drive 다운로드 (Legacy Mode)")
    print("="*50)

    folder_id = None

    if args.url:
        folder_id = parse_gdrive_url(args.url)
        if not folder_id:
            print(f"[ERROR] 올바른 Google Drive 폴더 URL이 아닙니다: {args.url}")
            sys.exit(1)
        print(f"URL에서 폴더 ID 추출: {folder_id}")
    elif args.folder_id:
        folder_id = args.folder_id
    elif args.source:
        folder_id = find_folder_by_name(service, args.source)
        if not folder_id:
            print(f"[ERROR] 폴더를 찾을 수 없습니다: {args.source}")
            sys.exit(1)

    if not args.yes:
        folder_info = get_folder_info(service, folder_id)
        if folder_info:
            if not confirm_folder(folder_info, "다운로드"):
                print("\n[취소] 다운로드가 취소되었습니다.")
                sys.exit(0)
    else:
        folder_info = get_folder_info(service, folder_id)
        if folder_info:
            print(f"소스 폴더: {folder_info['name']}")

    print(f"저장 위치: {local_path}")
    if args.filter:
        print(f"필터: {args.filter}")

    start_time = datetime.now()

    stats = download_folder(
        service, folder_id, local_path,
        file_filter=args.filter,
        overwrite=args.overwrite
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    print("\n" + "="*50)
    print("다운로드 완료!")
    print(f"  다운로드: {stats['downloaded']}개")
    print(f"  건너뜀: {stats['skipped']}개")
    print(f"  오류: {stats['errors']}개")
    print(f"  소요 시간: {elapsed:.1f}초")
    print("="*50)


if __name__ == "__main__":
    main()
