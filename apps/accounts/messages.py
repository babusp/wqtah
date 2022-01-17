"""
accounts messages file
"""

SUCCESS_CODE = {
    '2000': 'OK.',
    '2001': 'User registered successfully.',
    '2002': 'Reset password mail has been sent to your registered email.',
    '2003': 'Password Reset Successfully.',
}

ERROR_CODE = {
    '4000': 'ERROR.',
    '4001': "User with this email doesn't exists.",
    '4002': "Wrong password.",
    '4003': "User is deactivated.",
    '4004': "User with this email already exists.",
    '4005': "User is not verified.",
    '4006': "New password and Confirm password are not same.",
    '4007': "Link Expired.",
}
