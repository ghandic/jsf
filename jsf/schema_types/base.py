import logging
import random
import uuid
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel, Field
from typing_extensions import Self

logger = logging.getLogger()


class ProviderNotSetException(Exception):
    ...


class BaseSchema(BaseModel):
    # The type keyword is fundamental to JSON Schema. It specifies the data type for a schema.
    type: Optional[Union[str, List[str]]] = None
    # The title and description keywords must be strings. A "title" will preferably be short, whereas a "description" will provide a more lengthy explanation about the purpose of the data described by the schema.
    title: Optional[str] = None
    description: Optional[str] = None
    # The default keyword specifies a default value for an item. JSON processing tools may use this information to provide a default value for a missing key/value pair, though many JSON schema validators simply ignore the default keyword. It should validate against the schema in which it resides, but that isn't required.
    default: Optional[Any] = None
    # The examples keyword is a place to provide an array of examples that validate against the schema. This isn't used for validation, but may help with explaining the effect and purpose of the schema to a reader. Each entry should validate against the schema in which is resides, but that isn't strictly required. There is no need to duplicate the default value in the examples array, since default will be treated as another example.
    examples: Optional[List[Any]] = None
    # The $schema keyword is used to declare that a JSON fragment is actually a piece of JSON Schema. It also declares which version of the JSON Schema standard that the schema was written against.
    schema_: Optional[str] = Field(None, alias="$schema")
    # The $comment keyword is strictly intended for adding comments to the JSON schema source. Its value must always be a string. Unlike the annotations title, description and examples, JSON schema implementations aren't allowed to attach any meaning or behavior to it whatsoever, and may even strip them at any time. Therefore, they are useful for leaving notes to future editors of a JSON schema, (which is quite likely your future self), but should not be used to communicate to users of the schema.
    comments: Optional[str] = Field(None, alias="$comments")

    # JSF Custom fields
    path: Optional[str] = None
    name: Optional[str] = None
    provider: Optional[str] = Field(None, alias="$provider")
    set_state: Optional[Dict[str, str]] = Field(None, alias="$state")
    is_nullable: bool = False
    is_recursive: bool = False
    allow_none_optionals: float = Field(0.5, ge=0.0, le=1.0)
    max_recursive_depth: int = 10

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Self:
        raise NotImplementedError  # pragma: no cover

    def generate(self, context: Dict[str, Any]) -> Any:
        if self.is_recursive:
            context["state"]["__depth__"] += 1

        if self.set_state is not None:
            context["state"][self.path] = {k: eval(v, context)() for k, v in self.set_state.items()}

        if self.is_nullable and (
            random.uniform(0, 1) < self.allow_none_optionals
            or context["state"]["__depth__"] > self.max_recursive_depth
        ):
            return None
        if self.provider is not None:
            return eval(self.provider, context)()

        if context.get("use_defaults", False) and self.default:
            return self.default

        if context.get("use_examples", False) and self.examples:
            return random.choice(self.examples)

        raise ProviderNotSetException()

    def model(self, context: Dict[str, Any]) -> Optional[Tuple[Type, Field]]:
        raise NotImplementedError  # pragma: no cover

    def _get_unique_name(self, context: Dict[str, Any]) -> str:
        if context["__internal__"].get(self.name.capitalize()) is None:
            return self.name.capitalize()
        return self.name.capitalize() + str(uuid.uuid4().hex)

    def to_pydantic(self, context: Dict[str, Any], _type: Type) -> Tuple[Type, Field]:
        example = self.generate(context)
        if self.is_nullable:
            return (
                Optional[_type],
                Field(..., description=self.description, example=example),
            )
        return _type, Field(..., description=self.description, example=example)
