"""Verify immutable input archives and their exact extracted file copies."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def checked_path(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError(f'Unsafe repository path: {relative}')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {relative}')
    return path

def verify(root: Path = ROOT) -> dict:
    manifest = json.loads((root / 'provenance/INPUTS.json').read_text())
    result = {'status': 'passed', 'archives': [], 'manifest_entries_checked': 0,
              'extracted_files_checked': 0, 'limitations':
              'Checks identity and internal consistency, not scientific correctness or authorship.'}
    for spec in manifest['imports']:
        archive = checked_path(root, spec['archive'])
        actual = sha256(archive.read_bytes())
        if actual != spec['sha256']:
            raise ValueError(f'Archive hash mismatch: {spec["archive"]}')
        extracted = checked_path(root, spec['extracted_directory'])
        count = 0
        with ZipFile(archive) as z:
            if z.testzip() is not None:
                raise ValueError(f'Corrupt ZIP: {archive}')
            for item in z.infolist():
                if item.is_dir():
                    continue
                rel = Path(item.filename).relative_to(spec['archive_prefix'])
                dest = checked_path(extracted, rel.as_posix())
                if dest.read_bytes() != z.read(item.filename):
                    raise ValueError(f'Extracted bytes differ: {dest}')
                count += 1
        supplied = json.loads(checked_path(root, spec['manifest']).read_text())
        for relative, expected in supplied.items():
            data = checked_path(extracted, relative).read_bytes()
            if sha256(data) != expected:
                raise ValueError(f'Packet manifest mismatch: {relative}')
        result['archives'].append({'path': spec['archive'], 'sha256': actual,
                                   'extracted_files': count, 'manifest_entries': len(supplied)})
        result['extracted_files_checked'] += count
        result['manifest_entries_checked'] += len(supplied)
    a, b = manifest['cross_import_equality']
    if checked_path(root, a).read_bytes() != checked_path(root, b).read_bytes():
        raise ValueError('Inherited circuit fixture differs between packets')
    provenance = json.loads((root / 'research/parity_frames/PROVENANCE.json').read_text())
    matched_sha = next(x['sha256'] for x in result['archives'] if 'matched_audit' in x['path'])
    if provenance.get('source_archive_sha256') != matched_sha:
        raise ValueError('Parity packet provenance does not identify the matched archive')
    result['inherited_fixture_equal'] = True
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, help='Optional new output file; will not overwrite')
    args = parser.parse_args()
    report = verify()
    text = json.dumps(report, indent=2) + '\n'
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        with args.json.open('x', encoding='utf-8') as handle:
            handle.write(text)
    print(text, end='')

if __name__ == '__main__':
    main()
