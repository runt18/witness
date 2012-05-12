import jinja2

import jingo

import markdown as md

@jingo.register.filter
def markdown(s):
    return jinja2.Markup(md.markdown(unicode(s)))
