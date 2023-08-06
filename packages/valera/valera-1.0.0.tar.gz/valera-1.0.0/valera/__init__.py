from typing import Any

from district42 import GenericSchema

from ._validation_result import ValidationResult
from ._validator import Validator
from ._version import version

__version__ = version
__all__ = ("validate", "Validator", "ValidationResult",)


_validator = Validator()


def validate(schema: GenericSchema, value: Any, **kwargs: Any) -> ValidationResult:
    return schema.__accept__(_validator, value=value, **kwargs)
