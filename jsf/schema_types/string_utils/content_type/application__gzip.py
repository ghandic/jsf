import gzip
import io

from jsf.schema_types.string_utils.content_encoding import bytes_str_repr
from jsf.schema_types.string_utils.content_type.application__zip import create_random_file_name
from jsf.schema_types.string_utils.content_type.text__plain import random_fixed_length_sentence


def create_random_gzip(*args, **kwargs) -> str:
    fgz = io.BytesIO()
    gzip_obj = gzip.GzipFile(filename=create_random_file_name(), mode="wb", fileobj=fgz)
    gzip_obj.write(random_fixed_length_sentence().encode("utf-8"))
    gzip_obj.close()

    fgz.seek(0)
    return bytes_str_repr(fgz.getvalue())
