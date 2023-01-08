from jsf.schema_types.string_utils.content_type.application__gzip import create_random_gzip
from jsf.schema_types.string_utils.content_type.application__jwt import create_random_jwt
from jsf.schema_types.string_utils.content_type.application__zip import create_random_zip
from jsf.schema_types.string_utils.content_type.image__jpeg import random_jpg
from jsf.schema_types.string_utils.content_type.image__webp import random_webp
from jsf.schema_types.string_utils.content_type.text__plain import random_fixed_length_sentence


def not_implemented(*args, **kwargs):
    raise NotImplementedError()


ContentTypeGenerator = {
    "application/jwt": create_random_jwt,
    # "text/html": not_implemented,
    # "application/xml": not_implemented, # To implement: Port code from https://onlinerandomtools.com/generate-random-xml
    # "image/bmp": not_implemented, # To implement: request jpg and convert to bmp
    # "text/css": not_implemented,
    # "text/csv": not_implemented,
    # "image/gif": not_implemented, # To implement: request jpg and convert to gif
    "image/jpeg": random_jpg,
    # "application/json": not_implemented, # To implement: Port code from https://onlinerandomtools.com/generate-random-xml
    # "text/javascript": not_implemented,
    # "image/png": not_implemented, # To implement: request jpg and convert to png
    # "image/tiff": not_implemented, # To implement: request jpg and convert to tiff
    "text/plain": random_fixed_length_sentence,
    "image/webp": random_webp,
    "application/zip": create_random_zip,
    "application/gzip": create_random_gzip,
    # "application/x-bzip": not_implemented,  # To implement: create in memory random files using text/plain then zip
    # "application/x-bzip2": not_implemented,  # To implement: create in memory random files using text/plain then zip
    # "application/pdf": not_implemented, # To implement: request jpg and convert to pdf and/or make pdf using python package
    # "text/calendar": not_implemented,
}


def generate(content_type: str, min_length: int, max_length: int) -> str:
    return ContentTypeGenerator.get(content_type, not_implemented)(min_length, max_length)
