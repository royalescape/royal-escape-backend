from enum import Enum


class PotStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    UPCOMING = "upcomming"


class PotType(str, Enum):
    ELECTRONICS = "electronics"
    TRAVEL = "travel"
