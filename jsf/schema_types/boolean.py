import random
from typing import Any, Dict, Optional

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class Boolean(BaseSchema):
    def generate(self, context: Dict[str, Any]) -> Optional[bool]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return random.choice([True, False])

    def model(self, context: Dict[str, Any]):
        return self.to_pydantic(context, bool)

    @classmethod
    def from_dict(cls, d: Dict):
        return Boolean(**d)
