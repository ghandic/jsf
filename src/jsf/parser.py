import json
import logging
import random
from copy import deepcopy
from datetime import datetime
from itertools import count
from typing import Any, Dict, List, Optional, Tuple, Union

from faker import Faker
from jsonschema import validate
from pydantic import conlist
from smart_open import open as s_open

from .schema_types import AllTypes, Array, JSFEnum, JSFTuple, Object, PrimativeTypes, Primitives, AnyOf, OneOf

logger = logging.getLogger()
faker = Faker()


class JSF:
    def __init__(
        self,
        schema: Dict[str, Any],
        context: Dict[str, Any] = {
            "faker": faker,
            "random": random,
            "datetime": datetime,
            "__internal__": {"List": List, "Union": Union, "conlist": conlist},
        },
        initial_state: Dict[str, Any] = {},
    ):
        self.root_schema = schema
        self.definitions = {}
        self.base_state = {
            "__counter__": count(start=1),
            "__all_json_paths__": [],
            **initial_state,
        }
        self.base_context = context

        self.root = None
        self._parse(schema)

    def __parse_primitive(self, name: str, path: str, schema: Dict[str, Any]) -> PrimativeTypes:
        item_type, is_nullable = self.__is_field_nullable(schema)
        cls = Primitives.get(item_type)
        return cls.from_dict({"name": name, "path": path, "is_nullable": is_nullable, **schema})

    def __parse_object(self, name: str, path: str, schema: Dict[str, Any]) -> Object:
        _, is_nullable = self.__is_field_nullable(schema)
        model = Object.from_dict({"name": name, "path": path, "is_nullable": is_nullable, **schema})
        props = []
        for _name, definition in schema.get("properties", {}).items():
            props.append(self.__parse_definition(_name, path=f"{path}/{_name}", schema=definition))
        model.properties = props
        return model

    def __parse_array(self, name: str, path: str, schema: Dict[str, Any]) -> Array:
        _, is_nullable = self.__is_field_nullable(schema)
        arr = Array.from_dict({"name": name, "path": path, "is_nullable": is_nullable, **schema})
        arr.items = self.__parse_definition(name, name, schema["items"])
        return arr

    def __parse_tuple(self, name: str, path: str, schema: Dict[str, Any]) -> JSFTuple:
        _, is_nullable = self.__is_field_nullable(schema)
        arr = JSFTuple.from_dict({"name": name, "path": path, "is_nullable": is_nullable, **schema})
        arr.items = []
        for i, item in enumerate(schema["items"]):
            arr.items.append(self.__parse_definition(name, path=f"{name}[{i}]", schema=item))
        return arr

    def __is_field_nullable(self, schema: Dict[str, Any]) -> Tuple[str, bool]:
        item_type = schema.get("type")
        if isinstance(item_type, list):
            if "null" in item_type and len(set(item_type)) >= 2:
                item_type_deep_copy = deepcopy(item_type)
                item_type_deep_copy.remove("null")
                return random.choice(item_type_deep_copy), True
            raise TypeError  # pragma: no cover - not currently supporting other types TODO
        return item_type, False

    def __parse_anyOf(self, name: str, path: str, schema: Dict[str, Any]) -> AnyOf:
        schemas = []
        for d in schema["anyOf"]:
            schemas.append(self.__parse_definition(name, path, d))
        return AnyOf(name=name, path=path, schemas=schemas, **schema)

    def __parse_oneOf(self, name: str, path: str, schema: Dict[str, Any]) -> OneOf:
        schemas = []
        for d in schema["oneOf"]:
            schemas.append(self.__parse_definition(name, path, d))
        return OneOf(name=name, path=path, schemas=schemas, **schema)

    def __parse_definition(self, name: str, path: str, schema: Dict[str, Any]) -> AllTypes:
        self.base_state["__all_json_paths__"].append(path)
        item_type, is_nullable = self.__is_field_nullable(schema)
        if "const" in schema:
            schema["enum"] = [schema["const"]]

        if "enum" in schema:
            enum_list = schema["enum"]
            assert len(enum_list) > 0, "Enum List is Empty"
            assert all(
                isinstance(item, (int, float, str, type(None))) for item in enum_list
            ), "Enum Type is not null, int, float or string"
            return JSFEnum.from_dict({"name": name, "path": path, "is_nullable": is_nullable, **schema})
        elif "type" in schema:
            if item_type == "object" and "properties" in schema:
                return self.__parse_object(name, path, schema)
            elif item_type == "object" and "anyOf" in schema:
                return self.__parse_anyOf(name, path, schema)
            elif item_type == "object" and "oneOf" in schema:
                return self.__parse_oneOf(name, path, schema)
            elif item_type == "array":
                if (schema.get("contains") is not None) or isinstance(schema.get("items"), dict):
                    return self.__parse_array(name, path, schema)
                if isinstance(schema.get("items"), list) and all(isinstance(x, dict) for x in schema.get("items", [])):
                    return self.__parse_tuple(name, path, schema)
            else:
                return self.__parse_primitive(name, path, schema)
        elif "$ref" in schema:
            ext, frag = schema["$ref"].split("#")
            if ext == "":
                cls = deepcopy(self.definitions.get(f"#{frag}"))
            else:
                with s_open(ext, "r") as f:
                    external_jsf = JSF(json.load(f))
                cls = deepcopy(external_jsf.definitions.get(f"#{frag}"))
            cls.name = name
            cls.path = path
            return cls
        elif "anyOf" in schema:
            return self.__parse_anyOf(name, path, schema)
        elif "oneOf" in schema:
            return self.__parse_oneOf(name, path, schema)
        else:
            raise ValueError(f"Cannot parse schema {repr(schema)}")  # pragma: no cover

    def _parse(self, schema: Dict[str, Any]) -> AllTypes:
        for def_tag in ("definitions", "$defs"):
            for name, definition in schema.get(def_tag, {}).items():
                item = self.__parse_definition(name, path=f"#/{def_tag}", schema=definition)
                self.definitions[f"#/{def_tag}/{name}"] = item

        self.root = self.__parse_definition(name="root", path="#", schema=schema)

    @property
    def context(self):
        return {**self.base_context, "state": deepcopy(self.base_state)}

    def generate(self, n: Optional[int] = None) -> Any:
        if n is None or n == 1:
            return self.root.generate(context=self.context)
        return [self.root.generate(context=self.context) for _ in range(n)]

    def pydantic(self):
        return self.root.model(context=self.context)[0]

    def generate_and_validate(self) -> None:
        fake = self.root.generate(context=self.context)
        validate(instance=fake, schema=self.root_schema)

    def to_json(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.generate(), f, indent=2)

    @staticmethod
    def from_json(path: str) -> "JSF":
        with open(path, "r") as f:
            return JSF(json.load(f))
