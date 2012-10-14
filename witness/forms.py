from django import forms
from witness.models import Decision

class DecisionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DecisionForm, self).__init__(*args, **kwargs)
        document_version = self.instance.document_version
        self.fields['is_agreed'] = forms.TypedChoiceField(
                   label="Do you agree?",
                   choices=((True, document_version.yes_action_text),
                            (False, document_version.no_action_text)),
                   widget=forms.RadioSelect(attrs={'class':'radio'})
                )
        if document_version.require_name:
            self.fields['full_name'] = forms.CharField(widget=forms.TextInput(
                            attrs={'placeholder': 'John Doe'}))
        else:
            self.fields['full_name'] = forms.CharField(required=False,
                                            widget=forms.HiddenInput())

        if document_version.require_address:
            self.fields['address'] = forms.CharField(
                            widget=forms.TextInput(
                            attrs={'placeholder': '1 Anystreet Anytown, CA'}))
        else:
            self.fields['address'] = forms.CharField(required=False,
                                        widget=forms.HiddenInput())

    class Meta:
        model = Decision
        fields = ('full_name', 'address', 'is_agreed')
