from django import forms

from diary.models import DiaryEntry
from pets.models import Pet


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['pet', 'date', 'title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Краткое описание события'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        if user is not None:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)
