# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import hashlib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from session_csrf import anonymous_csrf

from witness import models

@anonymous_csrf
def home(request):
    documents = [document for document in
                 models.Document.objects.all().order_by("title")
                 if document.versions.count() > 0]
    data = {"documents": documents}
    return render(request, "witness/home.html", data)

@anonymous_csrf
def document_detail(request, document_slug, version_number):
    document_version = \
        get_object_or_404(models.DocumentVersion, document__slug=document_slug,
                          number=version_number)
    answered_yes = False
    answered_no = False
    latest_decision = None
    if request.user.is_authenticated():
        user = request.user
        decisions = \
            models.Decision.objects.filter(document_version=document_version,
                                           user=user)
        if decisions.count() > 0:
            latest_decision = decisions.latest()
            answered_yes = latest_decision.is_yes
            answered_no = latest_decision.is_no
        if 'yes' in request.POST or 'no' in request.POST:
            text_hash = hashlib.sha1(document_version.text).hexdigest()
            decision = models.Decision(document_version=document_version,
                                       user=user, email=user.email,
                                       full_name=user.get_full_name(),
                                       ip_address=request.META["REMOTE_ADDR"],
                                       text_hash=text_hash)
            if 'yes' in request.POST:
                decision.action_text = document_version.yes_action_text
                decision.is_yes = True
            if 'no' in request.POST:
                if 'yes' in request.POST:
                    return HttpResponse(status=400)
                decision.action_text = document_version.no_action_text
                decision.is_no = True
            if not ((answered_yes and decision.is_yes) or
                    (answered_no and decision.is_no)):
                decision.save()
                return redirect('/%s/%s/' % (document_slug, version_number))
    data = {'document_version': document_version, 'answered_yes': answered_yes,
            'answered_no': answered_no, "latest_decision": latest_decision}
    return render(request, 'witness/document_detail.html', data)
