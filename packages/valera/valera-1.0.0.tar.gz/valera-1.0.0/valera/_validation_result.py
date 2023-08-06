from typing import List

from .errors import ValidationError

__all__ = ("ValidationResult",)


class ValidationResult:
    def __init__(self) -> None:
        self._errors: List[ValidationError] = []

    def add_error(self, error: ValidationError) -> "ValidationResult":
        self._errors.append(error)
        return self

    def add_errors(self, errors: List[ValidationError]) -> "ValidationResult":
        for error in errors:
            self._errors.append(error)
        return self

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def get_errors(self) -> List[ValidationError]:
        return self._errors
