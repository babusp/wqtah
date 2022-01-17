"""
 Custom routers for job sourcing .
"""
# third party imports
from rest_framework.routers import DefaultRouter


class OptionalSlashRouter(DefaultRouter):
    """
    optional slash router class
    """
    def __init__(self):
        """
            explicitly appending '/' in urls if '/' doesn't exist for making common url patterns .
        """
        super(OptionalSlashRouter, self).__init__()
        self.trailing_slash = '/?'
