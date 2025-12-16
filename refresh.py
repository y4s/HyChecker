#!/usr/bin/env python3

import requests
import os
import sys
import time

API_URL = "https://api.hytl.tools/check/{}"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

AVAILABLE_FILE = os.path.join(SCRIPT_DIR, "available_names.txt")
UNAVAILABLE_FILE = os.path.join(SCRIPT_DIR, "unavailable_names.txt")

TIMEOUT = 6
DELAY_BETWEEN = 0.25  # polite delay between successful checks

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://hytl.tools/",
    "Origin": "https://hytl.tools"
})

def load_set(path):
    """Load lines from a file into a set (stripped, non-empty)."""
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def write_atomic(path, lines):
    """Write lines to path atomically."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for ln in lines:
            f.write(f"{ln}\n")
    os.replace(tmp, path)

def check_name_api(name):
    """
    Return True if available, False if unavailable.
    Handles rate limits (429) by waiting and retrying indefinitely.
    Returns None only on unrecoverable errors.
    """

    retries = 0
    max_retries = 999999  # effectively unlimited

    while retries < max_retries:
        try:
            resp = SESSION.get(API_URL.format(name), timeout=TIMEOUT)

            # RATE LIMITED
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    wait_time = int(retry_after)
                else:
                    wait_time = 30  # fallback to known limit

                print(f" → Rate limited for '{name}'. Waiting {wait_time}s...")
                time.sleep(wait_time)
                retries += 1
                continue

            # OTHER NON-200 CODES
            if resp.status_code != 200:
                print(f" → API error {resp.status_code} for '{name}' — retrying in 3s")
                retries += 1
                time.sleep(3)
                continue

            # Parse response
            data = resp.json()
            return bool(data.get("available"))

        except requests.exceptions.RequestException as e:
            print(f" → Network error for '{name}': {e} — retrying in 5s")
            retries += 1
            time.sleep(5)
            continue

        except ValueError:
            print(f" → Invalid JSON for '{name}' — retrying in 3s")
            retries += 1
            time.sleep(3)
            continue

    # Never really hits this because of infinite retries
    return None

def main():
    if not os.path.exists(AVAILABLE_FILE):
        print(f"No {AVAILABLE_FILE} found. Nothing to check.")
        return

    available = list(sorted(load_set(AVAILABLE_FILE)))
    if not available:
        print(f"{AVAILABLE_FILE} is empty. Nothing to check.")
        return

    unavailable_set = load_set(UNAVAILABLE_FILE)
    still_available = []
    moved_to_unavailable = []

    print(f"Checking {len(available)} names from {AVAILABLE_FILE}...\n")

    for idx, name in enumerate(available, start=1):
        print(f"{idx}/{len(available)}: {name}", end="")
        is_avail = check_name_api(name)

        if is_avail is True:
            still_available.append(name)
            print(" → (still available) ✔️")

        elif is_avail is False:
            if name not in unavailable_set:
                unavailable_set.add(name)
                moved_to_unavailable.append(name)
            print(" → (moved to unavailable) ❌")

        else:
            still_available.append(name)
            print(" → error, kept for retry later")

        time.sleep(DELAY_BETWEEN)

    # Save results
    write_atomic(AVAILABLE_FILE, sorted(still_available))
    write_atomic(UNAVAILABLE_FILE, sorted(unavailable_set))

    # Summary
    print("\nSummary:")
    print(f"  Checked: {len(available)}")
    print(f"  Still available: {len(still_available)} ✔️")
    print(f"  Moved to unavailable: {len(moved_to_unavailable)} ❌")

    if moved_to_unavailable:
        print("  Names moved:")
        for n in moved_to_unavailable:
            print(f"   - {n}")

if __name__ == "__main__":
    main()
