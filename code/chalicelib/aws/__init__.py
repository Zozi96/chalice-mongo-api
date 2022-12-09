from decouple import config

AWS_ACCESS_KEY_ID: str = config('AWS_ACCESS_KEY_ID', default='', cast=str)
AWS_SECRET_ACCESS_KEY: str = config('AWS_SECRET_ACCESS_KEY', default='', cast=str)
AWS_DEFAULT_REGION: str = config('AWS_DEFAULT_REGION', default='', cast=str)
