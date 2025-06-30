"""
SRI Hash Verification Script

This script verifies that the SRI hashes in your templates match the actual content
from the CDN URLs.
"""

import re
import requests
import hashlib
import base64
from pathlib import Path

def verify_sri_hash(url, expected_hash):
    """Verify that the SRI hash matches the actual content"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Extract algorithm and hash from expected_hash
        algorithm, expected_b64 = expected_hash.split('-', 1)

        # Calculate actual hash
        if algorithm == 'sha384':
            hasher = hashlib.sha384()
        elif algorithm == 'sha256':
            hasher = hashlib.sha256()
        elif algorithm == 'sha512':
            hasher = hashlib.sha512()
        else:
            return False, f"Unsupported algorithm: {algorithm}"

        hasher.update(response.content)
        actual_b64 = base64.b64encode(hasher.digest()).decode('ascii')

        if actual_b64 == expected_b64:
            return True, "✅ Hash matches"
        else:
            return False, f"❌ Hash mismatch. Expected: {expected_b64}, Got: {actual_b64}"

    except Exception as e:
        return False, f"❌ Error: {e}"

def extract_sri_from_template(file_path):
    """Extract SRI hashes from HTML template files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match integrity attributes
        pattern = r'(?:src|href)="([^"]+)"[^>]*integrity="([^"]+)"'
        matches = re.findall(pattern, content)

        return matches
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def main():
    print("🔒 SRI Hash Verification")
    print("=" * 40)

    template_files = [
        'templates/base.html',
        'templates/quiz.html'
    ]

    all_valid = True

    for template_file in template_files:
        print(f"\n📄 Checking {template_file}:")

        if not Path(template_file).exists():
            print(f"❌ File not found: {template_file}")
            all_valid = False
            continue

        sri_entries = extract_sri_from_template(template_file)

        if not sri_entries:
            print("ℹ️  No SRI hashes found in this file")
            continue

        for url, sri_hash in sri_entries:
            print(f"\n🔗 {url}")
            is_valid, message = verify_sri_hash(url, sri_hash)
            print(f"   {message}")

            if not is_valid:
                all_valid = False

    print(f"\n{'='*40}")
    if all_valid:
        print("🎉 All SRI hashes are valid!")
    else:
        print("⚠️  Some SRI hashes need to be updated")

    return all_valid

if __name__ == "__main__":
    main()
