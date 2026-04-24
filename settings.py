# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python-demo-site',
        'USER': 'root',
        'PASSWORD': 'rakics98',
        'HOST': 'localhost',      # Or your database IP address
        'PORT': '3306',           # Default MySQL port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}