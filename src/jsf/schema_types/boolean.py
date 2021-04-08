import random
from dataclasses import dataclass
from typing import Optional, Any, Dict

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Boolean(BaseSchema):
    def generate(self, state: Dict[str, Any]) -> Optional[bool]:
        try:
            return super().generate(state)
        except ProviderNotSetException:
            return random.choice([True, False])
