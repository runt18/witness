# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import models as auth_models

class Document(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    slug = models.SlugField()

    @property
    def latest_version(self):
        return self.versions.latest()

class DocumentVersion(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    document = models.ForeignKey(Document, related_name='versions')
    number = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    text = models.TextField()
    yes_action_text = models.CharField(max_length=64)
    no_action_text = models.CharField(max_length=64)
    is_retired = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'creation_time'

class Decision(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    document_version = models.ForeignKey(DocumentVersion)
    user = models.ForeignKey(auth_models.User)
    email = models.EmailField()
    full_name = models.CharField(max_length=128, blank=True)
    ip_address = models.CharField(max_length=64)
    text_hash = models.CharField(max_length=128)
    action_text = models.CharField(max_length=64)
    is_yes = models.BooleanField()
    is_no = models.BooleanField()

    class Meta:
        get_latest_by = 'creation_time'
