from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import BlogPost


class BlogPostPlugin(CMSPluginBase):
    model = BlogPost
    name = _('Blog post')
    render_template = 'djangocms_blogpost/post.html'

plugin_pool.register_plugin(BlogPostPlugin)
