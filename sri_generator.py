#!/usr/bin/env python3
"""
SRI Hash Generator Utility

This script generates Subresource Integrity (SRI) hashes for external resources.
Usage: python sri_generator.py <URL>
"""

import hashlib
import base64
import requests
import sys
import argparse

def get_sri_hash(url, algorithm='sha384'):
    """
    Generate SRI hash for a given URL
    
    Args:
        url (str): The URL to fetch and hash
        algorithm (str): Hash algorithm to use (sha256, sha384, sha512)
    
    Returns:
        str: SRI hash string in format 'algorithm-base64hash'
    """
    try:
        print(f"Fetching content from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content = response.content
        print(f"Content size: {len(content)} bytes")

        # Select hasher based on algorithm
        if algorithm == 'sha256':
            hasher = hashlib.sha256()
        elif algorithm == 'sha384':
            hasher = hashlib.sha384()
        elif algorithm == 'sha512':
            hasher = hashlib.sha512()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        hasher.update(content)
        hash_b64 = base64.b64encode(hasher.digest()).decode('ascii')

        return f"{algorithm}-{hash_b64}"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error generating hash: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate SRI hashes for web resources')
    parser.add_argument('url', help='URL to generate SRI hash for')
    parser.add_argument('--algorithm', '-a', choices=['sha256', 'sha384', 'sha512'],
                       default='sha384', help='Hash algorithm to use (default: sha384)')
    parser.add_argument('--format', '-f', choices=['hash', 'html', 'both'],
                       default='both', help='Output format (default: both)')

    args = parser.parse_args()

    sri_hash = get_sri_hash(args.url, args.algorithm)

    if sri_hash:
        print(f"\n✅ SRI Hash Generated Successfully!")
        print(f"Algorithm: {args.algorithm}")
        print(f"URL: {args.url}")

        if args.format in ['hash', 'both']:
            print(f"\nSRI Hash: {sri_hash}")

        if args.format in ['html', 'both']:
            if args.url.endswith('.css'):
                print(f'\nHTML (CSS):')
                print(f'<link rel="stylesheet" href="{args.url}"')
                print(f'      integrity="{sri_hash}"')
                print(f'      crossorigin="anonymous">')
            elif args.url.endswith('.js'):
                print(f'\nHTML (JavaScript):')
                print(f'<script src="{args.url}"')
                print(f'        integrity="{sri_hash}"')
                print(f'        crossorigin="anonymous"></script>')
            else:
                print(f'\nHTML Attribute:')
                print(f'integrity="{sri_hash}" crossorigin="anonymous"')
    else:
        print("❌ Failed to generate SRI hash")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Interactive mode for common CDN resources
        print("SRI Hash Generator")
        print("=" * 20)
        print("\nCommon CDN Resources:")

        common_resources = {
            '1': ('Bootstrap 5.3.0 CSS', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'),
            '2': ('Bootstrap 5.3.0 JS', 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'),
            '3': ('Font Awesome 6.4.0', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'),
            '4': ('Chart.js Latest', 'https://cdn.jsdelivr.net/npm/chart.js'),
            '5': ('jQuery 3.7.0', 'https://code.jquery.com/jquery-3.7.0.min.js')
        }

        for key, (name, url) in common_resources.items():
            print(f"{key}. {name}")

        choice = input("\nSelect a resource (1-5) or enter custom URL: ").strip()

        if choice in common_resources:
            _, url = common_resources[choice]
        elif choice.startswith('http'):
            url = choice
        else:
            print("Invalid choice or URL")
            sys.exit(1)

        algorithm = input("Hash algorithm (sha384/sha256/sha512) [sha384]: ").strip() or 'sha384'

        sri_hash = get_sri_hash(url, algorithm)

        if sri_hash:
            print(f"\n✅ SRI Hash: {sri_hash}")
            print(f"\nHTML Attribute: integrity=\"{sri_hash}\" crossorigin=\"anonymous\"")
        else:
            print("❌ Failed to generate SRI hash")
    else:
        main()
