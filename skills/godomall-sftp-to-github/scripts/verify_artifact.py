"""Verify preserved artifact bytes without executing their contents."""
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


def compare_streams(source, candidate, allow_trailing=False):
    source_hash = hashlib.sha256()
    candidate_hash = hashlib.sha256()
    source_bytes = candidate_bytes = 0
    prefix = True
    while True:
        block = candidate.read(1024 * 1024)
        if not block:
            break
        original = source.read(len(block))
        source_hash.update(original)
        source_bytes += len(original)
        candidate_hash.update(block)
        candidate_bytes += len(block)
        if block[:len(original)] != original:
            prefix = False
    while True:
        remainder = source.read(1024 * 1024)
        if not remainder:
            break
        source_hash.update(remainder)
        source_bytes += len(remainder)
    prefix = prefix and source_bytes > 0 and candidate_bytes >= source_bytes
    exact = prefix and source_bytes == candidate_bytes
    return {
        'verified': exact or (allow_trailing and prefix),
        'exact': exact,
        'source_bytes': source_bytes,
        'candidate_bytes': candidate_bytes,
        'source_sha256': source_hash.hexdigest(),
        'candidate_sha256': candidate_hash.hexdigest(),
        'source_is_prefix': prefix,
        'trailing_bytes': candidate_bytes - source_bytes if prefix else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--url')
    target.add_argument('--file', type=Path)
    parser.add_argument('--allow-trailing-response', action='store_true', help='Diagnostic: accept source prefix plus extra response bytes.')
    args = parser.parse_args()
    if args.source.stat().st_size == 0:
        parser.error('Source artifact is empty.')
    if args.url:
        if not args.url.startswith('https://'):
            parser.error('Use HTTPS.')
        candidate = urlopen(Request(args.url, headers={'User-Agent': 'artifact-verifier/1.0'}), timeout=60)
    else:
        candidate = args.file.open('rb')
    with args.source.open('rb') as source, closing(candidate):
        result = compare_streams(source, candidate, args.allow_trailing_response)
    print(json.dumps(result, indent=2))
    return 0 if result['verified'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
