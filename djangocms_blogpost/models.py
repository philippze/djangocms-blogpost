from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from cms.models import Page
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

#from htmlcutstring import cutHtmlString
import re


class CreatePageMixin(object):
    
    def ensure_is_in_page(self, user, parent_page_id):
        try:
            self.placeholder.page.pk
        except AttributeError:
            page = self.create_page(user, parent_page_id)
            self.assign_to_page(page)
            
    
    def create_page(self, user, parent_page_id):
        from cms import api # Import here because not available before model creation
        try:
            parent = Page.objects.get(
                reverse_id=parent_page_id,
                publisher_is_draft=True
            )
        except Page.DoesNotExist:
            parent = self.get_parent_page()
        page = api.create_page(
            self.name,
            self.PAGE_TEMPLATE,
            get_language(),
            created_by=user,
            parent=parent,
            position='first-child'
        )
        return page
    
    def assign_to_page(self, page):
        placeholder = page.placeholders.get(slot=self.PLACEHOLDER)
        self.placeholder = placeholder
        self.language = get_language()
        self.position = 0
        self.plugin_type = self.PLUGIN_TYPE


class BlogPostManager(models.Manager):
    def pub_for_language(self, current_language):
        published = Q(placeholder__page__publisher_is_draft=False)
        language_fits = Q(language=current_language)
        exists_in_current_language = Q(placeholder__page__languages__contains=current_language)
        return BlogPost.objects.filter(
            published
            & (language_fits | ~exists_in_current_language)
        )


class BlogPost(CreatePageMixin, CMSPlugin):
    name = models.CharField(max_length=100)
    body = HTMLField(_('Text'))
    image = FilerImageField(verbose_name=_('Bild'))
    
    objects = BlogPostManager()

    PAGE_TEMPLATE = 'blog-post.html'
    PLUGIN_TYPE = 'BlogPostPlugin'
    PLACEHOLDER = 'blogpost'
    
    def excerpt(self):
        text = re.sub(r'<[^>]*?>', '', self.body)
        return text[:225]
    
    def copy_relations(self, oldinstance):
        for associated_item in oldinstance.tagged_items.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            associated_item.pk = None
            associated_item.object_id = self.id
            associated_item.save()
