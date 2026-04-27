from __future__ import annotations

import json
import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials


def try_initialize_firebase() -> bool:
    if firebase_admin._apps:
        return True

    raw = (os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON") or "").strip()
    if raw:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(
                "FIREBASE_SERVICE_ACCOUNT_JSON is not valid JSON"
            ) from e
        cred = credentials.Certificate(data)
        firebase_admin.initialize_app(cred)
        return True

    path = (os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or "").strip()
    if path and os.path.isfile(path):
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        return True

    return False


def firebase_configured() -> bool:
    return bool(firebase_admin._apps)
