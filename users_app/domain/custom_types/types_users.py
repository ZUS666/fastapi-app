from typing import Any

from pydantic_core import CoreSchema, core_schema
from pydantic import GetCoreSchemaHandler


class UIDType(int):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(int))
