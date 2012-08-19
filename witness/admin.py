# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from witness.models import Document, DocumentVersion, Decision

# Globally disable delete selected
admin.site.disable_action('delete_selected')

class DocumentVersionAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        ''' 
        If a document version has been signed,
        no one can edit it
        '''
        return (Decision.objects.filter(document_version=obj).count()==0)

class DecisionAdmin(admin.ModelAdmin):
    ''' Prevent admins from manually tampering with the decision '''
    readonly_fields = Decision._meta.get_all_field_names()

    def has_delete_permission(self, request, obj=None):
        ''' Disable delete '''
        return False
    

admin.site.register(Document)
admin.site.register(DocumentVersion, DocumentVersionAdmin)
admin.site.register(Decision, DecisionAdmin)
