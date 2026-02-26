"""
Sync root config.yaml to all user configs under users/*/config.yaml.

Rules:
  - New keys in root config → added to user config (with root's default value)
  - Removed keys (in root but not in user) → removed from user config
  - Existing keys → user's value is preserved
"""

import os
import copy
import yaml


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_CONFIG = os.path.join(ROOT_DIR, "config.yaml")
USERS_DIR = os.path.join(ROOT_DIR, "users")


def deep_sync(template: dict, user: dict) -> dict:
    """
    Recursively sync user config against the template (root config).

    - Keys only in template → added with template's default value
    - Keys only in user → removed
    - Keys in both:
        - If both are dicts → recurse
        - Otherwise → keep user's value
    """
    result = {}
    for key in template:
        if key not in user:
            # New key from template, use default
            result[key] = copy.deepcopy(template[key])
        elif isinstance(template[key], dict) and isinstance(user[key], dict):
            # Both are dicts, recurse
            result[key] = deep_sync(template[key], user[key])
        else:
            # Key exists in both, keep user's value
            result[key] = user[key]
    # Keys only in user (not in template) are intentionally dropped
    return result


def sync_all_users():
    with open(ROOT_CONFIG, "r", encoding="utf-8") as f:
        root_config = yaml.safe_load(f)

    if not os.path.isdir(USERS_DIR):
        print(f"Users directory not found: {USERS_DIR}")
        return

    user_dirs = [
        d for d in os.listdir(USERS_DIR)
        if os.path.isdir(os.path.join(USERS_DIR, d))
    ]

    if not user_dirs:
        print("No user directories found.")
        return

    for username in user_dirs:
        user_config_path = os.path.join(USERS_DIR, username, "config.yaml")

        if not os.path.exists(user_config_path):
            # No config yet, copy the root config as-is
            with open(user_config_path, "w", encoding="utf-8") as f:
                yaml.dump(root_config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            print(f"[NEW]  {username} — created config from root template")
            continue

        with open(user_config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}

        synced = deep_sync(root_config, user_config)

        # Collect changes for logging
        added = find_diff_keys(root_config, user_config, mode="added")
        removed = find_diff_keys(user_config, root_config, mode="added")  # keys in user but not in root

        with open(user_config_path, "w", encoding="utf-8") as f:
            yaml.dump(synced, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        if added or removed:
            print(f"[SYNC] {username}")
            for k in added:
                print(f"       + {k}")
            for k in removed:
                print(f"       - {k}")
        else:
            print(f"[ OK ] {username} — already up to date")


def find_diff_keys(source: dict, target: dict, prefix: str = "", mode: str = "added") -> list:
    """Find keys present in source but missing in target (flat dotted paths)."""
    diffs = []
    for key in source:
        full_key = f"{prefix}.{key}" if prefix else str(key)
        if key not in target:
            diffs.append(full_key)
        elif isinstance(source[key], dict) and isinstance(target.get(key), dict):
            diffs.extend(find_diff_keys(source[key], target[key], full_key, mode))
    return diffs


if __name__ == "__main__":
    sync_all_users()
