import random
from typing import Any, Dict, List, Optional

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class AnyOf(BaseSchema):
    schemas: List[BaseSchema] = None

    @classmethod
    def from_dict(cls, d: Dict):
        return AnyOf(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[Any]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return random.choice(self.schemas).generate(context)

    def model(self, context: Dict[str, Any]):
        pass
