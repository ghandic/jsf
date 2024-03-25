import json
import logging
import random
from collections import ChainMap
from copy import deepcopy
from datetime import datetime
from itertools import count
from pathlib import Path
from types import MappingProxyType
from typing import Any, Dict, List, Optional, Tuple, Union

from faker import Faker
from jsonschema import validate
from pydantic import confloat
from smart_open import open as s_open

from jsf.schema_types import (
    AllOf,
    AllTypes,
    AnyOf,
    Array,
    JSFEnum,
    JSFTuple,
    Object,
    OneOf,
    Primitives,
    PrimitiveTypes,
)

logger = logging.getLogger()
faker = Faker()


class JSF:
    """The JSF class generates fake data based on a provided JSON Schema.

    Attributes:
        root_schema (Dict[str, Any]): The JSON schema based on which the fake data is generated.
        definitions (Dict): A dictionary to store definitions used in the JSON schema.
        base_state (Dict[str, Any]): A dictionary that represents the state of the parser. It includes a counter, a list of all JSON paths, and the provided initial state.
    """

    def __init__(
        self,
        schema: Dict[str, Any],
        context: Dict[str, Any] = MappingProxyType(
            {
                "faker": faker,
                "random": random,
                "datetime": datetime,
                "__internal__": {"List": List, "Union": Union, "Tuple": Tuple},
            }
        ),
        initial_state: Dict[str, Any] = MappingProxyType({}),
        allow_none_optionals: confloat(ge=0.0, le=1.0) = 0.5,
        max_recursive_depth: int = 10,
    ):
        """Initializes the JSF generator with the provided schema and
        configuration options.

        Args:
            schema (Dict[str, Any]): The JSON schema based on which the fake data is generated.
            context (Dict[str, Any], optional): A dictionary that provides additional utilities for handling the schema, such as a faker for generating fake data, a random number generator, and datetime utilities. It also includes an internal dictionary for handling List, Union, and Tuple types. Defaults to a dictionary with "faker", "random", "datetime", and "__internal__" keys.
            initial_state (Dict[str, Any], optional): A dictionary that represents the initial state of the parser. If you wish to extend the state so it can be accesses by your schema you can add any references in here. Defaults to an empty dictionary.
            allow_none_optionals (confloat, optional): A parameter that determines the probability of optional fields being set to None. Defaults to 0.5.
            max_recursive_depth (int, optional): A parameter that determines the maximum depth when generating a recursive schema. Defaults to 10.
        """
        self.root_schema = schema
        self.definitions = {}
        self.base_state = {
            "__counter__": count(start=1),
            "__all_json_paths__": [],
            "__depth__": 0,
            **initial_state,
        }
        self.base_context = context
        self.allow_none_optionals = allow_none_optionals
        self.max_recursive_depth = max_recursive_depth

        self.root = None
        self._parse(schema)

    @staticmethod
    def from_json(
        path: Path,
        context: Dict[str, Any] = MappingProxyType(
            {
                "faker": faker,
                "random": random,
                "datetime": datetime,
                "__internal__": {"List": List, "Union": Union, "Tuple": Tuple},
            }
        ),
        initial_state: Dict[str, Any] = MappingProxyType({}),
        allow_none_optionals: confloat(ge=0.0, le=1.0) = 0.5,
        max_recursive_depth: int = 10,
    ) -> "JSF":
        """Initializes the JSF generator with the provided schema at the given
        path and configuration options.

        Args:
            path (Path): The path to the JSON schema based on which the fake data is generated.
            context (Dict[str, Any], optional): A dictionary that provides additional utilities for handling the schema, such as a faker for generating fake data, a random number generator, and datetime utilities. It also includes an internal dictionary for handling List, Union, and Tuple types. Defaults to a dictionary with "faker", "random", "datetime", and "__internal__" keys.
            initial_state (Dict[str, Any], optional): A dictionary that represents the initial state of the parser. If you wish to extend the state so it can be accesses by your schema you can add any references in here. Defaults to an empty dictionary.
            allow_none_optionals (confloat, optional): A parameter that determines the probability of optional fields being set to None. Defaults to 0.5.
            max_recursive_depth (int, optional): A parameter that determines the maximum depth when generating a recursive schema. Defaults to 10.
        """
        with open(path) as f:
            return JSF(
                json.load(f), context, initial_state, allow_none_optionals, max_recursive_depth
            )

    def __parse_primitive(self, name: str, path: str, schema: Dict[str, Any]) -> PrimitiveTypes:
        item_type, is_nullable = self.__is_field_nullable(schema)
        cls = Primitives.get(item_type)
        return cls.from_dict(
            {
                "name": name,
                "path": path,
                "is_nullable": is_nullable,
                "allow_none_optionals": self.allow_none_optionals,
                "max_recursive_depth": self.max_recursive_depth,
                **schema,
            }
        )

    def __parse_object(
        self, name: str, path: str, schema: Dict[str, Any], root: Optional[AllTypes] = None
    ) -> Object:
        _, is_nullable = self.__is_field_nullable(schema)
        model = Object.from_dict(
            {
                "name": name,
                "path": path,
                "is_nullable": is_nullable,
                "allow_none_optionals": self.allow_none_optionals,
                "max_recursive_depth": self.max_recursive_depth,
                **schema,
            }
        )
        root = model if root is None else root
        props = []
        for _name, definition in schema.get("properties", {}).items():
            props.append(
                self.__parse_definition(_name, path=f"{path}/{_name}", schema=definition, root=root)
            )
        model.properties = props
        pattern_props = []
        for _name, definition in schema.get("patternProperties", {}).items():
            pattern_props.append(
                self.__parse_definition(_name, path=f"{path}/{_name}", schema=definition, root=root)
            )
        model.patternProperties = pattern_props

        return model

    def __parse_array(
        self, name: str, path: str, schema: Dict[str, Any], root: Optional[AllTypes] = None
    ) -> Array:
        _, is_nullable = self.__is_field_nullable(schema)
        arr = Array.from_dict(
            {
                "name": name,
                "path": path,
                "is_nullable": is_nullable,
                "allow_none_optionals": self.allow_none_optionals,
                "max_recursive_depth": self.max_recursive_depth,
                **schema,
            }
        )
        root = arr if root is None else root
        arr.items = self.__parse_definition(name, f"{path}/items", schema["items"], root=root)
        return arr

    def __parse_tuple(
        self, name: str, path: str, schema: Dict[str, Any], root: Optional[AllTypes] = None
    ) -> JSFTuple:
        _, is_nullable = self.__is_field_nullable(schema)
        arr = JSFTuple.from_dict(
            {
                "name": name,
                "path": path,
                "is_nullable": is_nullable,
                "allow_none_optionals": self.allow_none_optionals,
                "max_recursive_depth": self.max_recursive_depth,
                **schema,
            }
        )
        root = arr if root is None else root
        arr.items = []
        for i, item in enumerate(schema["items"]):
            arr.items.append(
                self.__parse_definition(name, path=f"{path}/{name}[{i}]", schema=item, root=root)
            )
        return arr

    def __is_field_nullable(self, schema: Dict[str, Any]) -> Tuple[str, bool]:
        item_type = schema.get("type")
        if isinstance(item_type, list):
            if "null" in item_type and len(set(item_type)) >= 2:
                item_type_deep_copy = deepcopy(item_type)
                item_type_deep_copy.remove("null")
                return random.choice(item_type_deep_copy), True
            if len(set(item_type)) >= 1:
                item_type_deep_copy = deepcopy(item_type)
                return random.choice(item_type_deep_copy), False
        return item_type, False

    def __parse_anyOf(
        self, name: str, path: str, schema: Dict[str, Any], root: Optional[AllTypes] = None
    ) -> AnyOf:
        model = AnyOf(name=name, path=path, max_recursive_depth=self.max_recursive_depth, **schema)
        root = model if root is None else root
        schemas = []
        for d in schema["anyOf"]:
            schemas.append(self.__parse_definition(name, path, d, root=root))
        model.schemas = schemas
        return model

    def __parse_allOf(
        self, name: str, path: str, schema: Dict[str, Any], root: Optional[AllTypes] = None
    ) -> AllOf:
        combined_schema = dict(ChainMap(*schema["allOf"]))
        model = AllOf(name=name, path=path, max_recursive_depth=self.max_recursive_depth, **schema)
        root = model if root is None else root
        model.combined_schema = self.__parse_definition(name, path, combined_schema, root=root)
        return model

    def __parse_oneOf(
        self, name: str, path: str, schema: Dict[str, Any], root: Optional[AllTypes] = None
    ) -> OneOf:
        model = OneOf(name=name, path=path, max_recursive_depth=self.max_recursive_depth, **schema)
        root = model if root is None else root
        schemas = []
        for d in schema["oneOf"]:
            schemas.append(self.__parse_definition(name, path, d, root=root))
        model.schemas = schemas
        return model

    def __parse_named_definition(self, path: str, def_name: str, root) -> AllTypes:
        schema = self.root_schema
        parsed_definition = None
        for def_tag in ("definitions", "$defs"):
            if path.startswith(f"#/{def_tag}/{def_name}"):
                root.is_recursive = True
                return root
            definition = schema.get(def_tag, {}).get(def_name)
            if definition is not None:
                parsed_definition = self.__parse_definition(
                    def_name, path=f"{path}/#/{def_tag}/{def_name}", schema=definition, root=root
                )
                self.definitions[f"#/{def_tag}/{def_name}"] = parsed_definition
        return parsed_definition

    def __parse_definition(
        self, name: str, path: str, schema: Dict[str, Any], root: Optional[AllTypes] = None
    ) -> AllTypes:
        self.base_state["__all_json_paths__"].append(path)
        item_type, is_nullable = self.__is_field_nullable(schema)
        if "const" in schema:
            schema["enum"] = [schema["const"]]

        if "enum" in schema:
            enum_list = schema["enum"]
            assert len(enum_list) > 0, "Enum List is Empty"
            assert all(
                isinstance(item, (int, float, str, dict, type(None))) for item in enum_list
            ), "Enum Type is not null, int, float, string or dict"
            return JSFEnum.from_dict(
                {
                    "name": name,
                    "path": path,
                    "is_nullable": is_nullable,
                    "allow_none_optionals": self.allow_none_optionals,
                    "max_recursive_depth": self.max_recursive_depth,
                    **schema,
                }
            )
        elif "type" in schema:
            if item_type == "object" and "properties" in schema:
                return self.__parse_object(name, path, schema, root)
            elif item_type == "object" and "anyOf" in schema:
                return self.__parse_anyOf(name, path, schema, root)
            elif item_type == "object" and "allOf" in schema:
                return self.__parse_allOf(name, path, schema, root)
            elif item_type == "object" and "oneOf" in schema:
                return self.__parse_oneOf(name, path, schema, root)
            elif item_type == "array":
                if (schema.get("contains") is not None) or isinstance(schema.get("items"), dict):
                    return self.__parse_array(name, path, schema, root)
                if isinstance(schema.get("items"), list) and all(
                    isinstance(x, dict) for x in schema.get("items", [])
                ):
                    return self.__parse_tuple(name, path, schema, root)
            else:
                return self.__parse_primitive(name, path, schema)
        elif "$ref" in schema:
            ext, frag = schema["$ref"].split("#")
            if ext == "":
                if f"#{frag}" in self.definitions:
                    cls = deepcopy(self.definitions.get(f"#{frag}"))
                else:
                    # parse referenced definition
                    ref_name = frag.split("/")[-1]
                    cls = self.__parse_named_definition(path, ref_name, root)
            else:
                with s_open(ext, "r") as f:
                    external_jsf = JSF(json.load(f))
                cls = deepcopy(external_jsf.definitions.get(f"#{frag}"))
            if path != "#" and cls == root:
                cls.name = name
            elif path != "#":
                cls.name = name
                cls.path = path
            return cls
        elif "anyOf" in schema:
            return self.__parse_anyOf(name, path, schema, root)
        elif "allOf" in schema:
            return self.__parse_allOf(name, path, schema, root)
        elif "oneOf" in schema:
            return self.__parse_oneOf(name, path, schema, root)
        elif not any(key in schema for key in ["not", "if", "then", "else"]):
            return self.__parse_primitive(name, path, {**schema, "type": list(Primitives.keys())})
        else:
            raise ValueError(f"Cannot parse schema {repr(schema)}")  # pragma: no cover

    def _parse(self, schema: Dict[str, Any]) -> AllTypes:
        for def_tag in ("definitions", "$defs"):
            for name, definition in schema.get(def_tag, {}).items():
                if f"#/{def_tag}/{name}" not in self.definitions:
                    item = self.__parse_definition(
                        name, path=f"#/{def_tag}/{name}", schema=definition
                    )
                    self.definitions[f"#/{def_tag}/{name}"] = item

        self.root = self.__parse_definition(name="root", path="#", schema=schema)

    @property
    def context(self):
        return {**self.base_context, "state": deepcopy(self.base_state)}

    def generate(
        self, n: Optional[int] = None, *, use_defaults: bool = False, use_examples: bool = False
    ) -> Any:
        """Generates a fake object from the provided schema, and returns the
        output.

        Args:
            n (int, optional): If n is provided, it returns a list of n objects. If n is 1 then it returns a single object.
            use_defaults (bool, optional): prefer the default value as defined in the schema over a randomly generated object. Defaults to False.
            use_examples (bool, optional): prefer an example as defined in the schema over a randomly generated object. This parameter is preceded by the `use_defaults` parameter if set. Defaults to False.
        """
        context = {**self.context, "use_defaults": use_defaults, "use_examples": use_examples}
        if n is None or n == 1:
            return self.root.generate(context=context)
        return [self.root.generate(context=context) for _ in range(n)]

    def pydantic(self):
        """Generates a fake object from the provided schema and provides the
        output as a Pydantic model."""
        return self.root.model(context=self.context)[0]

    def generate_and_validate(self) -> None:
        """Generates a fake object from the provided schema and performs
        validation on the result."""
        fake = self.root.generate(context=self.context)
        validate(instance=fake, schema=self.root_schema)

    def to_json(self, path: Path, **kwargs) -> None:
        """Generates a fake object from the provided schema and saves the
        output to the given path."""
        with open(path, "w") as f:
            json.dump(self.generate(), f, **kwargs)
