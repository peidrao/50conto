import re

from django import forms
from django.utils.translation import gettext_lazy as _

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class FormValidators:
    def password_validation(self):
        if not re.findall('\d', self):
            raise forms.ValidationError(
                _("A senha precisa conter números e letras"))

    def username_validation(self):
        if len(self) <= 3:
            raise forms.ValidationError(_("username curto demais."))

    def email_validation(self):
        if self and not re.match(EMAIL_REGEX, self):
            raise forms.ValidationError(_("Email não segue um padrão correto"))
