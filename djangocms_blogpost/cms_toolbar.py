from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from .models import BlogPost

@toolbar_pool.register
class BlogpostToolbarExtension(CMSToolbar):
    
    def populate(self):
        menu = self.toolbar.get_or_create_menu('blogpost', _('Blog'))
        url = reverse('admin:djangocms_blogpost_blogpost_add')
        menu.add_sideframe_item(_('Add a post'), url)
    
    def post_template_populate(self):
        pass
    
    def request_hook(self):
        pass

