import hashlib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from session_csrf import anonymous_csrf

from witness import models

@anonymous_csrf
def document_detail(request, document_slug, version_number):
    document_version = \
        get_object_or_404(models.DocumentVersion, document__slug=document_slug,
                          number=version_number)
    answered_yes = False
    answered_no = False
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
            decision.save()
            return HttpResponse("TODO: post-signing page")
    data = {'document_version': document_version, 'answered_yes': answered_yes,
            'answered_no': answered_no}
    return render(request, 'witness/document_detail.html', data)
