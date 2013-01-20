from django import forms
from witness.models import Decision
import bleach

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
    def clean(self):
        cleaned_data = super(DecisionForm, self).clean()
        for key in ('full_name', 'address', 'action_text'):
            cleaned_data[key] = bleach.clean(cleaned_data[key])
        return cleaned_data
        
    class Meta:
        model = Decision
        fields = ('full_name', 'address', 'is_agreed')
