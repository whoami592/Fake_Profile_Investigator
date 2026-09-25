"""Local comparison engine. No network requests or identity inference."""
import hashlib
import html
import json
import re
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

CREDIT = 'Coded by Cyber Security Engineer Mr Sabaz Ali Khan'
NOTICE = ('Similarity is a review clue, not proof of impersonation or identity. '
          'Shared logos, templates and authorized accounts can look alike. '
          'Low similarity does not establish authenticity. Photo comparison is not face recognition.')
FIELDS = ('username', 'display_name', 'bio', 'url', 'photo')

def normalize(text):
    return ' '.join(unicodedata.normalize('NFKC', text).casefold().split())

def similarity(a, b):
    a, b = normalize(a), normalize(b)
    return round(100 * SequenceMatcher(None, a, b, autojunk=False).ratio(), 1) if a and b else None

def validate(case):
    if not isinstance(case, dict) or case.get('version') != 1:
        raise ValueError('Unsupported case format; expected version 1.')
    for key in ('reference', 'candidate'):
        p = case.get(key)
        if not isinstance(p, dict):
            raise ValueError('Both profiles are required.')
        for field in FIELDS:
            if not isinstance(p.get(field, ''), str) or len(p.get(field, '')) > 10000:
                raise ValueError('Profile fields must be text, at most 10,000 characters.')
    for field in ('title', 'notes', 'observed_at'):
        if not isinstance(case.get(field, ''), str) or len(case.get(field, '')) > 20000:
            raise ValueError('Invalid case metadata.')
    return case

def photo_info(path):
    from PIL import Image, ImageOps, ImageStat
    import warnings
    p = Path(path)
    if p.stat().st_size > 25 * 1024 * 1024:
        raise ValueError('Photo exceeds 25 MB.')
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(p) as src:
            if src.width * src.height > 20_000_000:
                raise ValueError('Photo exceeds 20 megapixels; use a smaller copy.')
            src.seek(0)
            im = ImageOps.exif_transpose(src).convert('RGB')
            size = im.size
            gray = im.convert('L')
            detail = ImageStat.Stat(gray.resize((32, 32))).stddev[0]
            thumb = gray.resize((9, 8))
            small = [thumb.getpixel((x, y)) for y in range(8) for x in range(9)]
            bits = [small[y*9+x] > small[y*9+x+1] for y in range(8) for x in range(8)]
    return {'file': p.name, 'sha256': digest, 'dimensions': list(size), 'bits': bits, 'detail': detail}

def compare(case):
    validate(case)
    a, b = case['reference'], case['candidate']
    metrics, clues = {}, []
    for field in ('username', 'display_name', 'bio'):
        av, bv = a.get(field, ''), b.get(field, '')
        if field == 'username':
            av, bv = av.strip().lstrip('@'), bv.strip().lstrip('@')
        score = similarity(av, bv)
        metrics[field] = score
        if score is not None and score >= 80:
            clues.append(f'{field.replace("_", " ").title()}: substantial text overlap ({score}%).')
    photos = {'status': 'Not compared: select a local photo for both profiles.'}
    if a.get('photo') and b.get('photo'):
        try:
            pa, pb = photo_info(a['photo']), photo_info(b['photo'])
            distance = sum(x != y for x, y in zip(pa['bits'], pb['bits']))
            identical = pa['sha256'] == pb['sha256']
            low_detail = min(pa['detail'], pb['detail']) < 8
            photos = {'status': 'Compared', 'exact_same_file': identical,
                      'dhash_distance_out_of_64': distance,
                      'low_detail_warning': low_detail,
                      'reference': {k:v for k,v in pa.items() if k not in ('bits','detail')},
                      'candidate': {k:v for k,v in pb.items() if k not in ('bits','detail')}}
            if identical:
                clues.append('Photos have identical SHA-256 hashes: same file bytes.')
            elif distance <= 8 and not low_detail:
                clues.append('Photos have similar coarse image structure; manually inspect for reused imagery.')
            if low_detail:
                clues.append('Low-detail photo detected: perceptual hash similarity is unreliable.')
        except Exception as exc:
            photos = {'status': f'Photo comparison unavailable: {exc}'}
    return {'generated_at': datetime.now(timezone.utc).isoformat(), 'text_similarity_percent': metrics,
            'photos': photos, 'clues': clues, 'notice': NOTICE,
            'method': 'NFKC/casefold text + SequenceMatcher; SHA-256 and 64-bit grayscale difference hash. No calibrated probability or fake-account verdict.'}

def load_case(path):
    p = Path(path)
    if p.stat().st_size > 1024*1024:
        raise ValueError('Case file exceeds 1 MB.')
    return validate(json.loads(p.read_text(encoding='utf-8')))

def save_case(path, case):
    validate(case)
    Path(path).write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding='utf-8')

def report_html(case, result):
    esc = lambda x: html.escape(str(x))
    sections = ''.join(f'<h2>{esc(k.title())} profile</h2><pre>{esc(json.dumps(case[k], ensure_ascii=False, indent=2))}</pre>' for k in ('reference','candidate'))
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Profile comparison report</title>'
            '<style>body{font:16px system-ui;max-width:950px;margin:40px auto;padding:20px;color:#172432}'
            'pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f5;padding:18px}h1{color:#126449}</style>'
            f'<h1>Fake Profile Investigator</h1><p>{esc(CREDIT)}</p><h2>{esc(case.get("title","Untitled"))}</h2>'
            f'<p>{esc(NOTICE)}</p><p>Observed at (user supplied): {esc(case.get("observed_at",""))}</p>'
            + sections + f'<h2>Comparison</h2><pre>{esc(json.dumps(result, ensure_ascii=False, indent=2))}</pre>'
            f'<h2>Investigator notes</h2><pre>{esc(case.get("notes",""))}</pre>'
            '<p>Preserve original screenshots and source URLs. Confirm account ownership through a separately trusted channel before taking action. Generated timestamps are local observations, not platform-certified evidence.</p></html>')
