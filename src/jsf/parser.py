from copy import deepcopy
from typing import Dict, Optional, Any, Tuple as TupleType
from itertools import count
import json

from smart_open import open as s_open
from jsonschema import validate

from .schema_types import Object, Array, Primitives, Tuple, Enum, PrimativeTypes, AllTypes


class JSF:
    def __init__(self, schema: Dict[str, Any]):
        self.root_schema = schema
        self.definitions = {}
        self.base_state = {"__counter__": count(start=1), "__all_json_paths__": []}
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

    def __parse_tuple(self, name: str, path: str, schema: Dict[str, Any]) -> Tuple:
        _, is_nullable = self.__is_field_nullable(schema)
        arr = Tuple.from_dict({"name": name, "path": path, "is_nullable": is_nullable, **schema})
        arr.items = []
        for i, item in enumerate(schema["items"]):
            arr.items.append(self.__parse_definition(name, path=f"{name}[{i}]", schema=item))
        return arr

    def __is_field_nullable(self, schema: Dict[str, Any]) -> TupleType[str, bool]:
        item_type = schema.get("type")
        if isinstance(item_type, list):
            if "null" in item_type and len(set(item_type)) == 2:
                deepcopy(item_type).remove("null")
                return item_type[0], True
            raise TypeError
        return item_type, False

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
            return Enum.from_dict({"name": name, "path": path, "is_nullable": is_nullable, **schema})
        elif "type" in schema:
            if item_type == "object" and "properties" in schema:
                return self.__parse_object(name, path, schema)
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
        else:
            raise ValueError(f"Cannot parse schema {repr(schema)}")

    def _parse(self, schema: Dict[str, Any]) -> AllTypes:
        for name, definition in schema.get("definitions", {}).items():
            item = self.__parse_definition(name, path="#/definitions", schema=definition)
            self.definitions[f"#/definitions/{name}"] = item

        self.root = self.__parse_definition(name="root", path="#", schema=schema)

    def generate(self, n: Optional[int] = None) -> Any:
        if n is None or n == 1:
            return self.root.generate(state=self.base_state)
        return [self.root.generate(state=deepcopy(self.base_state)) for _ in range(n)]

    def generate_and_validate(self) -> None:
        fake = self.root.generate(state=self.base_state)
        validate(instance=fake, schema=self.root_schema)

    def to_json(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.generate(), f, indent=2)

    @staticmethod
    def from_json(path: str) -> "JSF":
        with open(path, "r") as f:
            return JSF(json.load(f))

