import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from dataclasses_json import config, dataclass_json

from .base import BaseSchema, ProviderNotSetException


@dataclass_json
@dataclass
class Tuple(BaseSchema):
    items: Optional[List[BaseSchema]] = None
    additionalItems: Optional[Union[bool, BaseSchema]] = None  # TODO: Random additional items to be appended
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False
    fixed: Optional[Union[str, int]] = field(default=None, metadata=config(field_name="$fixed"))

    def generate(self, context: Dict[str, Any]) -> Optional[List[Tuple]]:
        # TODO:  Random drop out "It’s ok to not provide all of the items"
        try:
            return super().generate(context)
        except ProviderNotSetException:

            if isinstance(self.fixed, str):
                self.minItems = self.maxItems = eval(self.fixed, context)()
            elif isinstance(self.fixed, int):
                self.minItems = self.maxItems = self.fixed

            if self.uniqueItems:
                output = []
                for _ in range(random.randint(self.minItems, self.maxItems)):
                    tmp = set()
                    tries = 0
                    item = 0
                    while len(tmp) < len(self.items):
                        last_len = len(tmp)
                        tmp.add(self.items[item].generate(context))
                        if len(tmp) > last_len:
                            item += 1
                        tries += 1
                        if tries > 100:  # pragma: no cover
                            break
                    output.append(tuple(tmp))
                return output
            return [
                tuple([item.generate(context) for item in self.items])
                for _ in range(random.randint(self.minItems, self.maxItems))
            ]

