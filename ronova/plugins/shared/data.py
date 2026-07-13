from dataclasses import dataclass, field

@dataclass
class AfkState:
    status: bool = False
    reason: str | None = None
    afk_time: float | None = None
    file_type: str | None = None
    file_id: str | None = None
    users: list[int] = field(default_factory=list)


AFK_DATA = AfkState()