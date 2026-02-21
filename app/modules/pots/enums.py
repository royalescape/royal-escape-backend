from enum import Enum


class PotStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    UPCOMING = "upcoming"


class PotType(str, Enum):
    ELECTRONICS = "electronics"
    TRAVEL = "travel"
