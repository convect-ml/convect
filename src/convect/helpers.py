import codecs
import dill
import sys
from typing import Union, List, Tuple

def is_iterable(value: Union[str, list, tuple]) -> bool:
    return isinstance(value, List) or isinstance(value, Tuple)


def list_large_vars(pickled_session: str) -> List[str]:
    session = dill.loads(
        codecs.decode(
            pickled_session.encode(), "base64_codec"
        )
    )
    large_vars = []
    for var_name in dir(session):
        session_var = getattr(session, var_name)
        if hasattr(session_var, '__module__') and session_var.__module__.startswith('IPython.core'):
            continue
        size_in_bytes = sys.getsizeof(dill.dumps(session_var))
        if size_in_bytes > 500000:
            print(f'"{var_name}" is {size_in_bytes} bytes in size')
            large_vars.append(var_name)
    return large_vars


def exclude_ignores_and_redump(pickled_session: str, ignore: Union[Tuple[str], List[str]]) -> str:
    assert is_iterable(ignore)
    session = dill.loads(
        codecs.decode(
            pickled_session.encode(), "base64_codec"
        )
    )
    for ignorable in ignore:
        delattr(session, ignorable)
    return codecs.encode(
        dill.dumps(session), "base64_codec"
    ).decode()