import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from dataclasses_json import config, dataclass_json

from .base import BaseSchema, ProviderNotSetException


@dataclass_json
@dataclass
class Array(BaseSchema):
    items: Optional[BaseSchema] = None
    contains: Optional[BaseSchema] = None  # NOTE: Validation only
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False
    fixed: Optional[Union[str, int]] = field(default=None, metadata=config(field_name="$fixed"))

    def generate(self, context: Dict[str, Any]) -> Optional[List[Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:

            if isinstance(self.fixed, str):
                self.minItems = self.maxItems = eval(self.fixed, context)()
            elif isinstance(self.fixed, int):
                self.minItems = self.maxItems = self.fixed

            output = [self.items.generate(context) for _ in range(random.randint(self.minItems, self.maxItems))]
            if self.uniqueItems:
                output = set(output)
                while len(output) < self.minItems:
                    output.add(self.items.generate(context))
                output = list(output)
            return output
