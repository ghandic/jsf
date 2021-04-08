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
            if self.uniqueItems:
                output = []
                for _ in range(random.randint(self.minItems, self.maxItems)):
                    tmp = set()
                    tries = 0
                    item = 0
                    while len(tmp) < len(self.items):
                        last_len = len(tmp)
                        tmp.add(self.items[item].generate(state))
                        if len(tmp) > last_len:
                            item += 1
                        tries += 1
                        if tries > 100:  # pragma: no cover
                            break
                    output.append(tuple(tmp))
                return output
            return [
                tuple([item.generate(state) for item in self.items])
                for _ in range(random.randint(self.minItems, self.maxItems))
            ]

