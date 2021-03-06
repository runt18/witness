# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import hashlib

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404, render, redirect

from session_csrf import anonymous_csrf

from witness import models, forms

@anonymous_csrf
def home(request):
    documents = [document for document in
                 models.Document.objects.all().order_by("title")
                 if document.versions.count() > 0]
    my_responses = None
    if request.user.is_authenticated():
        my_dvs = models.DocumentVersion.objects.filter(
                        decisions__user=request.user
                    ).exclude(
                        is_retired=True
                    ).order_by(
                        "title",
                        "-number"
                    ).distinct()
        my_responses = [dv.decisions.latest() for dv in my_dvs]

    data = {
            "documents" : documents,
            "my_responses" : my_responses
           }
    return render(request, "witness/home.html", data)

@anonymous_csrf
def document_detail(request, document_slug, version_number):
    document_version = get_object_or_404(
                            models.DocumentVersion,
                            document__slug=document_slug,
                            number=version_number)
    all_decisions = None
    latest_decision = None
    latest_version = None
    previous_versions = None
    form = None
    if document_version != document_version.document.latest_version:
        latest_version = document_version.document.latest_version
    if request.user.is_authenticated():
        user = request.user
        decisions = models.Decision.objects.filter(
                                        document_version=document_version,
                                        user=user)
        if decisions.count() > 0:
            latest_decision = decisions.latest()

        if request.user.is_superuser:
            # Show more info for superuser
            previous_versions = models.DocumentVersion.objects.filter(
                                                document=document_version.document
                                            ).exclude(
                                                id=document_version.id
                                            )
            all_users = list(set(models.Decision.objects.filter(
                        document_version=document_version
                    ).values_list('user', flat=True)))
            all_decisions = [models.Decision.objects.filter(
                                document_version=document_version,
                                user=u).latest()
                             for u in all_users]

        text_hash = hashlib.sha1(document_version.text).hexdigest()
        decision = models.Decision(document_version=document_version,
                                    user=user,
                                    email=user.email,
                                    full_name=user.get_full_name(),
                                    ip_address=request.META["REMOTE_ADDR"],
                                    text_hash=text_hash)
        if request.method == 'GET':
            form = forms.DecisionForm(instance=decision)
        elif request.method == 'POST':
            form = forms.DecisionForm(request.POST, instance=decision)

            if form.is_valid() and\
               (not latest_decision or
                not (latest_decision.is_agreed and form.instance.is_agreed)):
                # If the decision changed, save a new one
                decision = form.save(commit=False)
                decision.action_text = document_version.yes_action_text\
                                if decision.is_agreed\
                                else document_version.no_action_text
                decision.save()

                message = "Here's the document: {0!s} ".format(request.build_absolute_uri(
                        document_version.get_absolute_url()))
                send_mail(subject="You signed {0!s}".format((decision)),
                          message=message,
                          from_email='admin@example.com',
                          recipient_list=(user.email,),)

                return redirect(
                           reverse(
                               'witness.views.document_detail',
                                kwargs={
                                    'document_slug' : document_slug,
                                    'version_number' : version_number
                                }
                           )
                       )
    data = {
            "document_version" : document_version,
            "latest_decision" : latest_decision,
            "latest_version" : latest_version,
            "previous_versions" : previous_versions,
            "all_decisions" : all_decisions,
            "form" : form
        }
    return render(request, 'witness/document_detail.html', data)
