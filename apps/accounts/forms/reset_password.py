"""
reset-password form file
"""
# django imports
from django import forms


class ResetPasswordForm(forms.Form):
    """ used to validate the reset-password form """
    new_password = forms.CharField(max_length=30, min_length=8)
    confirm_password = forms.CharField(max_length=30, min_length=8)
    token = forms.CharField(max_length=30)
    email = forms.EmailField()
