import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Array(BaseSchema):
    items: Optional[BaseSchema] = None
    contains: Optional[BaseSchema] = None  # NOTE: Validation only
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False

    def generate(self, context: Dict[str, Any]) -> Optional[List[Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:

            output = [self.items.generate(context) for _ in range(random.randint(self.minItems, self.maxItems))]
            if self.uniqueItems:
                output = set(output)
                while len(output) < self.minItems:
                    output.add(self.items.generate(context))
                output = list(output)
            return output
