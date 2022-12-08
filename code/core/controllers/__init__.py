from dataclasses import dataclass, field

from typing import Optional, Dict, Text, Type

from chalice import BadRequestError

from core import HTTPMethod
from core.schemas import MongoBaseSchema


@dataclass
class BaseController:
    body_dict: Optional[Dict]
    schema_class: Type[MongoBaseSchema]
    id_field: Optional[Text] = field(default=None)
    http_method: Text = field(default=HTTPMethod.GET.value)

    def _validate_data(self) -> None:
        errors = self.schema_class().validate(self.body_dict)
        if errors:
            raise BadRequestError(errors)
