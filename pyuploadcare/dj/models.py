from django.db import models
from django.core.exceptions import ValidationError

from pyuploadcare.dj import forms, UploadCare
from pyuploadcare.file import File


class FileField(models.Field):
    __metaclass__ = models.SubfieldBase

    description = "UploadCare file id/URI with cached data"

    custom_attrs = {}

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, basestring):
            return UploadCare().file(value)

        if isinstance(value, File):
            return value

        raise ValidationError('Invalid value for a field')

    def get_prep_value(self, value):
        return value.serialize()

    def get_db_prep_save(self, value, connection=None):
        if value:
            value.store()
            return value.serialize()

    def value_to_string(self, obj):
        assert False

    def formfield(self, **kwargs):
        defaults = {'widget': forms.FileWidget,
                    'form_class': forms.FileField,
                    'custom_attrs': self.custom_attrs}
        defaults.update(kwargs)

        # yay for super!
        return super(FileField, self).formfield(**defaults)




class ImageField(FileField):
    def __init__(self, **kwargs):
        self.custom_attrs = dict(self.custom_attrs)
        self.custom_attrs['data-images-only'] = ""
        super(ImageField, self).__init__(**kwargs)

