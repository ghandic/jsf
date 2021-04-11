import random
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Boolean(BaseSchema):
    def generate(self, context: Dict[str, Any]) -> Optional[bool]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return random.choice([True, False])
