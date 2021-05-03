from typing import Any, Dict

from .base import BaseSchema, ProviderNotSetException


class Null(BaseSchema):
    def generate(self, context: Dict[str, Any]) -> None:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return None

    def model(self, context: Dict[str, Any]):
        return self.to_pydantic(context, type(None))

    def from_dict(d):
        return Null(**d)
