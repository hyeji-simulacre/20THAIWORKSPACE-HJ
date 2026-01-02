#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google Drive API 인증 모듈
- OAuth 2.0 인증 처리
- 토큰 관리 (자동 갱신)
- 서비스 객체 생성
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트 경로 설정 (스킬 폴더 기준으로 상위 5단계)
# .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/ → 프로젝트 루트
PROJECT_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(PROJECT_ROOT))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# .env 파일 로드 (있는 경우)
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

# API 스코프 - 드라이브 전체 접근
SCOPES = ['https://www.googleapis.com/auth/drive']

# 기본 경로 설정
DEFAULT_CREDENTIALS_PATH = PROJECT_ROOT / "credentials.json"
DEFAULT_TOKEN_PATH = PROJECT_ROOT / "token.json"


def get_credentials_path() -> Path:
    """credentials.json 경로 반환"""
    env_path = os.getenv("GDRIVE_CREDENTIALS_PATH")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    # 스킬 폴더 내 credentials.json 확인
    skill_creds = Path(__file__).parent.parent / "credentials.json"
    if skill_creds.exists():
        return skill_creds

    # 프로젝트 루트 확인
    if DEFAULT_CREDENTIALS_PATH.exists():
        return DEFAULT_CREDENTIALS_PATH

    return DEFAULT_CREDENTIALS_PATH


def get_token_path() -> Path:
    """token.json 경로 반환"""
    env_path = os.getenv("GDRIVE_TOKEN_PATH")
    if env_path:
        return Path(env_path)
    return DEFAULT_TOKEN_PATH


def authenticate() -> Credentials:
    """
    Google Drive API 인증 수행

    Returns:
        Credentials: 인증된 자격증명 객체
    """
    creds = None
    token_path = get_token_path()
    credentials_path = get_credentials_path()

    # 기존 토큰 확인
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"[WARN] 토큰 로드 실패: {e}")
            creds = None

    # 토큰이 없거나 만료된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[INFO] 토큰 갱신 중...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"[WARN] 토큰 갱신 실패: {e}")
                creds = None

        if not creds:
            # 새로 인증
            if not credentials_path.exists():
                print(f"[ERROR] credentials.json을 찾을 수 없습니다.")
                print(f"        예상 경로: {credentials_path}")
                print("\n[GUIDE] Google Cloud Console에서 OAuth 자격증명을 다운로드하세요:")
                print("        https://console.cloud.google.com/apis/credentials")
                sys.exit(1)

            print("[INFO] 브라우저에서 인증을 진행해주세요...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 토큰 저장
        with open(token_path, 'w', encoding='utf-8') as token_file:
            token_file.write(creds.to_json())
        print(f"[OK] 토큰 저장 완료: {token_path}")

    return creds


def get_drive_service():
    """
    Google Drive API 서비스 객체 반환

    Returns:
        Resource: Drive API 서비스 객체
    """
    creds = authenticate()
    return build('drive', 'v3', credentials=creds)


def test_connection():
    """연결 테스트 - 사용자 정보 출력"""
    try:
        service = get_drive_service()
        about = service.about().get(fields="user").execute()
        user = about.get('user', {})
        print("\n" + "="*50)
        print("Google Drive API 연결 성공!")
        print("="*50)
        print(f"  사용자: {user.get('displayName', 'N/A')}")
        print(f"  이메일: {user.get('emailAddress', 'N/A')}")
        print("="*50)
        return True
    except HttpError as e:
        print(f"[ERROR] API 오류: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 연결 실패: {e}")
        return False


if __name__ == "__main__":
    print("Google Drive API 인증 테스트")
    print("-" * 40)
    test_connection()
