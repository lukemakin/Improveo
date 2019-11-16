from django.core.exceptions import ValidationError
import os
import magic


def validate_ext(value):
    print(type(value), type(value.name))
    # <class 'django.db.models.fields.files.ImageFieldFile'> <class 'str'>
    ext = os.path.splitext(value.name)[1]
    ext_allowed = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in ext_allowed:
        raise ValidationError('This image format is not allowed')


### brew install libmagic ###

# def validate_ext(value):
#     filetype = magic.from_buffer(value.read())
#     ext_allowed = ['jpg', 'jpeg', 'png']
#     ext_list = []

#     for ext in ext_allowed:
#         if ext in filetype.lower():
#             ext_list.append(ext)

#     if len(ext_list) == 0:
#         raise ValidationError('This image format is not allowed')
