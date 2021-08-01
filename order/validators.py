import re
from django.utils.translation import gettext_lazy as _
from django import forms

ZIPCODE = r"^([0-9]{5}-[0-9]{3})"
DATE_CARD = r"^(0[1-9]|10|11|12)/20[0-9]{2}$"

class OrderValidator:
    def zipcode_validation(self):
        if self and not re.match(ZIPCODE, self):
            raise forms.ValidationError(_("CEP precisa ser escrito: 00000-000"))
