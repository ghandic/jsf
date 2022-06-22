import random
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from .base import BaseSchema, ProviderNotSetException


class Array(BaseSchema):
    items: Optional[BaseSchema] = None
    contains: Optional[BaseSchema] = None  # NOTE: Validation only
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False
    fixed: Optional[Union[int, str]] = Field(None, alias="$fixed")

    def from_dict(d):
        return Array(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[List[Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:

            if isinstance(self.fixed, str):
                self.minItems = self.maxItems = eval(self.fixed, context)()
            elif isinstance(self.fixed, int):
                self.minItems = self.maxItems = self.fixed

            output = [self.items.generate(context) for _ in range(random.randint(self.minItems, self.maxItems))]
            if self.uniqueItems and self.items.type == "object":
                output = [dict(s) for s in set(frozenset(d.items()) for d in output)]
                while len(output) < self.minItems:
                    output.append(self.items.generate(context))
                    output = [dict(s) for s in set(frozenset(d.items()) for d in output)]
            elif self.uniqueItems:
                output = set(output)
                while len(output) < self.minItems:
                    output.add(self.items.generate(context))
                output = list(output)
            return output

    def model(self, context: Dict[str, Any]):
        _type = eval(f"List[Union[{','.join([self.items.model(context)[0].__name__])}]]", context["__internal__"])
        return self.to_pydantic(context, _type)
