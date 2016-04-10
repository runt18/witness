# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from django.core import urlresolvers
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect

from witness.models import Document, DocumentVersion, Decision

# Globally disable delete selected
admin.site.disable_action('delete_selected')

class DocumentAdmin(admin.ModelAdmin):
    def view_latest_version(self, request, queryset):
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
        try:
            document = queryset.get()
            return redirect( "{0!s}?document={1!s}".format(
                    urlresolvers.reverse('admin:witness_documentversion_add'),
                    document.id)
                   )
        except Document.MultipleObjectsReturned:
            ''' Multiple documents are checked '''
            self.message_user(
                    request,
                    "Only one document can be selected"
                )

    change_form_template = 'witness_admin/document_change_form.html'

    actions = (view_latest_version, add_new_version)
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
                "Successfully retired {0!s} document version(s)".format(
                    queryset.count())
            )
    def document_title(self, obj):
        return str(obj.document.title)

    def num_signatures(self, obj):
        return Decision.objects.filter(document_version=obj).count()
    num_signatures.short_description = "Number of Signatures"

    def change_view(self, request, object_id, extra_context=None):
        '''
        If a document version has been signed,
        no one can edit it
        '''
        if Decision.objects.filter(document_version__id=object_id).count()!=0:
            return HttpResponseBadRequest("The document has been signed")
        return super(DocumentVersionAdmin, self).change_view(request,
                object_id, extra_context=extra_context)

    actions = (clone_and_modify, retire)
    list_display = ('title', 'number', 'document_title', 'num_signatures',
                    'require_name', 'require_address')


class DecisionAdmin(admin.ModelAdmin):
    ''' Prevent admins from manually tampering with the decision '''
    readonly_fields = Decision._meta.get_all_field_names()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def document(self, obj):
        return obj.document_version.document.title
    def document_version(self, obj):
        return obj.document_version.title

    list_display = (
            'document',
            'document_version',
            'email',
            'is_agreed',
            'action_text',
            'creation_time')
    change_form_template = 'witness_admin/decision_change_form.html'


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentVersion, DocumentVersionAdmin)
admin.site.register(Decision, DecisionAdmin)
