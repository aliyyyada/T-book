from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label="Автор или название", max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Введите автора или название'}))
