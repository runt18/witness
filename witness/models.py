# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import models as auth_models

class Document(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128, verbose_name=_('title'))
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    @property
    def latest_version(self):
        return self.versions.latest()

class DocumentVersion(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    document = models.ForeignKey(Document, related_name='versions')
    number = models.CharField(max_length=64, verbose_name=_('version number'))
    title = models.CharField(max_length=128,
                             verbose_name=_('full title of this version'))
    text = models.TextField(verbose_name=_('document text'))
    yes_action_text = models.CharField(max_length=64)
    no_action_text = models.CharField(max_length=64)
    is_retired = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        get_latest_by = 'creation_time'

class Decision(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    # Prevent deletion of the referenced object
    document_version = models.ForeignKey(DocumentVersion,
                                         on_delete=models.PROTECT)
    user = models.ForeignKey(auth_models.User)
    email = models.EmailField(verbose_name=_("user's email address"))
    full_name = models.CharField(max_length=128,
                                 verbose_name=_("user's full name"),
                                 blank=True)
    ip_address = models.CharField(max_length=64, verbose_name=_('IP address'))
    text_hash = models.CharField(max_length=128,
                                 verbose_name=_('hash of document text'))
    action_text = models.CharField(max_length=64,
                                   verbose_name=_('text of chosen action'))
    is_agreed = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.document_version.title, self.action_text)

    class Meta:
        get_latest_by = 'creation_time'
