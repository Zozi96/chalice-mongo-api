from decouple import config

AWS_ACCESS_KEY_ID: str = config('AWS_ACCESS_KEY_ID', default='', cast=str)
AWS_SECRET_ACCESS_KEY: str = config('AWS_SECRET_ACCESS_KEY', default='', cast=str)
REGION_NAME: str = config('REGION_NAME', default='', cast=str)
DEBUG: bool = config('DEBUG', default=False, cast=bool)

APP_CONFIG: dict = {
    'app_name': 'code',
    'debug': DEBUG
}
