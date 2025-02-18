from django.http import HttpResponse


def index(request):
    """home view"""
    return HttpResponse("Hello, world. You're at the polls index")


def detail(request, question_id):
    """
    Question's detail
    :param request:
    :param question_id: id of the question
    :return: question's detail view
    """
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    """
    View of question's results
    :param request:
    :param question_id:
    :return:
    """
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    """
    View of votes
    :param request:
    :param question_id:
    :return:
    """
    return HttpResponse("You're voting on question %s." % question_id)
