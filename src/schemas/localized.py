from typing import Self

from pydantic import BaseModel, Field, ValidationInfo, model_validator


class Localized(BaseModel):
    translations: dict | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def localize(self, info: ValidationInfo) -> Self:
        """Replace fields with their translation for the locale passed in the validation context."""
        locale = (info.context or {}).get("locale")
        for field, value in (self.translations or {}).get(locale, {}).items():
            setattr(self, field, value)
        return self
