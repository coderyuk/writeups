# this involves downloading a requests module for python it performs the same function as curl
# pip install requests

import hashlib
import sys

import requests


def verify_url_content(url: str, expected_output: str, timeout: int = 10) -> bool:
    try:
        # Equivalent to running: curl -sL --max-time 10 "<url>"
        # -s silent -L follow redirects --max-time aborts process if time exceeded

        response = requests.get(url, timeout=timeout)

        response.raise_for_status()

        # Normalize whitespace to prevent false flags from trailing newlines
        actual_output = response.text.strip()
        expected_clean = expected_output.strip()

        if actual_output != expected_clean:
            print(f"[FLAGGED] Content mismatch for: {url}")
            print(f"  Expected: {expected_clean[:100]}")
            print(f"  Received: {actual_output[:100]}")
            return False

        print(f"[OK] Output matches expected content for: {url}")
        return True

    except requests.exceptions.RequestException as error:
        print(f"[FLAGGED] Request failed for: {url} ({error})")
        return False


if __name__ == "__main__":
    # Example endpoint that returns the decoded string "HTTPBIN is awesome"
    target_url = "http://chatelaine.cylabacademy.net:19297/profile/user/"
    i = 0
    expected_text = "User not found."
    while i < 3001:
        # Convert number to string, then encode to bytes
        number_bytes = str(i).encode("utf-8")
        hashnumber = hashlib.md5(number_bytes)
        target_url = f"{target_url}{hashnumber}"
        i += 1

    if not verify_url_content(target_url, expected_text):
        sys.exit(1)
