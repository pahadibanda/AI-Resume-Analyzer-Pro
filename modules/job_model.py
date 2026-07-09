from dataclasses import dataclass

@dataclass
class Job:
    company: str
    role: str
    location: str
    experience: str
    source: str
    apply_link: str