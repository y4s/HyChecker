import requests
import time
import os
import sys
import re

API_URL = "https://api.hytl.tools/check/{}"

# Use a file passed as argument or default to name.txt in script folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "name.txt")
if len(sys.argv) > 1:
    FILE_PATH = sys.argv[1]

# Output files
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "name_checked.txt")
AVAILABLE_FILE = os.path.join(SCRIPT_DIR, "available_names.txt")
UNAVAILABLE_FILE = os.path.join(SCRIPT_DIR, "unavailable_names.txt")

def normalize_name(name):
    """Normalize username: lowercase, remove spaces/dashes, keep only a-z, 0-9, underscore."""
    name = name.replace(" ", "").replace("-", "").lower()
    # Keep only letters, digits, and underscore
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name

def check_name(name):
    """Check availability of a username via the API."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://hytl.tools/",
        "Origin": "https://hytl.tools"
    }

    try:
        response = requests.get(
            API_URL.format(name.strip()),
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            return "✔️" if data.get("available") else "❌"

        elif response.status_code == 403:
            return "error 403 (blocked)"

        else:
            return f"error {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"error {e}"

def load_existing(file_path):
    """Load existing usernames from a file into a set."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return set(line.strip().split(" (")[0] for line in f if line.strip())
    return set()

def main():
    # Verify the input file exists
    if not os.path.exists(FILE_PATH):
        print(f"File not found: {FILE_PATH}")
        return

    # Read new usernames from file, normalize, filter out names <3 or >16 characters
    skipped = []
    new_lines = []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            raw_name = line.strip()
            if not raw_name:
                continue
            name = normalize_name(raw_name)
            if len(name) < 3 or len(name) > 16:
                skipped.append(raw_name)
                continue
            new_lines.append(name)

    if skipped:
        print(f"⚠ Skipped {len(skipped)} usernames (too short, too long, or invalid chars): {', '.join(skipped)}")

    if not new_lines:
        print("⚠ No valid usernames to check (3–16 characters, letters/numbers/underscore only).")
        return

    # Load existing results to avoid duplicates
    checked_names = load_existing(OUTPUT_FILE)
    available_names_existing = load_existing(AVAILABLE_FILE)
    unavailable_names_existing = load_existing(UNAVAILABLE_FILE)

    output_lines = []
    available_names = set(available_names_existing)
    unavailable_names = set(unavailable_names_existing)

    print(f"\n🔎 Checking {len(new_lines)} new usernames...\n")
    for idx, line in enumerate(new_lines, start=1):
        # Skip if already checked
        if line in checked_names:
            print(f"{idx}/{len(new_lines)}: {line} → already checked")
            continue

        status = check_name(line)
        output_lines.append(f"{line} ({status})")

        # Separate files
        if status == "✔️":
            available_names.add(line)
        elif status == "❌":
            unavailable_names.add(line)

        print(f"{idx}/{len(new_lines)}: {line} → {status}")
        time.sleep(0.25)  # polite delay

    # Append new results to files
    if output_lines:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(output_lines) + "\n")

        with open(AVAILABLE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(available_names)) + "\n")

        with open(UNAVAILABLE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(unavailable_names)) + "\n")

    print(f"\n💠 [DONE]")
    print(f"\n> Updated files:")
    print(f"- {OUTPUT_FILE} (Full List)")
    print(f"- {AVAILABLE_FILE} (Available)")
    print(f"- {UNAVAILABLE_FILE} (Unavailable)")

if __name__ == "__main__":
    main()
