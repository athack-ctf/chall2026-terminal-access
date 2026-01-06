#!/usr/bin/env python3
"""
Register a user, then perform the 2-step login:
1) POST /api/login/verify  -> get (user_id, token)
2) POST /api/login/session -> create Flask session (cookie) using Bearer token

Usage:
  python3 solution.py http://127.0.0.1:2026 username password
"""

import sys
import requests


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 solution.py <base_url> <username> <password>")
        raise SystemExit(1)

    base_url = sys.argv[1].rstrip("/")
    username = sys.argv[2]
    password = sys.argv[3]

    s = requests.Session()

    # Register
    r = s.post(f"{base_url}/register", json={"username": username, "password": password}, timeout=10)
    print("REGISTER:", r.status_code, r.text)

    # Verify credentials -> token + user_id
    r = s.post(f"{base_url}/api/login/verify", json={"username": username, "password": password}, timeout=10)
    print("VERIFY:", r.status_code, r.text)
    r.raise_for_status()
    data = r.json()
    user_id = data["user_id"]
    token = data["token"]

    print("Instead of the above user_id, we send user_id : 1, the first created user i.e the admin")

    # Create session using Bearer token
    r = s.post(
        f"{base_url}/api/login/session",
        json={"user_id": 1},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    print("SESSION:", r.status_code, r.text)

    # Show that we now have a session cookie stored in the Session
    print("COOKIES:", s.cookies.get_dict())


if __name__ == "__main__":
    main()
