from dataclasses import dataclass
from enum import Enum

class EntityType(Enum):
    PERSON = "PER"
    LOCATION = "LOC"

@dataclass
class Entity:
    text: str
    type: EntityType
    count: int = 1