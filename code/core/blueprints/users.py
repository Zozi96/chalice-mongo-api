from chalice import Blueprint

from core.controllers.users import UserController, RetrieveUserController
from core.schemas.users import UserSchema

blueprint = Blueprint(__name__)


@blueprint.route('/', methods=('GET', 'POST'))
def list_create_users():
    return UserController(
        body_dict=blueprint.current_request.json_body,
        schema_class=UserSchema,
        http_method=blueprint.current_request.method,
    )()


@blueprint.route('/{user_id}', methods=('GET', 'PUT', 'DELETE'))
def retrieve_user(user_id: str):
    return RetrieveUserController(
        body_dict=blueprint.current_request.json_body,
        id_field=user_id,
        schema_class=UserSchema,
        http_method=blueprint.current_request.method
    )()
