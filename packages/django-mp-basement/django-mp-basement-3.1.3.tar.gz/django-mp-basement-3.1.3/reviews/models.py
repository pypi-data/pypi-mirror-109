
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reviews',
        verbose_name=_('Owner'), null=True, blank=True,
        on_delete=models.SET_NULL)

    is_active = models.BooleanField(_('Is active'), default=False)

    name = models.CharField(_("Name"), max_length=255)

    email = models.EmailField(_("Email"), max_length=255)

    rating = models.PositiveIntegerField(
        _('Rating'), default=5, choices=((x, str(x)) for x in range(1, 6)))

    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    text = models.TextField(_('Review'), max_length=1000, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id', )
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')


class ReviewImage(models.Model):

    review = models.ForeignKey(
        Review, verbose_name=_('Review'), related_name='images',
        on_delete=models.CASCADE)

    file = models.ImageField(_('File'), upload_to='reviews', max_length=255)

    order = models.PositiveIntegerField(_('Ordering'), default=0)

    order_field_name = 'order'
    order_with_respect_to = 'review'

    def get_preview(self, size):

        from sorl.thumbnail import get_thumbnail

        if not self.file:
            return None

        return get_thumbnail(self.file.file, size)

    def get_preview_tag(self, width=100, empty_label='-----'):

        if not self.file:
            return empty_label

        try:
            url = self.get_preview(str(width)).url
        except Exception:
            return _('Image not found')

        return mark_safe(
            '<img src="{}" width: {}px; title="{}" />'.format(
                url, width, self.file.url))

    @property
    def preview_tag(self):
        return self.get_preview_tag()

    preview_tag.fget.short_description = _('Preview')

    def __str__(self):
        return str(self.review)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = _('Review image')
        verbose_name_plural = _('Review images')
