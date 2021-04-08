import random
from datetime import datetime
from typing import Optional, Any, List, Dict, Any
from dataclasses import dataclass, field

from dataclasses_json import config, dataclass_json
from faker import Faker

faker = Faker()


class ProviderNotSetException(Exception):
    ...


@dataclass_json
@dataclass
class BaseSchema:
    # The type keyword is fundamental to JSON Schema. It specifies the data type for a schema.
    type: Optional[str] = None
    # The title and description keywords must be strings. A “title” will preferably be short, whereas a “description” will provide a more lengthy explanation about the purpose of the data described by the schema.
    title: Optional[str] = None
    description: Optional[str] = None
    # The default keyword specifies a default value for an item. JSON processing tools may use this information to provide a default value for a missing key/value pair, though many JSON schema validators simply ignore the default keyword. It should validate against the schema in which it resides, but that isn’t required.
    default: Optional[Any] = None
    # The examples keyword is a place to provide an array of examples that validate against the schema. This isn’t used for validation, but may help with explaining the effect and purpose of the schema to a reader. Each entry should validate against the schema in which is resides, but that isn’t strictly required. There is no need to duplicate the default value in the examples array, since default will be treated as another example.
    examples: Optional[List[Any]] = None
    # The $schema keyword is used to declare that a JSON fragment is actually a piece of JSON Schema. It also declares which version of the JSON Schema standard that the schema was written against.
    schema: Optional[str] = field(default=None, metadata=config(field_name="$schema"))
    # The $comment keyword is strictly intended for adding comments to the JSON schema source. Its value must always be a string. Unlike the annotations title, description and examples, JSON schema implementations aren’t allowed to attach any meaning or behavior to it whatsoever, and may even strip them at any time. Therefore, they are useful for leaving notes to future editors of a JSON schema, (which is quite likely your future self), but should not be used to communicate to users of the schema.
    comments: Optional[str] = field(default=None, metadata=config(field_name="$comment"))

    # JSF Custom fields
    path: Optional[str] = None
    name: Optional[str] = None
    provider: Optional[str] = field(default=None, metadata=config(field_name="$provider"))
    set_state: Optional[str] = field(default=None, metadata=config(field_name="$state"))
    is_nullable: bool = False

    def generate(self, state: Dict[str, Any]) -> Any:
        eval_globals = {"state": state, "faker": faker, "random": random, "datetime": datetime}
        if self.set_state is not None:
            state[self.path] = {k: eval(v, eval_globals)() for k, v in self.set_state.items()}

        if self.is_nullable and random.uniform(0, 1) < 0.9:
            return None
        if self.provider is not None:
            return eval(self.provider, eval_globals)()
        raise ProviderNotSetException()

