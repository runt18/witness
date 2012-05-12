import jinja2

from jingo import register

from babel import dates

import markdown as md

@register.filter
def markdown(s):
    return jinja2.Markup(md.markdown(unicode(s)))

@register.filter
def date(t):
    return dates.format_date(t)
