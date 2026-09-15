"""Restore the two supplied archives exactly; refuse unexpected paths or hashes."""
from pathlib import Path
import hashlib
import io
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / '.bootstrap'

def read_parts(names):
    return b''.join((BOOT / name).read_bytes() for name in names)

def safe_path(relative):
    p = ROOT / relative
    if Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError(f'Unsafe path: {relative}')
    if not p.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError(f'Escaping path: {relative}')
    return p

def write_once(relative, data):
    p = safe_path(relative)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(data)

if (ROOT / 'provenance/REMOTE_INITIALIZED.json').exists():
    raise RuntimeError('Initialization has already completed')
parity = read_parts(['parity-00.part', 'parity-02-small.part',
                     'parity-03-small.part', 'parity-04-small.part'] +
                    [f'parity_tail_{i:02}.part' for i in range(13)])
# The identical compressed circuit fixture occurs in both original archives.
# Reusing those bytes reduces transfer; the complete archive hash still governs.
matched = (read_parts([f'matched_tail_{i:02}.part' for i in range(13)]) +
           (BOOT / 'matched_bridge.part').read_bytes() + parity[11975:16154] +
           read_parts([f'matched_end_{i:02}.part' for i in range(13)]))
manifest = json.loads((ROOT / 'provenance/INPUTS.json').read_text())
archives = [parity, matched]
for data, spec in zip(archives, manifest['imports'], strict=True):
    if hashlib.sha256(data).hexdigest() != spec['sha256']:
        raise ValueError(f'Archive transfer mismatch: {spec["archive"]}')
    write_once(spec['archive'], data)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP checksum failure')
        seen = set()
        for item in z.infolist():
            if item.is_dir():
                continue
            member = Path(item.filename)
            if '..' in member.parts or member.is_absolute():
                raise ValueError('Unsafe ZIP member')
            rel = member.relative_to(spec['archive_prefix'])
            dest = Path(spec['extracted_directory']) / rel
            if dest in seen:
                raise ValueError('Duplicate ZIP member')
            seen.add(dest)
            write_once(dest.as_posix(), z.read(item))
for patch in json.loads((BOOT / 'preserved_logs.json').read_text()):
    original = safe_path(patch['source']).read_bytes()
    data = original
    for start, stop, replacement in reversed(patch['edits']):
        data = data[:start] + replacement.encode('utf-8') + data[stop:]
    if hashlib.sha256(data).hexdigest() != patch['sha256']:
        raise ValueError('Historical log restoration mismatch')
    write_once(patch['destination'], data)
write_once('validation/bootstrap/matched/01-validate.log',
           (ROOT / 'validation/bootstrap/matched/validation.json').read_bytes())
(ROOT / 'validation/initialization').mkdir(parents=True, exist_ok=True)
print('Restored both original ZIPs, 22 scientific files, and preserved bootstrap logs.')
