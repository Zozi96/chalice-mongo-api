from decouple import config


DEBUG: bool = config('DEBUG', default=False, cast=bool)

APP_CONFIG: dict = {
    'app_name': 'code',
    'debug': DEBUG
}
