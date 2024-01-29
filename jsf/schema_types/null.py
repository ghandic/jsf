from typing import Any, Dict

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class Null(BaseSchema):
    def generate(self, context: Dict[str, Any]) -> None:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return None

    def model(self, context: Dict[str, Any]):
        return self.to_pydantic(context, type(None))

    @classmethod
    def from_dict(cls, d: Dict):
        return Null(**d)
