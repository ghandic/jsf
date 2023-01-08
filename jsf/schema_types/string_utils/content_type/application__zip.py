import io
import random
import zipfile
from typing import Tuple

import rstr

from jsf.schema_types.string_utils.content_encoding import bytes_str_repr
from jsf.schema_types.string_utils.content_type.text__plain import random_fixed_length_sentence


def create_random_file_name() -> str:
    return rstr.xeger(r"[a-zA-Z0-9]+\.txt")


def create_random_file() -> Tuple[str, io.BytesIO]:
    return (create_random_file_name(), io.BytesIO(random_fixed_length_sentence().encode("utf-8")))


def create_random_zip(*args, **kwargs) -> str:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in [create_random_file() for _ in range(random.randint(1, 10))]:
            zip_file.writestr(file_name, data.getvalue())

    return bytes_str_repr(zip_buffer.getvalue())
