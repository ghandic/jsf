import logging
import random
from typing import Any, Dict, List, Optional, Union

from pydantic import create_model, BaseModel

from .base import BaseSchema, ProviderNotSetException

logger = logging.getLogger()


class PropertyNames(BaseModel):
    pattern: Optional[str] = None


PropertyDependency = Dict[str, List[str]]
SchemaDependency = Dict[str, "Object"]


class Object(BaseSchema):
    properties: Dict[str, BaseSchema] = {}
    additionalProperties: Optional[Union[bool, BaseSchema]] = None
    required: Optional[List[str]] = None
    propertyNames: Optional[PropertyNames] = None
    minProperties: Optional[int] = None
    maxProperties: Optional[int] = None
    dependencies: Optional[Union[PropertyDependency, SchemaDependency]] = None
    patternProperties: Optional[Dict[str, BaseSchema]] = None

    def from_dict(d):
        return Object(**d)

    def should_keep(self, property_name: str) -> bool:
        if isinstance(self.required, list) and property_name in self.required:
            return True
        return random.uniform(0, 1) < 0.5

    def generate(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return {o.name: o.generate(context) for o in self.properties if self.should_keep(o.name)}

    def model(self, context: Dict[str, Any]):
        self.generate(context)
        name = self._get_unique_name(context)
        _type = create_model(name, **{o.name: o.model(context) for o in self.properties})
        context["__internal__"][_type.__name__] = _type
        return self.to_pydantic(context, _type)


Object.update_forward_refs()
