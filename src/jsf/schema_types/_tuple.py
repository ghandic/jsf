from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field

from .base import BaseSchema, ProviderNotSetException


class JSFTuple(BaseSchema):
    items: Optional[List[BaseSchema]] = None
    additionalItems: Optional[Union[bool, BaseSchema]] = None  # TODO: Random additional items to be appended
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False
    fixed: Optional[Union[int, str]] = Field(None, alias="$fixed")

    def from_dict(d):
        return JSFTuple(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[List[Tuple]]:
        # TODO:  Random drop out "It’s ok to not provide all of the items"
        try:
            return super().generate(context)
        except ProviderNotSetException:
            return tuple([item.generate(context) for item in self.items])

    def model(self, context: Dict[str, Any]):
        _type = eval(
            f"conlist(Union[{','.join([item.model(context)[0].__name__ for item in self.items])}], min_items={len(self.items)}, max_items={len(self.items)})",
            context["__internal__"],
        )
        return self.to_pydantic(context, _type)
