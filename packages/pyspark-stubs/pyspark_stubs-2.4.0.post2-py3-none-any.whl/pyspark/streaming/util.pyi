# Stubs for pyspark.streaming.util (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

class TransformFunction:
    ctx = ...  # type: Any
    func = ...  # type: Any
    deserializers = ...  # type: Any
    rdd_wrap_func = ...  # type: Any
    failure = ...  # type: Any
    def __init__(self, ctx, func, *deserializers) -> None: ...
    def rdd_wrapper(self, func): ...
    def call(self, milliseconds, jrdds): ...
    def getLastFailure(self): ...
    class Java:
        implements = ...  # type: Any

class TransformFunctionSerializer:
    ctx = ...  # type: Any
    serializer = ...  # type: Any
    gateway = ...  # type: Any
    failure = ...  # type: Any
    def __init__(self, ctx, serializer, gateway: Optional[Any] = ...) -> None: ...
    def dumps(self, id): ...
    def loads(self, data): ...
    def getLastFailure(self): ...
    class Java:
        implements = ...  # type: Any

def rddToFileName(prefix, suffix, timestamp): ...
