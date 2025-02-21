from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Course, Learner


class PollForm(forms.Form):
    question_text = forms.CharField(label="Question", max_length=100)


class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    learners = forms.ModelMultipleChoiceField(
        queryset=Learner.objects.all(), required=False  # Champ devient facultatif
    )


class LearnerRegisterForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea, required=True)
    course = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "address", "course"]


class CourseQuestionForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        empty_label="Sélectionner un cours"
    )
    question_text = forms.CharField(label="Question", max_length=100)
