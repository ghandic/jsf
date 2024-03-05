import logging
import random
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import ConfigDict

from jsf.schema_types.base import BaseSchema, ProviderNotSetException

logger = logging.getLogger()
_types = {"string": str, "integer": int, "number": float}


class JSFEnum(BaseSchema):
    enum: Optional[List[Union[str, int, float, dict, None]]] = []
    model_config = ConfigDict()

    def generate(self, context: Dict[str, Any]) -> Optional[Union[str, int, float]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return random.choice(self.enum)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "JSFEnum":
        return JSFEnum(**d)

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        base = _types.get(self.type, str)
        _type = Enum(
            value=self._get_unique_name(context),
            type=base,
            names={str(v): v for v in self.enum},
        )
        context["__internal__"][_type.__name__] = _type
        return self.to_pydantic(context, _type)
