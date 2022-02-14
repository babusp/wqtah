"""
Storage strategies.
"""
# third party imports
from storages.backends.azure_storage import AzureStorage
from django.conf import settings


class CustomFileStorage(AzureStorage):
    """
    Custom storage for s3
    """
    account_name = settings.AZURE_STORAGE_NAME
    account_key = settings.AZURE_STORAGE_KEY
    azure_container = settings.AZURE_STORAGE_CONTAINER
    expiration_secs = None
