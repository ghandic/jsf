import logging
import random
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import rstr
from pydantic import BaseModel, create_model

from jsf.schema_types.base import BaseSchema, ProviderNotSetException

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

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Object":
        return Object(**d)

    def should_keep(self, property_name: str, context: Dict[str, Any]) -> bool:
        if isinstance(self.required, list) and property_name in self.required:
            return True
        return (
            random.uniform(0, 1) > self.allow_none_optionals
            and context["state"]["__depth__"] <= self.max_recursive_depth
        )

    def generate(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            explicit_properties = {
                o.name: o.generate(context)
                for o in self.properties
                if self.should_keep(o.name, context)
            }
            pattern_props = {}
            if self.patternProperties:
                for o in self.patternProperties:
                    for _ in range(random.randint(0, 10)):
                        if self.should_keep(o.name, context):
                            pattern_props[rstr.xeger(o.name)] = o.generate(context)
            return {**pattern_props, **explicit_properties}

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        self.generate(context)
        name = self._get_unique_name(context)
        _type = create_model(name, **{o.name: o.model(context) for o in self.properties})
        context["__internal__"][_type.__name__] = _type
        return self.to_pydantic(context, _type)


Object.model_rebuild()
