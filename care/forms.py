from django import forms

from care.models import Procedure
from pets.models import Pet


class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure
        fields = ['pet', 'name', 'description', 'scheduled_date', 'done', 'done_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание процедуры'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'done_at': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
        }

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        if user is not None:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)
        if self.instance.pk:
            self.fields['done'].disabled = False
