import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Enum(BaseSchema):
    enum: List[Union[str, int, float]] = None

    def generate(self, context: Dict[str, Any]) -> Optional[Union[str, int, float]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return random.choice(self.enum)
