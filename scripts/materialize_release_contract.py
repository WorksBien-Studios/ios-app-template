#!/usr/bin/env python3
"""Generate WorksBien release automation files from APP_IDENTITY.json."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
IDENTITY_PATH = ROOT / "APP_IDENTITY.json"
APP_MAP_PATH = ROOT / ".github" / "testflight-app-map.json"
LISTING_PATH = ROOT / "docs" / "app-store-listing-manifest.json"
APPLE_STANDARD_EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"


def load_identity() -> dict[str, Any]:
    with IDENTITY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def ordered_dump(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def build_app_map(identity: dict[str, Any]) -> dict[str, Any]:
    app = identity["app"]
    credentials = identity["credentials"]
    release = identity["release"]
    xcode = identity["xcode"]

    return {
        "schema_version": identity.get("schema_version", "1.0"),
        "state": identity.get("release_state", "draft"),
        "repository": identity["repository"],
        "bundle_id": app["bundle_id"],
        "team_id": app["team_id"],
        "asc_app_id": app["asc_app_id"],
        "credential_alias": credentials["credential_alias"],
        "asc_key_id": credentials["asc_key_id"],
        "asc_issuer_id": credentials["asc_issuer_id"],
        "private_key_secret_name": credentials["private_key_secret_name"],
        "runtime_env": {
            "key_id": "ASC_KEY_ID",
            "issuer_id": "ASC_ISSUER_ID",
            "private_key": "ASC_PRIVATE_KEY",
        },
        "beta_group_id": release["beta_group_id"],
        "listing_platform": release["listing_platform"],
        "marketing_version": release["marketing_version"],
        "xcode_container_type": xcode["container_type"],
        "xcode_container": xcode["container"],
        "scheme": xcode["scheme"],
        "required_check_name": xcode["required_check_name"],
        "signing_style": xcode["signing_style"],
        "export_method": xcode["export_method"],
        "signing_certificate": xcode["signing_certificate"],
    }


def build_listing_manifest(identity: dict[str, Any]) -> dict[str, Any]:
    app = identity["app"]
    listing = identity["listing"]

    return {
        "schema_version": identity.get("schema_version", "1.0"),
        "mode": listing.get("mode", "draft"),
        "app": {
            "app_id": app["asc_app_id"],
            "platform": "ios",
            "bundle_id": app["bundle_id"],
            "version": listing["version"],
            "company_name": app["company_name"],
            "release_kind": listing["release_kind"],
            "primary_category": app["primary_category"],
        },
        "source_control": {
            "fact_ledger_complete": False,
            "facts_reconciled": False,
        },
        "authorization": {
            "live_submission_authorized": False,
        },
        "human_review": {
            "attested": False,
        },
        "locales": [
            {
                "locale": locale["locale"],
                "claims_supported": locale.get("claims_supported", False),
                "name": locale["name"],
                "subtitle": locale["subtitle"],
                "promotional_text": locale.get("promotional_text", ""),
                "description": locale.get("description", ""),
                "keywords": locale.get("keywords", []),
                "support_url": listing["support_url"],
                "marketing_url": listing["marketing_url"],
                "privacy_url": listing["privacy_url"],
                "eula_url": locale.get("eula_url", APPLE_STANDARD_EULA),
                "whats_new": locale.get("whats_new", ""),
            }
            for locale in listing["locales"]
        ],
        "screenshots": listing.get("screenshots", []),
        "review": {
            "contact_complete": False,
            "notes": listing.get("review_notes", ""),
        },
        "compliance_controls": {
            "metadata_complete_accurate": {"status": "blocked"},
            "screenshots_authentic_current": {"status": "blocked"},
            "reviewer_access": {"status": "blocked"},
            "legal_urls_live": {"status": "blocked"},
            "privacy_policy_matches_build": {"status": "blocked"},
            "app_privacy_answers_match_build_and_sdks": {"status": "blocked"},
        },
    }


def write_or_check(path: pathlib.Path, content: str, check: bool) -> bool:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != content:
            print(f"{path.relative_to(ROOT)} is out of sync with APP_IDENTITY.json", file=sys.stderr)
            return False
        return True

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args()

    identity = load_identity()
    outputs = {
        APP_MAP_PATH: ordered_dump(build_app_map(identity)),
        LISTING_PATH: ordered_dump(build_listing_manifest(identity)),
    }

    ok = all(write_or_check(path, content, args.check) for path, content in outputs.items())
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
