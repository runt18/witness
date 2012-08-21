from contextlib import contextmanager
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import get_language

import test_utils
from funfactory.urlresolvers import get_url_prefix, Prefixer, reverse, set_url_prefix
from tower import activate

from witness.models import Document, DocumentVersion, Decision


class WitnessTestHelper(object):
    """
    Helper class that provides factory methods for model creation and other
    common methods used for testing.
    """

    def create_document(self, **kwargs):
        self.slug_counter = getattr(self, 'slug_counter', 0) + 1
        defaults = {
            'title': 'Test Document %d' % self.slug_counter,
            'slug': 'doc-%d' % self.slug_counter,
        }
        defaults.update(kwargs)
        return Document.objects.create(**defaults)

    def create_documentversion(self, **kwargs):
        self.slug_counter = getattr(self, 'slug_counter', 0) + 1
        defaults = {
            'number': 'v-%d' % self.slug_counter,
            'title': 'Test Version %d' % self.slug_counter,
            'text': 'Lorem ipsum dolor.',
            'yes_action_text': 'Yes',
            'no_action_text': 'No',
            'is_retired': False,
        }
        if 'document' not in kwargs:
            defaults['document'] = self.create_document()
        defaults.update(kwargs)
        return DocumentVersion.objects.create(**defaults)

    def create_decision(self, **kwargs):
        self.slug_counter = getattr(self, 'slug_counter', 0) + 1
        defaults = {
            'email': 'test-%d@example.com' % self.slug_counter,
            'full_name': 'John Doe',
            'ip_address': '111.222.333.444',
            'action_text': 'Yes',
            'is_agreed': True,
        }
        if 'document_version' not in kwargs:
            defaults['document_version'] = self.create_documentversion()
        if 'user' not in kwargs:
            defaults['user'] = User.objects.create(username='test-%d' % self.slug_counter)
        defaults.update(kwargs)
        return Decision.objects.create(**defaults)

    @contextmanager
    def activate(self, locale):
        """Context manager that temporarily activates a locale."""
        old_prefix = get_url_prefix()
        old_locale = get_language()
        rf = test_utils.RequestFactory()
        set_url_prefix(Prefixer(rf.get('/%s/' % (locale,))))
        activate(locale)
        yield
        set_url_prefix(old_prefix)
        activate(old_locale)


class ModelTests(WitnessTestHelper, test_utils.TestCase):

    def test_create_document(self):
        before = datetime.datetime.now()
        doc = self.create_document()
        after = datetime.datetime.now()
        self.assertTrue(doc.creation_time >= before)
        self.assertTrue(doc.creation_time <= after)

    def test_create_document_with_duplicate_slug_returns_error(self):
        doc = self.create_document()

        try:
            self.create_document(slug=doc.slug)
        except IntegrityError:
            pass
        else:
            self.fail()

    def test_latest_version_property_on_document_returns_most_recent_document_version(self):
        doc = self.create_document()
        self.create_documentversion()  # does not belong to doc
        version = self.create_documentversion(document=doc)
        self.create_documentversion(document=doc)

        self.assertEqual(doc.latest_version, version)

    def test_latest_version_property_on_document_when_no_versions_exist_returns_none(self):
        doc = self.create_document()
        self.assertEqual(doc.latest_version, None)

    def test_create_documentversion(self):
        before = datetime.datetime.now()
        version = self.create_documentversion()
        after = datetime.datetime.now()
        self.assertTrue(version.creation_time >= before)
        self.assertTrue(version.creation_time <= after)

    def test_create_decision(self):
        before = datetime.datetime.now()
        decision = self.create_decision()
        after = datetime.datetime.now()
        self.assertTrue(decision.creation_time >= before)
        self.assertTrue(decision.creation_time <= after)


class ViewTests(WitnessTestHelper, test_utils.TestCase):

    def test_home_page_lists_documents_ordered_by_title(self):

        doc1 = self.create_document(title='Charlie')
        self.create_documentversion(document=doc1)
        doc2 = self.create_document(title='Alpha')
        self.create_documentversion(document=doc2)
        doc3 = self.create_document(title='Beta')
        self.create_documentversion(document=doc3)

        with self.activate(settings.LANGUAGE_CODE):
            url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'witness/home.html')
        self.assertTrue('documents' in response.context)
        documents = response.context['documents']
        self.assertEqual(len(documents), 3)
        self.assertEqual(documents[0], doc2)
        self.assertEqual(documents[1], doc3)
        self.assertEqual(documents[2], doc1)

    def test_home_page_does_not_display_documents_that_dont_have_a_version(self):
        doc = self.create_document()
        self.create_documentversion(document=doc)
        self.create_document()  # No version

        with self.activate(settings.LANGUAGE_CODE):
            url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'witness/home.html')
        self.assertTrue('documents' in response.context)
        documents = response.context['documents']
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0], doc)

    def test_document_detail_page_loads(self):
        doc = self.create_document()
        version = self.create_documentversion(document=doc)

        url = reverse('document_detail', args=[doc.slug, version.number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'witness/document_detail.html')
        self.assertEqual(response.context['document_version'], version)

    def test_document_detail_invalid_slug_returns_404(self):
        doc = self.create_document()
        version = self.create_documentversion(document=doc)

        with self.activate(settings.LANGUAGE_CODE):
            url = reverse('document_detail', args=['invalid', version.number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_document_detail_invalid_version_number_returns_404(self):
        doc = self.create_document()
        with self.activate(settings.LANGUAGE_CODE):
            url = reverse('document_detail', args=[doc.slug, 'invalid'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
