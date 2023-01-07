from typing import Any, Dict, Optional

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class AllOf(BaseSchema):
    combined_schema: BaseSchema = None

    def from_dict(d):
        return AllOf(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[Any]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return self.combined_schema.generate(context)

    def model(self, context: Dict[str, Any]):
        pass
