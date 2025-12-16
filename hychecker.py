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
    return re.sub(r"[^a-z0-9_]", "", name)

def check_name(name, max_retries=5):
    """Check availability of a username via the API with retry/backoff handling."""
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

    delay = 1.0  # initial backoff

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                API_URL.format(name),
                headers=headers,
                timeout=8
            )

            if response.status_code == 200:
                data = response.json()
                return "✔️" if data.get("available") else "❌"

            if response.status_code == 429:
                print(f"⏳ {name} → rate limited (retry {attempt}/{max_retries}, waiting {delay:.1f}s)")
                time.sleep(delay)
                delay *= 2
                continue

            if response.status_code == 403:
                print(f"🚫 {name} → temporarily blocked (cooling down 10s)")
                time.sleep(10)
                continue

            return f"error {response.status_code}"

        except requests.exceptions.RequestException as e:
            print(f"⚠ {name} → network error ({e}), retrying in {delay:.1f}s")
            time.sleep(delay)
            delay *= 2

    return "error (max retries)"

def load_existing(file_path):
    """Load existing usernames from a file into a set."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return set(line.strip().split(" (")[0] for line in f if line.strip())
    return set()

def main():
    if not os.path.exists(FILE_PATH):
        print(f"File not found: {FILE_PATH}")
        return

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
        print(f"⚠ Skipped {len(skipped)} invalid usernames: {', '.join(skipped)}")

    if not new_lines:
        print("⚠ No valid usernames to check.")
        return

    checked_names = load_existing(OUTPUT_FILE)
    available_names = load_existing(AVAILABLE_FILE)
    unavailable_names = load_existing(UNAVAILABLE_FILE)

    output_lines = []

    print(f"\n🔎 Checking {len(new_lines)} usernames...\n")

    for idx, name in enumerate(new_lines, start=1):
        if name in checked_names:
            print(f"{idx}/{len(new_lines)}: {name} → already checked")
            continue

        status = check_name(name)
        output_lines.append(f"{name} ({status})")

        if status == "✔️":
            available_names.add(name)
        elif status == "❌":
            unavailable_names.add(name)

        print(f"{idx}/{len(new_lines)}: {name} → {status}")

        time.sleep(0.25)  # base delay between names

        # long cooldown every 100 requests (VERY IMPORTANT)
        if idx % 100 == 0:
            print("🛑 Cooling down for 30 seconds...")
            time.sleep(30)

    if output_lines:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(output_lines) + "\n")

        with open(AVAILABLE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(available_names)) + "\n")

        with open(UNAVAILABLE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(unavailable_names)) + "\n")

    print("\n💠 DONE")
    print("> Updated files:")
    print(f"- {OUTPUT_FILE}")
    print(f"- {AVAILABLE_FILE}")
    print(f"- {UNAVAILABLE_FILE}")

if __name__ == "__main__":
    main()
