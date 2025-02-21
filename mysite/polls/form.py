from django import forms

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
