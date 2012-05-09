#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'witness.settings')

from funfactory import manage


manage.setup_environ(__file__, more_pythonic=True)

if __name__ == "__main__":
    manage.main()
