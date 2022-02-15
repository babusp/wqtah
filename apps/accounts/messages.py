"""
accounts messages file
"""

SUCCESS_CODE = {
    "2000": "OK.",
    "2001": "User registered successfully.",
    "2002": "Reset password mail has been sent to your registered email.",
    "2003": "Password Reset Successfully.",
    "2004": "User logged-out successfully",
    "2005": "OTP send to your mobile number",
    "2006": "business deleted",
    "2007": "Profile updated successfully",
    "2008": "Service save successfully.",
    "2009": "Business added successfully.",
    "2010": "Business updated successfully.",
    "2011": "Business Attachment deleted successfully.",
    "2012": "Service Attachment deleted successfully."

}

ERROR_CODE = {
    "4001": "User with this phone number doesn't exists.",
    "4002": "Wrong password.",
    "4003": "Invalid login credentials",
    "4004": "User with this email/phone already exists.",
    "4005": "User is not verified.",
    "4006": "New password and Confirm password are not same.",
    "4007": "Link expired.",
    "4008": "Sorry! Your account is not active. We have sent you a verification link to activate your account.",
    "4009": "Invalid OTP.",
    "4010": "Invalid phone no.",
    "4011": "Object not found.",
    "4012": "Token is expired or invalid",
    "4013": "End date must occur after Start date.",
    "4014": "Business with this email id already exists",
    "4015": "Business Profile already exists",
    "4016": "Invalid Input",

}

SMS_TEMPLATE = {
    "0001": {
        "message": "Hi {first_name} , \nPlease use {otp} as OTP for verification of your Phone number."
    }
}
