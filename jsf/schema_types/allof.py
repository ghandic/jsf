from typing import Any, Dict, Optional

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class AllOf(BaseSchema):
    combined_schema: BaseSchema = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AllOf":
        return AllOf(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[Any]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return self.combined_schema.generate(context)

    def model(self, context: Dict[str, Any]) -> None:
        pass
