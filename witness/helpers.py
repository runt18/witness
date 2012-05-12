import jinja2

from jingo import register

import markdown as md

@register.filter
def markdown(s):
    return jinja2.Markup(md.markdown(unicode(s)))
