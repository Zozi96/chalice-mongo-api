from chalice import Chalice

from core.settings import APP_CONFIG
from core.blueprints.users import blueprint as users_blueprint

app = Chalice(**APP_CONFIG)
app.register_blueprint(users_blueprint, url_prefix='/users')


@app.route('/')
def index():
    return {'hello': 'world!'}
