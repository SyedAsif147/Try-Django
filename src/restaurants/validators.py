from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

def validate_email(value):
	email = value
	if '.edu' in email:
		raise ValidationError("We do not accept edu emails") 

CATEGORIES = ['Indian', 'Non Veg', 'Veg', 'Barbeque', 'Something']

def validate_category(value):
	cat = value.capitalize()
	if not value in CATEGORIES and not cat in CATEGORIES:
		raise ValidationError(f"{value} not a valid category")