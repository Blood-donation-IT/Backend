from __future__ import annotations

import base64
import binascii
import json
import os
import re
from typing import Any

import firebase_admin
from firebase_admin import credentials


def _strip_bom(s: str) -> str:
    return s.lstrip("\ufeff")


def _strip_outer_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1].strip()
    return s


def _normalize_env_json_string(raw: str) -> str:
    raw = _strip_bom((raw or "").strip())
    raw = _strip_outer_quotes(raw)
    raw = _strip_outer_quotes(raw)
    return raw.strip()


def _try_parse_json_dict(text: str) -> dict[str, Any] | None:
    try:
        val = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(val, dict):
        return val
    return None


def _parse_base64_json(text: str) -> dict[str, Any] | None:
    cleaned = re.sub(r"\s+", "", text)
    if not cleaned:
        return None
    pad = len(cleaned) % 4
    if pad:
        cleaned += "=" * (4 - pad)
    try:
        decoded = base64.b64decode(cleaned, validate=False)
    except binascii.Error:
        return None
    try:
        s = decoded.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return _try_parse_json_dict(s)


def _normalize_private_key_field(data: dict[str, Any]) -> dict[str, Any]:
    pk = data.get("private_key")
    if not isinstance(pk, str) or not pk.strip():
        return data
    if "\\n" in pk and pk.count("\n") < 2 and "BEGIN" in pk:
        out = dict(data)
        out["private_key"] = pk.replace("\\n", "\n")
        return out
    return data


def parse_firebase_service_account_json(raw: str) -> dict[str, Any]:
    normalized = _normalize_env_json_string(raw)
    if not normalized:
        raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON is empty")

    json_err: json.JSONDecodeError | None = None
    data: dict[str, Any] | None = None
    try:
        val = json.loads(normalized)
        if isinstance(val, dict):
            data = val
    except json.JSONDecodeError as e:
        json_err = e

    if data is None:
        data = _parse_base64_json(normalized)

    if data is None:
        hint = ""
        if json_err is not None:
            hint = f" ({json_err.msg} at position {json_err.pos})"
        raise ValueError(
            "FIREBASE_SERVICE_ACCOUNT_JSON must be valid JSON (whole service account object) "
            + hint
        )

    required = ("type", "project_id", "private_key_id", "private_key", "client_email")
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise ValueError(
            "FIREBASE_SERVICE_ACCOUNT_JSON is missing required fields: "
            + ", ".join(missing)
        )

    return _normalize_private_key_field(data)


def try_initialize_firebase() -> bool:
    if firebase_admin._apps:
        return True

    raw = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON") or ""
    if raw.strip():
        data = parse_firebase_service_account_json(raw)
        try:
            cred = credentials.Certificate(data)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            raise ValueError(
                "Firebase Admin could not initialize from FIREBASE_SERVICE_ACCOUNT_JSON"
            ) from e
        return True

    return False


def firebase_configured() -> bool:
    return bool(firebase_admin._apps)
