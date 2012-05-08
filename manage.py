#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'witness.settings')

from funfactory import manage


manage.setup_environ(__file__, more_pythonic=True)

if __name__ == "__main__":
    manage.main()
