import random
from typing import Any, Dict, List, Optional

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class OneOf(BaseSchema):
    schemas: List[BaseSchema] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OneOf":
        return OneOf(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[List[Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            filtered_schemas = []
            if context["state"]["__depth__"] > self.max_recursive_depth:
                filtered_schemas = [schema for schema in self.schemas if not schema.is_recursive]
            return random.choice(filtered_schemas or self.schemas).generate(context)

    def model(self, context: Dict[str, Any]) -> None:
        pass
