from django import forms

from robots.enums import RobotAction
from robots.models import Robot


class RobotActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('', '-- выберите действие --')] + RobotAction.choices)


class RobotCreatForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    strength = forms.IntegerField(max_value=20, min_value=0)
    agility = forms.IntegerField(max_value=20, min_value=0)

    class Meta:
        model = Robot
        fields = ["name", "strength", "agility"]
