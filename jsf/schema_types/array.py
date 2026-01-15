import random
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import Field

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class Array(BaseSchema):
    items: Optional[BaseSchema] = None
    contains: Optional[BaseSchema] = None  # NOTE: Validation only
    # If `items` is provided in the schema, JSON Schema treats the array as
    # having an item type.  In that case JSF should emit at least one element
    # by default.  Using ``None`` here allows us to distinguish between the
    # schema omitting ``minItems`` and explicitly setting ``minItems`` to ``0``
    # which callers may rely on.
    minItems: Optional[int] = None
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
            if self.items is None:
                # No item schema means we cannot infer what the array should
                # contain, therefore return an empty list.
                return []

            if isinstance(self.fixed, str):
                self.minItems = self.maxItems = eval(self.fixed, context)()
            elif isinstance(self.fixed, int):
                self.minItems = self.maxItems = self.fixed

            depth = context["state"]["__depth__"]

            # ``minItems`` may be ``None`` when it wasn't provided in the
            # schema.  In that scenario we want non-empty arrays if an item
            # schema exists.  When the user explicitly sets ``minItems`` to 0
            # we honour that and allow empty arrays.
            min_items = (
                int(self.minItems)
                if self.minItems is not None
                else (0 if self.items is None else 1)
            )
            max_items = int(self.maxItems) if self.maxItems is not None else 5

            output = []
            for _ in range(random.randint(min_items, max_items)):
                output.append(self.items.generate(context))
                context["state"]["__depth__"] = depth
            if self.uniqueItems and self.items.type == "object":
                output = [dict(s) for s in {frozenset(d.items()) for d in output}]
                while len(output) < min_items:
                    output.append(self.items.generate(context))
                    output = [dict(s) for s in {frozenset(d.items()) for d in output}]
                    context["state"]["__depth__"] = depth
            elif self.uniqueItems:
                output = set(output)
                while len(output) < min_items:
                    output.add(self.items.generate(context))
                    context["state"]["__depth__"] = depth
                output = list(output)
            return output

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        if self.items is None:
            _type = List[Any]
        else:
            _type = eval(
                f"List[Union[{','.join([self.items.model(context)[0].__name__])}]]",
                context["__internal__"],
            )
        return self.to_pydantic(context, _type)
