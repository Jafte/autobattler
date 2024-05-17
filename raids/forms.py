from django import forms


class RaidActionForm(forms.Form):
    point = forms.CharField()
