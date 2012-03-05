from django import forms

class SearchForm(forms.Form):
    free_text = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    tag_mode = forms.ChoiceField(choices=(('all', 'all',), ('any', 'any',)))

class modelCreationForm(forms.Form):
    album_name = forms.CharField(min_length=3)
    album_height = forms.IntegerField(min_value=1, max_value=800, initial=500, label='Height in pixel')
    album_width = forms.IntegerField(min_value=1, max_value=800, initial=700, label='Width in pixel')
