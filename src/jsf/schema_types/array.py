from dataclasses import dataclass
import random
from typing import Optional, List, Dict, Any

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Array(BaseSchema):
    items: Optional[BaseSchema] = None
    contains: Optional[BaseSchema] = None  # NOTE: Validation only
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False

    def generate(self, state: Dict[str, Any]) -> Optional[List[Any]]:
        try:
            return super().generate(state)
        except ProviderNotSetException:

            output = [self.items.generate(state) for _ in range(random.randint(self.minItems, self.maxItems))]
            if self.uniqueItems:
                output = set(output)
                while len(output) < self.minItems:
                    output.add(self.items.generate(state))
                output = list(output)
            return output

