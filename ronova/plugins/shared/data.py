from dataclasses import dataclass, field

@dataclass
class PremiumState:
    status: bool = False
    text: str | None = None

PREMIUM_STATE = PremiumState()
