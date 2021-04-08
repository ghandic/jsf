from dataclasses import dataclass
from typing import Any, Dict

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Null(BaseSchema):
    def generate(self, state: Dict[str, Any]) -> None:
        try:
            return super().generate(state)
        except ProviderNotSetException:
            return None
