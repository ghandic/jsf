import random
from dataclasses import dataclass
from typing import List, Union, Optional, Any, Dict

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Enum(BaseSchema):
    enum: List[Union[str, int, float]] = None

    def generate(self, state: Dict[str, Any]) -> Optional[Union[str, int, float]]:
        try:
            return super().generate(state)
        except ProviderNotSetException:
            return random.choice(self.enum)

