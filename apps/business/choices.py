"""
choices file
"""
from apps.business import constants
from apps.utility.constants import IMAGE, VIDEO

LEVEL_CHOICES = (
    (constants.BUSINESS, "Add Business"),
    (constants.COMPANY_DETAIL, "Company Detail"),
    (constants.COMPLETED, "Profile Completed"),
)

MEDIA_TYPE = (
    (IMAGE, "image"),
    (VIDEO, "video"),
)
