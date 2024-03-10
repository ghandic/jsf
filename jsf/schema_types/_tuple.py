from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import Field

from jsf.schema_types.base import BaseSchema, ProviderNotSetException


class JSFTuple(BaseSchema):
    items: Optional[List[BaseSchema]] = None
    additionalItems: Optional[
        Union[bool, BaseSchema]
    ] = None  # TODO: Random additional items to be appended
    minItems: Optional[int] = 0
    maxItems: Optional[int] = 5
    uniqueItems: Optional[bool] = False
    fixed: Optional[Union[int, str]] = Field(None, alias="$fixed")

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "JSFTuple":
        return JSFTuple(**d)

    def generate(self, context: Dict[str, Any]) -> Optional[List[Tuple]]:
        # TODO:  Random drop out "It's ok to not provide all of the items"
        try:
            return super().generate(context)
        except ProviderNotSetException:
            depth = context["state"]["__depth__"]
            output = []
            for item in self.items:
                output.append(item.generate(context))
                context["state"]["__depth__"] = depth
            return tuple(output)

    def model(self, context: Dict[str, Any]) -> Tuple[Type, Any]:
        _type = eval(
            f"Tuple[{','.join([item.model(context)[0].__name__ for item in self.items])}]",
            context["__internal__"],
        )
        return self.to_pydantic(context, _type)
