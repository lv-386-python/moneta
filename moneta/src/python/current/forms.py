from django import forms

from icons.models import Icon

icons = Icon.get_icons('current')

ICON_CHOICES = tuple([(str(icon.id), icon.css) for icon in icons])


class EditCurrentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, max_length=45)

    current_icons = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=ICON_CHOICES,
        error_messages={'required': "You didn't select any icon."})
