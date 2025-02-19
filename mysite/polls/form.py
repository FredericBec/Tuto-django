from django import forms


class PollForm(forms.Form):
    question_text = forms.CharField(label="Question", max_length=100)
