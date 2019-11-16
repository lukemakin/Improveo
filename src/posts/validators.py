from django.core.exceptions import ValidationError


def validate_ext(value):
    value = str(value)
    ext = value.split(".")[-1]
    valid_extensions = ['jpg', 'jpeg', 'png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('This file extension is not allowed.')
