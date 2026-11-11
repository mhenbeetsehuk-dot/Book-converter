"""Safe, auditable capability research registry. No arbitrary code execution."""
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
import json

ALLOWED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "GPL-3.0", "LGPL-3.0", "MPL-2.0", "CC0-1.0"}

@dataclass
class Capability:
    name: str
    task: str
    source_url: str
    license_id: str
    method: str
    status: str = "researched"
    test_evidence: str = ""
    approved_by: str = ""

    def validate(self):
        parsed = urlparse(self.source_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("Source must be an HTTPS URL")
        if self.license_id not in ALLOWED_LICENSES:
            raise ValueError("License needs manual review before integration")
        if self.status not in {"researched", "prototype", "tested", "approved"}:
            raise ValueError("Unknown capability status")
        if self.status == "approved" and (not self.test_evidence or not self.approved_by):
            raise ValueError("Approval requires test evidence and a reviewer")

def save_capability(capability: Capability, directory: str = "capabilities") -> Path:
    capability.validate()
    folder = Path(directory)
    folder.mkdir(parents=True, exist_ok=True)
    slug = "".join(c if c.isalnum() or c in "-_" else "-" for c in capability.name.lower()).strip("-")
    if not slug:
        raise ValueError("Capability needs a valid name")
    path = folder / (slug + ".json")
    path.write_text(json.dumps(asdict(capability), indent=2), encoding="utf-8")
    return path

def load_capability(path: str) -> Capability:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    capability = Capability(**data)
    capability.validate()
    return capability
