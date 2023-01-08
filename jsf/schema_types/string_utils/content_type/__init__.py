from jsf.schema_types.string_utils.content_type.application__jwt import create_random_jwt
from jsf.schema_types.string_utils.content_type.text__plain import random_fixed_length_sentence


def not_implemented(*args, **kwargs):
    raise NotImplementedError()


ContentTypeGenerator = {
    "application/jwt": create_random_jwt,
    # "text/html": not_implemented,
    # "application/xml": not_implemented,
    # "image/bmp": not_implemented,
    # "text/css": not_implemented,
    # "text/csv": not_implemented,
    # "image/gif": not_implemented,
    # "image/jpeg": not_implemented,
    # "application/json": not_implemented,
    # "text/javascript": not_implemented,
    # "image/png": not_implemented,
    # "image/tiff": not_implemented,
    "text/plain": random_fixed_length_sentence,
    # "image/webp": not_implemented,
    # "application/zip": not_implemented,
    # "application/pdf": not_implemented,
    # "text/calendar": not_implemented,
}

def generate(content_type: str, min_length:int, max_length:int) -> str:
    return ContentTypeGenerator.get(content_type, not_implemented)(min_length, max_length)