from dataclasses import dataclass, field
from typing import Text, Any

from bson import ObjectId
from chalice import NotFoundError, Response


def get_object_id(object_id: Text) -> ObjectId:
    """Get object id from string."""

    if not ObjectId.is_valid(object_id):
        raise NotFoundError('Invalid ID')
    return ObjectId(object_id)


@dataclass
class StandardResponse:
    message: Text
    data: Any
    status_code: int = field(default=200)

    def __call__(self, *args, **kwargs) -> Response:
        return Response(
            body={'message': self.message, 'data': self.data},
            status_code=self.status_code,
        )
