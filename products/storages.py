from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage

PROTECTED_MEDIA = getattr(settings, 'PROTECTED_MEDIA', None)
if PROTECTED_MEDIA is None:
    raise ImproperlyConfigured('PROTECTED_MEDIA is not set in settings.py')


# django-storages
class ProtectedStorage(FileSystemStorage):
    location = PROTECTED_MEDIA  # default one is MEDIA_ROOT
