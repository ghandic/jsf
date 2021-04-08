import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from .base import BaseSchema, ProviderNotSetException


@dataclass
class Tuple(BaseSchema):
    items: Optional[List[BaseSchema]] = None
    additionalItems: Optional[Union[bool, BaseSchema]] = None  # TODO: Random additional items to be appended
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False

    def generate(self, state: Dict[str, Any]) -> Optional[List[Tuple]]:
        # TODO:  Random drop out "It’s ok to not provide all of the items"
        try:
            return super().generate(state)
        except ProviderNotSetException:
            return [
                tuple([item.generate(state) for item in self.items])
                for _ in range(random.randint(self.minItems, self.maxItems))
            ]
