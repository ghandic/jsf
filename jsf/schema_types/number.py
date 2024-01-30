import math
import random
from typing import Any, Dict, Optional, Tuple, Type, Union

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class Number(BaseSchema):
    multipleOf: Optional[Union[float, int]] = None
    minimum: Optional[Union[float, int]] = 0
    exclusiveMinimum: Optional[Union[bool, float, int]] = None
    maximum: Optional[Union[float, int]] = 9999
    exclusiveMaximum: Optional[Union[bool, float, int]] = None
    # enum: List[Union[str, int, float]] = None  # NOTE: Not used - enums go to enum class

    def generate(self, context: Dict[str, Any]) -> Optional[float]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            step = self.multipleOf if self.multipleOf is not None else 1

            if isinstance(self.exclusiveMinimum, bool):
                _min = self.minimum + step
            elif isinstance(self.exclusiveMinimum, (int, float)):
                _min = self.exclusiveMinimum + step
            else:
                _min = self.minimum

            if isinstance(self.exclusiveMaximum, bool):
                _max = self.maximum - step
            elif isinstance(self.exclusiveMaximum, (int, float)):
                _max = self.exclusiveMaximum - step
            else:
                _max = self.maximum

            return float(
                step * random.randint(math.ceil(float(_min) / step), math.floor(float(_max) / step))
            )

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        return self.to_pydantic(context, float)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Number":
        return Number(**d)


class Integer(Number):
    def generate(self, context: Dict[str, Any]) -> Optional[int]:
        n = super().generate(context)
        return int(n) if n is not None else n

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        return self.to_pydantic(context, int)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Integer":
        return Integer(**d)
