import jwt
from django import forms
from django.conf import settings

from robots.enums import RobotAction


class RobotActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('', '-- выберите действие --')] + RobotAction.choices)


class RobotCreatForm(forms.Form):
    name = forms.CharField(max_length=100)
    robot_option_key = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        robot_option_key = self.cleaned_data['robot_option_key']
        try:
            jwt.decode(robot_option_key, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            raise forms.ValidationError(message="Жулишь?")
