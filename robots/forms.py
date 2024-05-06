from django import forms

from gameplay.person import BasePerson
from robots.enums import RobotAction
from robots.models import Robot


class RobotActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('', '-- выберите действие --')] + RobotAction.choices)


class RobotCreatForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    experience = forms.IntegerField(min_value=0)
    strength = forms.IntegerField(max_value=20, min_value=0)
    dexterity = forms.IntegerField(max_value=20, min_value=0)
    intelligence = forms.IntegerField(max_value=20, min_value=0)
    constitution = forms.IntegerField(max_value=20, min_value=0)
    wisdom = forms.IntegerField(max_value=20, min_value=0)
    charisma = forms.IntegerField(max_value=20, min_value=0)

    class Meta:
        model = Robot
        fields = [
            "name",
            "experience",
            "strength",
            "dexterity",
            "intelligence",
            "constitution",
            "wisdom",
            "charisma",
        ]
