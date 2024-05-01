from django import forms

from robots.enums import RobotAction


class RobotActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('', '-- выберите действие --')] + RobotAction.choices)
