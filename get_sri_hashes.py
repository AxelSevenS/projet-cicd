import hashlib
import base64
import requests

def get_sri_hash(url, algorithm='sha384'):
    """Get SRI hash for a given URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        content = response.content

        if algorithm == 'sha384':
            hasher = hashlib.sha384()
        elif algorithm == 'sha256':
            hasher = hashlib.sha256()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        hasher.update(content)
        hash_b64 = base64.b64encode(hasher.digest()).decode('ascii')

        return f"{algorithm}-{hash_b64}"

    except Exception as e:
        print(f"Error getting hash for {url}: {e}")
        return None

# URLs to get SRI hashes for
urls = {
    'Bootstrap CSS': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'Bootstrap JS': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'Font Awesome': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'Chart.js': 'https://cdn.jsdelivr.net/npm/chart.js'
}

print("SRI Hashes for External Resources:")
print("=" * 50)

for name, url in urls.items():
    print(f"\n{name}:")
    print(f"URL: {url}")
    sri_hash = get_sri_hash(url)
    if sri_hash:
        print(f"SRI: integrity=\"{sri_hash}\"")
    else:
        print("Failed to get SRI hash")
