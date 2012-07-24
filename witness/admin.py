# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from witness.models import Document, DocumentVersion, Decision

# Globally disable delete selected
admin.site.disable_action('delete_selected')

admin.site.register(Document)
admin.site.register(DocumentVersion)
admin.site.register(Decision)
