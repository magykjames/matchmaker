from django import forms

from .models import LEVELS

class UserResponseForm(forms.Form):
    question_id = forms.IntegerField()
    user_answer_id = forms.IntegerField()
    importance_level = forms.ChoiceField(choices=LEVELS)
    match_answer_id = forms.IntegerField()
    match_importance_level = forms.ChoiceField(choices=LEVELS)
