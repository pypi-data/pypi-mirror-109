
from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField
from assets.multiupload import MultiFileField

from reviews.models import Review


class ReviewForm(forms.ModelForm):

    images = MultiFileField(
        label=_('Images'), max_num=100, min_num=1, required=False)

    captcha = ReCaptchaField()

    class Meta:
        model = Review
        fields = ['name', 'email', 'text', 'rating']
