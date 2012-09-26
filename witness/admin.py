# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from django.core import urlresolvers
from django.shortcuts import redirect

from witness.models import Document, DocumentVersion, Decision

# Globally disable delete selected
admin.site.disable_action('delete_selected')

class DocumentAdmin(admin.ModelAdmin):
    def view(self, request, queryset):
        ''' View the latest version of a document '''
        try:
            document = queryset.get()
            return redirect(
                    document.latest_version.get_absolute_url()
                )
        except Document.MultipleObjectsReturned:
            ''' Multiple documents are checked '''
            self.message_user(
                    request, 
                    "Only one document can be selected"
                )

    def add_new_version(self, request, queryset):
        ''' Add a new version for a document '''
        return redirect(
                urlresolvers.reverse(
                    'admin:witness_documentversion_add',
                    )
                )

    actions = (view, add_new_version)
    list_display = ('title', 'latest_version')

class DocumentVersionAdmin(admin.ModelAdmin):
    def clone_and_modify(self, request, queryset):
        ''' 
        Clone an existing document version, and redirect to the change page
        '''
        try:
            original_dv = queryset.get()
            new_dv = DocumentVersion(
                    document=original_dv.document,
                    title=original_dv.title,
                    text=original_dv.text,
                    yes_action_text=original_dv.yes_action_text,
                    no_action_text=original_dv.no_action_text
                )
            new_dv.save()
            return redirect(
                    urlresolvers.reverse(
                        'admin:witness_documentversion_change',
                        args=(new_dv.id,)
                        )
                )
        except DocumentVersion.MultipleObjectsReturned:
            ''' Multiple versions are checked '''
            self.message_user(
                    request, 
                    "Only one document version can be selected"
                )

    def retire(self, request, queryset):
        queryset.update(is_retired=True)
        self.message_user(
                request, 
                "Successfully retired %s document version(s)" % 
                    queryset.count()
            )
    def document_title(self, obj):
        return str(obj.document.title)

    def num_signatures(self, obj):
        return Decision.objects.filter(document_version=obj).count()
    num_signatures.short_description = "Number of Signatures"

    actions = (clone_and_modify, retire)
    list_display = ('title', 'number', 'document_title', 'num_signatures')

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
    

admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentVersion, DocumentVersionAdmin)
admin.site.register(Decision, DecisionAdmin)
