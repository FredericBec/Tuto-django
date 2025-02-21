from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .form import CourseAdminForm
from .models import Question, Choice, Learner, Teacher, Course


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]})
    ]
    inlines = [ChoiceInline]

    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["question_text", "pub_date"]
    ordering = ["pub_date"]
    search_fields = ["question_text", "pub_date"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "question", "votes"]
    list_filter = ["choice_text", "question", "votes"]
    ordering = ["votes"]
    search_fields = ["choice_text", "question__question_text", "votes"]


class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ["name", "teacher", "start_date", "end_date"]
    list_filter = ["name"]
    ordering = ["name", "start_date", "end_date"]
    search_fields = ["name"]
    filter_vertical = ["learners"]


class LeanerInline(admin.StackedInline):
    model = Learner
    can_delete = False
    verbose_name_plural = "learner"


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = "teacher"


class UserAdmin(BaseUserAdmin):
    inlines = [LeanerInline, TeacherInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
