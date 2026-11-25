from django import forms

from pets.models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'sex', 'birth_date', 'weight', 'photo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Кличка', 'class': 'input'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Описание питомца'}),
        }
