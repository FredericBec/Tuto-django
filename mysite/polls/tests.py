import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localtime
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from .models import Question, Choice


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:all"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:all"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:all"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:all"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:all"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class PollsApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.question = create_question(question_text='Quel est votre couleur préférée?', days=1)
        cls.choice = Choice.objects.create(question=cls.question, choice_text='nouveau choix', votes=0)
        cls.question_2 = create_question(question_text='zero + zero?', days=2)
        cls.choice_2 = Choice.objects.create(question=cls.question_2, choice_text='tête à toto', votes=1)


class QuestionApiTests(PollsApiTestCase):

    url = reverse_lazy('question-list')

    def test_question_list(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'question_text': question.question_text,
                'pub_date': localtime(question.pub_date).isoformat(),
                'course': None
            } for question in [self.question, self.question_2]
        ]
        self.assertEqual(excepted, response.json())

    def test_create_question(self):

        question_count = Question.objects.count()

        response = self.client.post(self.url, data={'question_text': 'nouvelle question', 'pub_date': '2025-01-20'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Question.objects.count(), question_count)


class ChoiceApiTests(PollsApiTestCase):

    url = reverse_lazy('choice-list')

    @staticmethod
    def get_choice_list_data(choices):
        return [
            {
                'question': choice.question.pk,
                'choice_text': choice.choice_text,
                'votes': choice.votes
            } for choice in choices
        ]

    def test_choice_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_choice_list_data([self.choice, self.choice_2]), response.json())

    def test_choice_list_filter(self):
        response = self.client.get(self.url + f'?question_id={self.question.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_choice_list_data([self.choice]), response.json())

    def test_create_choice(self):
        choice_count = Choice.objects.count()
        response = self.client.post(self.url, data={'choice_text': 'nouveau choix', 'votes': 0})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Choice.objects.count(), choice_count)

    def test_delete_choice(self):
        response = self.client.delete(reverse('choice-detail', kwargs={'pk': self.choice.pk}))
        self.assertEqual(response.status_code, 405)
        self.choice.refresh_from_db()
