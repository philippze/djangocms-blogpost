from django import template
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from djangocms_blogpost.models import BlogPost

import datetime


register = template.Library()


@register.filter
def short_date(date):
    try:
        day = date.day
    except AttributeError:
        date = datetime.datetime.now()
        day = date.day
    month = date.strftime("%B")
    year = date.year
    this_year = datetime.datetime.now().year
    html = '<strong>%s.</strong> %s' % (day, month[:3])
    if not year == this_year:
        html = '%s<br />%s' % (html, year)
    return mark_safe(html)


@register.assignment_tag
def get_blogposts(length=None):
    current_language = get_language()
    posts = BlogPost.objects.pub_for_language(current_language).order_by('placeholder__page__path')
    if length is None:
        return posts
    else:
        return posts[:length]
