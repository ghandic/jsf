import random

import requests  # pants: no-infer-dep

from jsf.schema_types.string_utils.content_encoding import bytes_str_repr


def random_webp(*args, **kwargs) -> str:
    return bytes_str_repr(
        requests.get(
            f"https://picsum.photos/{random.randint(1,50)*10}/{random.randint(1,50)*10}.webp"
        ).content
    )
