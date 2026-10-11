"""Small full-text corpus with immutable reviewed source binding."""
import hashlib
import json
import re
from pathlib import Path
from .schema import EvidenceRef
from .versions import verify_snapshot, sha256

LINKS = {
    'outage_credit': ['Rule 1','Rule 2','Rule 3','Rule 4','Rule 5','KB-1002','KB-1004','KB-1005','KB-1006','KB-1007','KB-1001'],
    'general_credit': ['Rule 1','Rule 2','Rule 4','Rule 5','KB-1001','KB-1002','KB-1006','KB-1007'],
    'outage_deadline': ['Rule 2','Rule 3','KB-1004','KB-1005'],
    'dispute_deadline': ['Rule 1','KB-1001'],
    'bill_explanation': ['KB-1003'],
}

class Corpus:
    def __init__(self, root: str | Path = '.'):
        self.root = Path(root)
        self.policy_snapshot = None
        if (self.root / 'manifest.json').exists():
            self.policy_snapshot = verify_snapshot(self.root)
            self.policy_snapshot = {**self.policy_snapshot,
                'manifest_sha256': sha256(self.root / 'manifest.json')}
        lock_path = self.root / 'config/corpus-lock.json'
        lock = json.loads(lock_path.read_text())
        self.entries: dict[str,EvidenceRef] = {}
        for relative, expected in lock['files'].items():
            path = self.root / relative
            raw = path.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if digest != expected:
                raise ValueError(f'Policy source changed: {relative}; review rules before updating corpus lock')
            lines = raw.decode().splitlines()
            starts = [(i, m.group(1)) for i,line in enumerate(lines)
                      if (m := re.match(r'^#{2,3} ((?:Rule \d+)|(?:KB-\d+))\b',line))]
            for index, (start, source_id) in enumerate(starts):
                end = starts[index+1][0] if index+1 < len(starts) else len(lines)
                self.entries[source_id] = EvidenceRef(document_id='BIL-POL-014' if source_id.startswith('Rule') else 'NimbusCare-KB', source_id=source_id,path=str(path.resolve()) if self.policy_snapshot else relative,start_line=start+1,end_line=end,excerpt='\n'.join(lines[start:end]).strip(),version=digest)
        if set(self.entries) != {*(f'Rule {n}' for n in range(1,6)), *(f'KB-{n}' for n in range(1001,1011))}:
            raise ValueError('Corpus must contain all five rules and all ten KB articles')
        self.version = hashlib.sha256(json.dumps(lock['files'],sort_keys=True).encode()).hexdigest()

    def get(self, source_id: str) -> EvidenceRef:
        return self.entries[source_id]

    def retrieve(self, query: str, intents: list[str]) -> list[EvidenceRef]:
        if any(x in ('taxes','unknown') for x in intents):
            return list(self.entries.values())
        words = set(re.findall(r'[a-z]{3,}',query.lower()))
        scores = [(len(words & set(re.findall(r'[a-z]{3,}',r.excerpt.lower()))), sid) for sid,r in self.entries.items()]
        ids = [sid for score,sid in sorted(scores,reverse=True)[:3] if score]
        for intent in intents:
            ids += LINKS.get(intent, [])
        return [self.get(sid) for sid in dict.fromkeys(ids)]
