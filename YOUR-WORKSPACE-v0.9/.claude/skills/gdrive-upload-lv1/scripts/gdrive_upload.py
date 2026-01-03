#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google Drive 파일/폴더 업로드 모듈 (Lv1 - Outbox Workflow)
- Workflow Mode: Outbox(Ready -> InProgress -> Complete/Failed) 자동 처리
- Legacy Mode: 단일 파일/폴더 수동 업로드
"""

import os
import sys
import re
import shutil
import argparse
import mimetypes
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from googleapiclient.http import MediaFileUpload
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
    pattern = r'folders/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def get_folder_info(service, folder_id: str) -> dict:
    """
    폴더 정보 조회 (이름, 경로, 파일 수)

    Args:
        service: Drive API 서비스 객체
        folder_id: 폴더 ID

    Returns:
        dict: 폴더 정보
    """
    try:
        folder = service.files().get(
            fileId=folder_id,
            fields='id, name, parents, webViewLink'
        ).execute()

        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            fields='files(id, mimeType)',
            pageSize=100
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


def confirm_folder(folder_info: dict, action: str = "업로드") -> bool:
    """
    사용자에게 폴더 확인 요청

    Args:
        folder_info: 폴더 정보 딕셔너리
        action: 작업 유형

    Returns:
        bool: 확인 여부
    """
    print("\n" + "="*50)
    print(f"📁 대상 폴더 확인")
    print("="*50)
    print(f"  폴더명: {folder_info['name']}")
    print(f"  폴더 ID: {folder_info['id']}")
    print(f"  링크: {folder_info['link']}")
    print(f"  기존 파일: {folder_info['file_count']}개")
    if folder_info['folder_count'] > 0:
        print(f"  하위 폴더: {folder_info['folder_count']}개 (무시됨)")
    print("="*50)

    response = input(f"\n이 폴더로 {action}하시겠습니까? (y/n): ").strip().lower()
    return response in ['y', 'yes', '예']


# MIME 타입 매핑
MIME_TYPES = {
    '.md': 'text/markdown',
    '.txt': 'text/plain',
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.json': 'application/json',
    '.py': 'text/x-python',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.hwp': 'application/x-hwp',
    '.hwpx': 'application/hwp+zip',
}


def get_mime_type(file_path: Path) -> str:
    """파일의 MIME 타입 반환"""
    suffix = file_path.suffix.lower()
    if suffix in MIME_TYPES:
        return MIME_TYPES[suffix]
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type or 'application/octet-stream'


def find_or_create_folder(service, folder_name: str, parent_id: str = None) -> str:
    """
    드라이브에서 폴더를 찾거나 생성

    Args:
        service: Drive API 서비스 객체
        folder_name: 폴더 이름
        parent_id: 부모 폴더 ID (없으면 루트)

    Returns:
        str: 폴더 ID
    """
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=1
    ).execute()

    files = results.get('files', [])
    if files:
        return files[0]['id']

    # 폴더 생성
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    folder = service.files().create(
        body=file_metadata,
        fields='id'
    ).execute()

    print(f"  [+] 폴더 생성: {folder_name}")
    return folder.get('id')


def get_existing_files(service, folder_id: str) -> dict:
    """
    폴더 내 기존 파일 목록 조회 (증분 업로드용)

    Returns:
        dict: {파일명: {'id': id, 'modifiedTime': time}}
    """
    existing = {}
    page_token = None

    while True:
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name, modifiedTime)',
            pageToken=page_token,
            pageSize=100
        ).execute()

        for file in results.get('files', []):
            existing[file['name']] = {
                'id': file['id'],
                'modifiedTime': file.get('modifiedTime')
            }

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return existing


def upload_file(service, local_path: Path, folder_id: str = None,
                incremental: bool = False, existing_files: dict = None) -> dict:
    """
    단일 파일 업로드

    Args:
        service: Drive API 서비스 객체
        local_path: 로컬 파일 경로
        folder_id: 대상 드라이브 폴더 ID
        incremental: 증분 업로드 여부
        existing_files: 기존 파일 목록 (증분용)

    Returns:
        dict: 업로드된 파일 정보
    """
    file_name = local_path.name
    mime_type = get_mime_type(local_path)
    file_size = local_path.stat().st_size

    # 증분 업로드: 기존 파일 확인
    if incremental and existing_files and file_name in existing_files:
        print(f"  [SKIP] {file_name} (이미 존재)")
        return existing_files[file_name]

    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # 5MB 이상은 resumable upload
    if file_size > 5 * 1024 * 1024:
        media = MediaFileUpload(
            str(local_path),
            mimetype=mime_type,
            resumable=True,
            chunksize=1024*1024
        )
    else:
        media = MediaFileUpload(str(local_path), mimetype=mime_type)

    try:
        # 기존 파일이 있으면 업데이트
        if existing_files and file_name in existing_files:
            file = service.files().update(
                fileId=existing_files[file_name]['id'],
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            print(f"  [UPDATE] {file_name}")
        else:
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            print(f"  [UPLOAD] {file_name}")

        return file

    except HttpError as e:
        print(f"  [ERROR] {file_name}: {e}")
        return None


def upload_folder(service, local_folder: Path, remote_folder_name: str = None,
                  parent_id: str = None, incremental: bool = False) -> dict:
    """
    단일 폴더 내 파일만 업로드 (하위 폴더 제외)

    Args:
        service: Drive API 서비스 객체
        local_folder: 로컬 폴더 경로
        remote_folder_name: 드라이브 폴더 이름 (기본: 로컬 폴더명)
        parent_id: 부모 폴더 ID
        incremental: 증분 업로드 여부

    Returns:
        dict: 업로드 결과 통계
    """
    if remote_folder_name is None:
        remote_folder_name = local_folder.name

    folder_id = find_or_create_folder(service, remote_folder_name, parent_id)

    existing_files = {}
    if incremental:
        existing_files = get_existing_files(service, folder_id)

    stats = {'uploaded': 0, 'updated': 0, 'skipped': 0, 'errors': 0}

    for item in local_folder.iterdir():
        if item.name.startswith('.') or item.is_dir():
            continue

        if item.is_file():
            result = upload_file(
                service, item, folder_id,
                incremental=incremental,
                existing_files=existing_files
            )
            if result:
                if item.name in existing_files:
                    stats['updated'] += 1
                else:
                    stats['uploaded'] += 1
            else:
                stats['errors'] += 1

    return stats


def run_workflow_mode(service, dry_run=False, target_folder=None, limit=0, files_filter=None, verbose=False):
    """
    Outbox 워크플로우 실행 (Ready -> InProgress -> Complete/Failed)
    """
    print("="*50)
    print("Google Drive 업로드 (Workflow Mode)")
    print("="*50)

    # 설정 로드
    ready_dir = Path(os.getenv('GDRIVE_UPLOAD_READY_DIR', '02_outbox/01_ready')).resolve()
    inprogress_dir = Path(os.getenv('GDRIVE_UPLOAD_INPROGRESS_DIR', '02_outbox/02_inprogress')).resolve()
    complete_dir = Path(os.getenv('GDRIVE_UPLOAD_COMPLETE_DIR', '02_outbox/03_complete')).resolve()
    failed_dir = Path(os.getenv('GDRIVE_UPLOAD_FAILED_DIR', '02_outbox/04_failed')).resolve()

    root_folder_id = None
    
    if target_folder:
        root_folder_id = target_folder
        print(f"  [CONFIG] Target Overridden: {target_folder}")
    else:
        root_folder_id = os.getenv('GDRIVE_UPLOAD_DEFAULT_FOLDER_ID')
        print(f"  [CONFIG] Using Default Folder")

    # 디렉토리 확인
    for d in [ready_dir, inprogress_dir, complete_dir, failed_dir]:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            print(f"  [INFO] 폴더 생성: {d}")

    # 파일 스캔
    all_files = [f for f in ready_dir.iterdir() if f.is_file() and not f.name.startswith('.')]
    
    # --files 필터 적용
    if files_filter:
        files = [f for f in all_files if f.name in files_filter]
        if len(files) < len(files_filter):
            print(f"  [INFO] 요청한 {len(files_filter)}개 중 {len(files)}개 파일만 발견됨")
    else:
        files = all_files
    
    # --limit 적용
    if limit and limit > 0:
        files = files[:limit]
        
    if not files:
        print("  [INFO] 업로드할 파일이 없습니다 (Ready 폴더가 비어있음).")
        return

    print(f"  [READY] {len(files)}개 파일 대기 중")
    if limit:
        print(f"  [LIMIT] 최대 {limit}개 파일")

    if not root_folder_id and not dry_run:
        print("  [ERROR] GDRIVE_UPLOAD_DEFAULT_FOLDER_ID 환경변수가 설정되지 않았습니다.")
        return

    # ID가 URL 형식이면 파싱
    if root_folder_id and 'drive.google.com' in root_folder_id:
        parsed_id = parse_gdrive_url(root_folder_id)
        if parsed_id:
             print(f"  [INFO] URL에서 ID 추출: {parsed_id}")
             root_folder_id = parsed_id
        else:
             print(f"  [WARN] URL 파싱 실패, 원본 값 사용: {root_folder_id}")

    # 대상 폴더 정보 조회
    if not dry_run:
        folder_info = get_folder_info(service, root_folder_id)
        if not folder_info:
            print(f"  [ERROR] 대상 폴더(ID: {root_folder_id})를 찾을 수 없습니다.")
            return
        print(f"  [TARGET] {folder_info['name']} (ID: {root_folder_id})")

    if dry_run:
        print("\n[DRY-RUN] 실제 업로드나 이동은 수행되지 않습니다.")
        for f in files:
            print(f"  - [MOVE] {f.name} -> {inprogress_dir}")
            print(f"  - [UPLOAD] {f.name} -> Drive Folder({root_folder_id})")
            print(f"  - [MOVE] {f.name} -> {complete_dir}")
        return

    # 처리 시작
    success_count = 0
    fail_count = 0

    for file in files:
        file_name = file.name
        print(f"\nProcessing: {file_name}")

        try:
            # 1. Ready -> InProgress
            inprogress_path = inprogress_dir / file_name
            shutil.move(str(file), str(inprogress_path))
            print(f"  [MOVE] -> InProgress")

            # 2. Upload
            result = upload_file(service, inprogress_path, root_folder_id)

            if result:
                # 3. Success -> Complete
                complete_path = complete_dir / file_name
                if complete_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    complete_path = complete_dir / f"{file.stem}_{timestamp}{file.suffix}"
                
                shutil.move(str(inprogress_path), str(complete_path))
                print(f"  [MOVE] -> Complete")
                success_count += 1
            else:
                raise Exception("Upload failed (returned None)")

        except Exception as e:
            # 4. Fail -> Failed
            print(f"  [ERROR] {e}")
            failed_path = failed_dir / file_name
            src_path = inprogress_dir / file_name
            if not src_path.exists():
                src_path = ready_dir / file_name
            
            if src_path.exists():
                 if failed_path.exists():
                     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                     failed_path = failed_dir / f"{file.stem}_{timestamp}{file.suffix}"
                 shutil.move(str(src_path), str(failed_path))
                 print(f"  [MOVE] -> Failed")
            
            fail_count += 1

    print("\n" + "="*50)
    print("작업 완료")
    print(f"성공: {success_count}, 실패: {fail_count}")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(
        description='Google Drive에 파일/폴더 업로드 (Lv1 - Outbox Workflow)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # [권장] Outbox 워크플로우 실행 (.env 설정 필요)
  python gdrive_upload.py

  # 단일 파일 업로드
  python gdrive_upload.py report.pdf

  # 폴더 내 파일만 업로드
  python gdrive_upload.py ./my-project --folder-name "Projects"
        """
    )

    parser.add_argument('path', nargs='?', help='업로드할 파일 또는 폴더 경로 (생략 시 워크플로우 모드)')
    parser.add_argument('--dry-run', action='store_true', help='[Workflow] 실행 시뮬레이션 (실제 업로드 없음)')
    parser.add_argument('--select-uploadpage-id', dest='select_upload_id', help='[Workflow] 업로드할 구글 드라이브 폴더 지정 (URL 또는 ID)')
    parser.add_argument('--limit', type=int, default=0, help='[Workflow] 업로드할 최대 파일 수 (0 = 무제한)')
    parser.add_argument('--files', nargs='+', help='[Workflow] 특정 파일만 업로드 (파일명 목록)')
    parser.add_argument('--verbose', '-v', action='store_true', help='[Workflow] 상세 출력')
    # Legacy 옵션 (하위 호환성)
    parser.add_argument('--targetfolder', help='--select-uploadpage-id와 동일 (하위 호환)')
    parser.add_argument('--url', help='대상 드라이브 폴더 URL')
    parser.add_argument('--folder-id', help='대상 드라이브 폴더 ID')
    parser.add_argument('--folder-name', help='대상 드라이브 폴더 이름')
    parser.add_argument('--incremental', '-i', action='store_true', help='변경된 파일만 업로드')
    parser.add_argument('--yes', '-y', action='store_true', help='확인 없이 바로 진행')

    args = parser.parse_args()
    service = get_drive_service()

    # target 결정
    target = args.select_upload_id or args.targetfolder

    # 1. 워크플로우 모드 (path 인자가 없는 경우)
    if not args.path:
        run_workflow_mode(
            service, 
            dry_run=args.dry_run, 
            target_folder=target,
            limit=args.limit,
            files_filter=args.files,
            verbose=args.verbose
        )
        return

    # 2. 레거시 모드 (기존 로직)
    local_path = Path(args.path).resolve()
    if not local_path.exists():
        print(f"[ERROR] 경로를 찾을 수 없습니다: {local_path}")
        sys.exit(1)

    print("="*50)
    print("Google Drive 업로드 (Legacy Mode)")
    print("="*50)
    print(f"소스: {local_path}")

    # 대상 폴더 설정
    parent_id = None

    if args.url:
        parent_id = parse_gdrive_url(args.url)
        if not parent_id:
            print(f"[ERROR] 올바른 Google Drive 폴더 URL이 아닙니다: {args.url}")
            sys.exit(1)
        print(f"URL에서 폴더 ID 추출: {parent_id}")

    elif args.targetfolder:
        if 'drive.google.com' in args.targetfolder:
            parent_id = parse_gdrive_url(args.targetfolder)
        else:
            parent_id = args.targetfolder
        print(f"[CONFIG] Target Folder: {parent_id}")

    elif args.folder_id:
        parent_id = args.folder_id

    elif args.folder_name:
        parent_id = find_or_create_folder(service, args.folder_name)

    # 폴더 확인
    if parent_id:
        folder_info = get_folder_info(service, parent_id)
        if folder_info and not args.yes:
             if not confirm_folder(folder_info, "업로드"):
                 print("\n[취소] 업로드가 취소되었습니다.")
                 sys.exit(0)

    start_time = datetime.now()

    if local_path.is_file():
        result = upload_file(service, local_path, parent_id)
        if result:
            print("\n" + "="*50)
            print("업로드 완료!")
            if 'webViewLink' in result:
                print(f"링크: {result['webViewLink']}")
    else:
        stats = upload_folder(
            service, local_path,
            remote_folder_name=args.folder_name or local_path.name,
            parent_id=parent_id if args.folder_name else None,
            incremental=args.incremental
        )

        elapsed = (datetime.now() - start_time).total_seconds()
        print("\n" + "="*50)
        print("업로드 완료!")
        print(f"  새 파일: {stats['uploaded']}개")
        print(f"  업데이트: {stats['updated']}개")
        print(f"  건너뜀: {stats['skipped']}개")
        print(f"  오류: {stats['errors']}개")
        print(f"  소요 시간: {elapsed:.1f}초")
        print("="*50)


if __name__ == "__main__":
    main()
