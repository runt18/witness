# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table('witness_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('witness', ['Document'])

        # Adding model 'DocumentVersion'
        db.create_table('witness_documentversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['witness.Document'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('yes_action_text', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('no_action_text', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_retired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('witness', ['DocumentVersion'])

        # Adding model 'Decision'
        db.create_table('witness_decision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('document_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['witness.DocumentVersion'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('text_hash', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('action_text', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_yes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_no', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('witness', ['Decision'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table('witness_document')

        # Deleting model 'DocumentVersion'
        db.delete_table('witness_documentversion')

        # Deleting model 'Decision'
        db.delete_table('witness_decision')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'witness.decision': {
            'Meta': {'object_name': 'Decision'},
            'action_text': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['witness.DocumentVersion']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'is_no': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_yes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text_hash': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'witness.document': {
            'Meta': {'object_name': 'Document'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'witness.documentversion': {
            'Meta': {'object_name': 'DocumentVersion'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['witness.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'no_action_text': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'yes_action_text': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['witness']