from django.db import models
from dataclasses import dataclass, field


# Create your models here.
@dataclass
class Suggestion:
    name: str
    longitute: float
    latitute: float
    distance_diff: float = field(repr=False, default=0.0)
    score: float = None
