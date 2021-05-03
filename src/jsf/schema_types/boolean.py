import random
from typing import Any, Dict, Optional

from .base import BaseSchema, ProviderNotSetException


class Boolean(BaseSchema):
    def generate(self, context: Dict[str, Any]) -> Optional[bool]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return random.choice([True, False])

    def model(self, context: Dict[str, Any]):
        return self.to_pydantic(context, bool)

    def from_dict(d):
        return Boolean(**d)
