# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

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
