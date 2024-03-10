import random
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import Field

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class Array(BaseSchema):
    items: Optional[BaseSchema] = None
    contains: Optional[BaseSchema] = None  # NOTE: Validation only
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False
    fixed: Optional[Union[int, str]] = Field(None, alias="$fixed")

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Array":
        return Array(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[List[Any]]:
        try:
            return super().generate(context)
        except ProviderNotSetException:
            if isinstance(self.fixed, str):
                self.minItems = self.maxItems = eval(self.fixed, context)()
            elif isinstance(self.fixed, int):
                self.minItems = self.maxItems = self.fixed

            depth = context["state"]["__depth__"]
            output = []
            for _ in range(random.randint(int(self.minItems), int(self.maxItems))):
                output.append(self.items.generate(context))
                context["state"]["__depth__"] = depth
            if self.uniqueItems and self.items.type == "object":
                output = [dict(s) for s in {frozenset(d.items()) for d in output}]
                while len(output) < self.minItems:
                    output.append(self.items.generate(context))
                    output = [dict(s) for s in {frozenset(d.items()) for d in output}]
                    context["state"]["__depth__"] = depth
            elif self.uniqueItems:
                output = set(output)
                while len(output) < self.minItems:
                    output.add(self.items.generate(context))
                    context["state"]["__depth__"] = depth
                output = list(output)
            return output

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        _type = eval(
            f"List[Union[{','.join([self.items.model(context)[0].__name__])}]]",
            context["__internal__"],
        )
        return self.to_pydantic(context, _type)
