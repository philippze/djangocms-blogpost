from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import BlogPost


class CreatePageMixin(object):
    
    def save_model(self, request, obj, form, change):
        user = request.user
        # This requires a page with the id 'blog':
        obj.ensure_is_in_page(user, 'blog')
        super(CreatePageMixin, self).save_model(request, obj, form, change)
    
    def response_post_save_add(self, request, obj):
        return HttpResponseRedirect('/admin/cms/page/')

    def get_queryset(self, request):
        qs = super(CreatePageMixin, self).get_queryset(request)
        return qs.filter(placeholder__page__publisher_is_draft=True)


class BlogPostAdmin(CreatePageMixin, admin.ModelAdmin):
    pass


admin.site.register(BlogPost, BlogPostAdmin)
