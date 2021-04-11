from dataclasses import dataclass
from typing import Any, Dict

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Null(BaseSchema):
    def generate(self, context: Dict[str, Any]) -> None:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return None
