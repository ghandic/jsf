import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from .base import BaseSchema, ProviderNotSetException


@dataclass
class PropertyNames:
    pattern: Optional[str]


PropertyDependency = Dict[str, List[str]]
SchemaDependency = Dict[str, "Object"]


@dataclass
class Object(BaseSchema):
    properties: Dict[str, BaseSchema] = None
    additionalProperties: Optional[Union[bool, BaseSchema]] = None
    required: Optional[List[str]] = None
    propertyNames: Optional[PropertyNames] = None
    minProperties: Optional[int] = None
    maxProperties: Optional[int] = None
    dependencies: Optional[Union[PropertyDependency, SchemaDependency]] = None
    patternProperties: Optional[Dict[str, BaseSchema]] = None

    def should_keep(self, property_name: str) -> bool:
        if isinstance(self.required, list) and property_name in self.required:
            return True
        return random.uniform(0, 1) < 0.5

    def generate(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return {o.name: o.generate(context) for o in self.properties if self.should_keep(o.name)}
