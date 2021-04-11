import math
import random
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Number(BaseSchema):
    multipleOf: Optional[float] = None
    minimum: Optional[float] = 0
    exclusiveMinimum: Optional[float] = None
    maximum: Optional[float] = 9999
    exclusiveMaximum: Optional[float] = None
    # enum: List[Union[str, int, float]] = None  # NOTE: Not used - enums go to enum class

    def generate(self, context: Dict[str, Any]) -> Optional[float]:
        try:
            return super().generate(context)
        except ProviderNotSetException:

            step = self.multipleOf if self.multipleOf is not None else 1

            if isinstance(self.exclusiveMinimum, bool):
                _min = self.minimum + step
            elif isinstance(self.exclusiveMinimum, int):
                _min = self.exclusiveMinimum + step
            else:
                _min = self.minimum

            if isinstance(self.exclusiveMaximum, bool):
                _max = self.maximum - step
            elif isinstance(self.exclusiveMaximum, int):
                _max = self.exclusiveMaximum - step
            else:
                _max = self.maximum

            return float(step * random.randint(math.ceil(float(_min) / step), math.floor(float(_max) / step)))


class Integer(Number):
    def generate(self, context: Dict[str, Any]) -> Optional[int]:
        return int(super().generate(context))
