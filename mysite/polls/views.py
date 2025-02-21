from email.policy import default

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Max
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .form import PollForm, LearnerRegisterForm, CourseQuestionForm
from .models import Question, Choice, Course, Learner


class IndexView(generic.TemplateView):
    template_name = "polls/index.html"


class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_choices"] = self.object.get_choices()
        return context


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("polls:index")
    template_name = "authenticate/register.html"


class CourseView(LoginRequiredMixin, generic.ListView):
    login_url = "/polls/course_register/"
    template_name = "courses/courses.html"
    context_object_name = "latest_course_list"

    def get_queryset(self):
        return Course.objects.filter(start_date__lte=timezone.now()).order_by("start_date")[:10]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        learner = Learner.objects.filter(user=self.request.user).first()

        if learner:
            taken_courses = learner.courses.all()
        else:
            taken_courses = []

        context["taken_courses"] = taken_courses
        return context


def vote(request, question_id):
    """
    Question votes
    :param request: request send
    :param question_id: id of the question
    :return: redirect to results view
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def statistics(request):
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    total_votes = Choice.objects.aggregate(Sum("votes"))
    avg_votes = Choice.objects.aggregate(Avg("votes", default=0))
    last_id = Question.objects.aggregate(id=Max("id"))
    last_question_recorded = Question.objects.get(pk=last_id.get("id"))

    context = {
        "total_questions": total_questions,
        "total_choices": total_choices,
        "total_votes": total_votes,
        "avg_votes": avg_votes,
        "last_question_recorded": last_question_recorded
    }

    return render(request, "polls/statistics.html", context)


def get_question(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:login"))

    if not hasattr(request.user, "teacher"):
        return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")

    if request.method == "POST":
        form = PollForm(request.POST)

        if form.is_valid():
            question_text = form.cleaned_data["question_text"]
            choice_texts = request.POST.getlist("choice_text[]")

            new_question = Question(question_text=question_text, pub_date=timezone.now())
            new_question.save()
            for choice_text in choice_texts:
                if choice_text.strip():
                    new_question.choice_set.create(question=new_question, choice_text=choice_text, votes=0)

            return HttpResponseRedirect(reverse("polls:all"))

    else:
        form = PollForm()

    return render(request, "polls/poll_form.html", {"form": form})


def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("polls:index"))
            else:
                return render(request, "authenticate/login.html", {"error_message": "You didn't enter a valid username or password"})

    return render(request, "authenticate/login.html")


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("polls:index"))


def LearnerRegister(request):
    if request.method == "POST":
        form = LearnerRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            address = form.cleaned_data["address"]
            course = form.cleaned_data["course"]

            learner = Learner.objects.create(user=user, address=address)

            if course:
                learner.courses.set(course)

            login(request, user)
            return HttpResponseRedirect(reverse("polls:courses"))
    else:
        form = LearnerRegisterForm()

    return render(request, "courses/course_register.html", {"form": form})


def add_course_question(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:login"))

    if not hasattr(request.user, "teacher"):
        return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")

    if request.method == "POST":
        form = CourseQuestionForm(request.POST)

        if form.is_valid():
            course = form.cleaned_data["course"]
            question_text = form.cleaned_data["question_text"]
            choice_texts = request.POST.getlist("choice_text[]")

            new_question = Question(course=course, question_text=question_text, pub_date=timezone.now())
            new_question.save()
            for choice_text in choice_texts:
                if choice_text.strip():
                    new_question.choice_set.create(question=new_question, choice_text=choice_text, votes=0)

            return HttpResponseRedirect(reverse("polls:courses"))

    else:
        form = CourseQuestionForm()

    return render(request, "courses/add_course_question.html", {"form": form})


def course_vote(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    question = Question.objects.filter(course=course).first()
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
