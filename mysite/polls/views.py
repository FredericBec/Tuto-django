from email.policy import default

from django.db.models import Sum, Avg, Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.TemplateView):
    template_name = "polls/index.html"


class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


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
