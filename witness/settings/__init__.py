# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from .base import *
try:
    from .local import *
except ImportError, exc:
    exc.args = tuple(['{0!s} (did you rename settings/local.py-dist?)'.format(exc.args[0])])
    raise exc
