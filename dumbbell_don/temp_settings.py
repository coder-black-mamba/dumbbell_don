from .settings import *

# Override settings for testing
DEBUG = True

# Disable Cloudinary for testing
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Disable email sending
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Disable Cloudinary
CLOUDINARY_STORAGE = {}

# Disable SSL
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
