# Django Tutorial

## Polls Application

### Part one

Création du projet, initialisation du serveur de développement et création de la vue polls


### Part two

1. Configuration de la base de données
2. Création des models Question et Choice puis insertion dans la base de données
3. Création du site d'administration


#### Exos Part one and two
1. Ajout de la ligne admin.site.register(Choice) dans admin.py pour l'ajouter à la console d'administration
2. Ajout de 5 questions avec 3 choix pour chaque question depuis la console d'administration

    | Question                                              | Choix 1            | Choix 2                         | Choix 3    |
    |-------------------------------------------------------|--------------------|---------------------------------|------------|
    | What is the next movie you will go see at the cinema? | Un parfait inconnu | Captain America Brave New World | Hola Frida |
    | Which programming language do you prefer?             | Java               | Python                          | Php        |
    | What pet do you have?                                 | a dog              | a cat                           | a rabbit   |
    | What is your favorite framework?                      | Angular            | Django                          | Symfony    |
    | Which framework would you like to learn to use?       | React              | VuesJS                          | .NET       |

3. Visualisation des résultats
   1. tous les attributs des classes ne sont pas visibles.
   2. On ne peut filtrer qu'avec les noms des différentes listes
   3. On ne peut pas trier les données selon les attributs
   4. Non mais à partir d'un choix, on peut naviguer vers la question correspondante avec l'icône <img src="https://icones.pro/wp-content/uploads/2021/05/symbole-de-l-oeil-bleu.png" alt="oeil bleu" width="20" height="20">

4. Modification du ModelAdmin
   1. Ajout des classes ModelAdmin QuestionAdmin et ChoiceAdmin
   2. Ajout des 4 options aux 2 classes d'admin
         
       | option         | description                                       |
       |----------------|---------------------------------------------------|
       | list_display   | permet d'afficher tous les attributs d'une classe |
       | list_filter    | permet de filtrer selon un attribut d'une classe  |
       | ordering       | permet d'ordonner selon un champ                  |
       | search _fields | permet de rechercher selon un attribut            |
   3. Ajout de la classe QuestionAdmin et ChoiceAdmin en paramètre du register

5. Après avoir créé un utilisateur avec le super admin, la tentative de connexion avec le nouvel utilisateur a échoué.
6. En ajoutant le statut d'équipe, l'utilisateur peut se connecter au site d'administration, mais sans pouvoir modifier le contenu.
7. En décochant Actif, l'utilisateur ne peut pas se connecter au site d'administration.

#### Exos Django Shell

1. Lister tous les objets de type Question :
   ```
    >>> from polls.models import Choice, Question
    >>> from django.utils import timezone         
    >>> for question in Question.objects.all():
    ...     print(question.id, question.question_text, question.pub_date)                     
    ...
    What's up? 2025-02-17 10:03:23+00:00
    What is the next movie you will go see at the cinema? 2025-02-12 10:20:06+00:00
    Which programming language do you prefer? 2024-11-20 08:15:11+00:00
    What pet do you have? 2024-10-24 10:45:00+00:00
    What is your favorite framework? 2025-01-08 10:38:17+00:00
    Which framework would you like to learn to use? 2024-12-13 09:05:03+00:00
   ```
2. Ajout du filtre sur la date de publication
    ```
    >>> current_month = timezone.now().month            
    >>> Question.objects.filter(pub_date__month=current_month)
    <QuerySet [<Question: What's up? 2025-02-17 10:03:23+00:00>, <Question: What is the next movie you will go see at the cinema? 2025-02-12 10:20:06+00:00>]>
    >>>
   ```
3. Trouver la question d'id 2 et afficher les choix disponibles à la question d'id 2
    ```
    >>> Question.objects.get(pk=2)
    <Question: What is the next movie you will go see at the cinema? 2025-02-12 10:20:06+00:00>
    >>> q = Question.objects.get(pk=2)
    >>> q.choice_set.all()
    <QuerySet [<Choice: Un parfait inconnu>, <Choice: Captain america Brave New World>, <Choice: Hola Frida>]>
    ```
4. Faire une boucle pour afficher les attributs de chaque question et leur choix associés :
    ```
    >>> questions = Question.objects.prefetch_related("choice_set")
    >>> for question in questions:                                                       
    ...     print(f"Question: {question.question_text} - pub_date: {question.pub_date}")
    ...     for choice in question.choice_set.all(): 
    ...             print(f" - {choice.choice_text}")                                    
    ...
    Question: What's up? - pub_date: 2025-02-17 10:03:23+00:00
     - Not much
       - The sky
    Question: What is the next movie you will go see at the cinema? - pub_date: 2025-02-12 10:20:06+00:00
       - Un parfait inconnu
       - Captain america Brave New World
       - Hola Frida
    Question: Which programming language do you prefer? - pub_date: 2024-11-20 08:15:11+00:00
       - Java
       - Python
       - Php
    Question: What pet do you have? - pub_date: 2024-10-24 10:45:00+00:00
       - a dog
       - a cat
       - a rabbit
    Question: What is your favorite framework? - pub_date: 2025-01-08 10:38:17+00:00
       - Angular
       - Django
       - Symfony
    Question: Which framework would you like to learn to use? - pub_date: 2024-12-13 09:05:03+00:00
       - React
       - VueJS
       - .NET
     ```
5. Affichez le nombre de choix pour chaque question :
    ```
    >>> for question in questions:                                                                                       
    ...     print(f"Question: {question.question_text} - pub_date: {question.pub_date} - nbr de choix: {question.choice_set.count()}")
    ...
    Question: What's up? - pub_date: 2025-02-17 10:03:23+00:00 - nbr de choix: 2
    Question: What is the next movie you will go see at the cinema? - pub_date: 2025-02-12 10:20:06+00:00 - nbr de choix: 3
    Question: Which programming language do you prefer? - pub_date: 2024-11-20 08:15:11+00:00 - nbr de choix: 3
    Question: What pet do you have? - pub_date: 2024-10-24 10:45:00+00:00 - nbr de choix: 3
    Question: What is your favorite framework? - pub_date: 2025-01-08 10:38:17+00:00 - nbr de choix: 3
    Question: Which framework would you like to learn to use? - pub_date: 2024-12-13 09:05:03+00:00 - nbr de choix: 3
   ```
6. Chercher toutes les questions triées par le nombre de votes à chaque choix :
    ```
   
   ```
   
7. Trier les questions par ordre antéchronologique :
    ```
    >>> questions = Question.objects.order_by("pub_date").values()
    >>> for question in questions:                                 
    ...     print(question)
    ...
    {'id': 4, 'question_text': 'What pet do you have?', 'pub_date': datetime.datetime(2024, 10, 24, 10, 45, tzinfo=datetime.timezone.utc)}
    {'id': 3, 'question_text': 'Which programming language do you prefer?', 'pub_date': datetime.datetime(2024, 11, 20, 8, 15, 11, tzinfo=datetime.timezone.utc)}
    {'id': 6, 'question_text': 'Which framework would you like to learn to use?', 'pub_date': datetime.datetime(2024, 12, 13, 9, 5, 3, tzinfo=datetime.timezone.utc)}
    {'id': 5, 'question_text': 'What is your favorite framework?', 'pub_date': datetime.datetime(2025, 1, 8, 10, 38, 17, tzinfo=datetime.timezone.utc)}
    {'id': 2, 'question_text': 'What is the next movie you will go see at the cinema?', 'pub_date': datetime.datetime(2025, 2, 12, 10, 20, 6, tzinfo=datetime.timezone.utc)}
    {'id': 1, 'question_text': "What's up?", 'pub_date': datetime.datetime(2025, 2, 17, 10, 3, 23, tzinfo=datetime.timezone.utc)}
   ```
8. Cherchez toutes les questions contenant un mot dans le texte des choix :
    ```
    >>> Question.objects.filter(choice__choice_text__contains="ra")
    <QuerySet [<Question: What is the next movie you will go see at the cinema?>, <Question: What pet do you have?>]>
   ```
   
9. Créer une question via le shell :
    ```
    >>> question = Question(question_text="Do you work full time at office?", pub_date=timezone.now())
    >>> question.save()
    >>> Question.objects.all()
    <QuerySet [<Question: What's up?>, <Question: What is the next movie you will go see at the cinema?>, <Question: Which programming language do you prefer?>, <Question: What pet do you have?>, <Question: What is your favorite framework?>, <Question: Which framework would you like to learn to use?>, <Question: Do you work full time at office?>]>
   ```

10. Ajouter 3 choix à la question créée :
    ```
    >>> question.choice_set.all()
    <QuerySet []>
    >>> question.choice_set.create(choice_text="Totally", votes=0)
    <Choice: Totally>
    >>> question.choice_set.create(choice_text="Partially", votes=0)
    <Choice: Partially>
    >>> question.choice_set.create(choice_text="Nope", votes=0)      
    <Choice: Nope>
    >>> question.choice_set.all()                                    
    <QuerySet [<Choice: Totally>, <Choice: Partially>, <Choice: Nope>]>
    >>>
    ```

11. Lister les questions publiées récemment :
    ```
    >>> question.choice_set.all()                                    
    <QuerySet [<Choice: Totally>, <Choice: Partially>, <Choice: Nope>]>
    >>> questions = Question.objects.all()
    >>> for question in questions:
    ...     if question.was_published_recently:
    ...             print(question)
    ...
    What's up?
    What is the next movie you will go see at the cinema?
    Which programming language do you prefer?
    What pet do you have?
    What is your favorite framework?
    Which framework would you like to learn to use?
    Do you work full time at office?
    >>>
    ```

### Part three

Modification des vues puis ajout des templates index et detail

### Part Four

Ajout d'un formulaire simple et modifications des vues en vue génériques

#### Exos part 3 and 4
1. Ajout de la date de publication dans index.html :
    ```
   <span>{{question.pub_date}}</span>
   ```

2. Ajout de la page all qui liste tous les sondages :
    Ajout d'un template all.html puis modification de l'index.html. 
    Ajout d'une view AllView et modification des urls. 
    ```
    {% if latest_question_list %}
    <table>
        <thead>
            <tr>
                <th>Id</th>
                <th>Question</th>
            </tr>
        </thead>
        <tbody>
            {% for question in latest_question_list %}
                <tr>
                    <td>{{ question.id }}</td>
                    <td>
                        <a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}
    ```

3. Modifier all.html pour inclure un template frequency :
    Ajout d'un template frequency.html et d'une vue générique FrequencyView puis ajout de l'url.
    Modification de la méthode get_choices() pour gérer le cas où le total est égale à 0.
   ```
    class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_choices"] = self.object.get_choices()
        return context
    ```
    ```
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
    ```
    ```
    {% if has_choices %}
    <table>
        <thead>
            <tr>
                <th>Choix</th>
                <th>Nombre de votes</th>
                <th>Fréquence de votes</th>
            </tr>
        </thead>
        <tbody>
            {% for choice in has_choices %}
                <tr>
                    <td>{{choice.0}}</td>
                    <td>{{choice.1}}</td>
                    <td>{{choice.2|floatformat:0}} %</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
        <p>Pas de résultats</p>
    {% endif %}
    ```

4. Ajout d'une page statistics :
    nouvelle vue statistics
    ```
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
   ```
   
   Ajout dans index.html
   ```
   <a href="{% url 'polls:statistics' %}">Statistiques</a>
   ```
   
   statistics.html
   ```
   <table>
    <thead>
        <tr>
            <th>Nombre total de sondage</th>
            <th>Nombre total de choix</th>
            <th>Nombre total de votes</th>
            <th>Moyenne de votes</th>
            <th>Dernière question enregistrée</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{{ total_questions }}</td>
            <td>{{ total_choices }}</td>
            <td>{{ total_votes.votes__sum }}</td>
            <td>{{ avg_votes.votes__avg }}</td>
            <td>{{ last_question_recorded.question_text }}</td>

        </tr>
    </tbody>
    </table>
   ```
   Ajout de l'url dans polls.url.py
   ```
   path("statistics/", views.statistics, name="statistics"),
   ```

5. Ajout d'un formulaire pour ajouter une question :
    ```
   from django import forms


    class PollForm(forms.Form):
    question_text = forms.CharField(label="Question", max_length=100)

   ```
   ```
   <form action="{% url 'polls:add' %}" method="post">
    {% csrf_token %}
    <div class="fieldWrapper">
        {{ form.question_text.errors }}
        {{ form.question_text.label_tag }}
        {{ form.question_text }}
    </div>
   </form>
   ```
   ```
   def get_question(request):
    if request.method == "POST":
        form = PollForm(request.POST)

        if form.is_valid():
            question_text = form.cleaned_data["question_text"]

            new_question = Question(question_text=question_text, pub_date=timezone.now())
            new_question.save()
            

            return HttpResponseRedirect(reverse("polls:all"))

    else:
        form = PollForm()

    return render(request, "polls/poll_form.html", {"form": form})
   ```

6. Ajout des choix pour la question créée via le formulaire :
    ```
   def get_question(request):
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
   ```
   ```
   <form action="{% url 'polls:add' %}" method="post">
      {% csrf_token %}
      <div class="fieldWrapper">
        {{ form.question_text.errors }}
        {{ form.question_text.label_tag }}
        {{ form.question_text }}
      </div>
      <div class="fieldWrapper">
        <label for="choice1">Choix 1:</label>
        <input type="text" name="choice_text[]" id="choice1">
      </div>
      <div class="fieldWrapper">
        <label for="choice2">Choix 2:</label>
        <input type="text" name="choice_text[]" id="choice2">
      </div>
      <div class="fieldWrapper">
        <label for="choice3">Choix 3:</label>
        <input type="text" name="choice_text[]" id="choice3">
      </div>
      <div class="fieldWrapper">
        <label for="choice4">Choix 4:</label>
        <input type="text" name="choice_text[]" id="choice4">
      </div>
      <div class="fieldWrapper">
        <label for="choice4">Choix 5:</label>
        <input type="text" name="choice_text[]" id="choice5">
      </div>
      <input type="submit" value="Add">
    </form>
   ```

### Part five

Ajout des tests unitaires dans l'application

### Part six

Ajout du style dans la page d'index

### Part seven

Personnalisation du formulaire d'administration pour les questions

### Part eight

Ajout de Django Debug Toolbar

## Complement

### Héritage de gabarits

Ajout de base.html dans un répertoire templates à la racine du projet
```
<!DOCTYPE html>
<html lang="en">
<head>
    {% load static %}
    <link rel="stylesheet" href="{% static 'polls/style.css' %}">
    <title>{% block title %}Bienvenue sur mon site{% endblock %}</title>
</head>

<body>
    <header>
        {% block header %}{% endblock %}
    </header>

    <main id="content">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

Ajout des balises dans chaque templates
```
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <div class="poll_container">
        <h1>Bienvenue sur mon application de sondage</h1>

        <a href="{% url 'polls:all' %}">Questions</a>
        <a href="{% url 'polls:statistics' %}">Statistiques</a>
        <a href="{% url 'polls:add' %}">Créer un sondage</a>
    </div>
{% endblock %}
```
### Authentication

Ajout d'un template de login
```
{% extends 'base.html' %}

{% block title %}login{% endblock %}

{% block header %}<h1>Connexion :</h1>{% endblock %}

{% block content %}

<form action="{% url 'polls:login' %}" method="post">
    {% csrf_token %}
    <div>
        <label for="username">Nom d'utilisateur :</label>
        <input type="text" name="username" id="username" required>
    </div>
    <div>
        <label for="password">Mot de passe :</label>
        <input type="text" name="password" id="password" required>
    </div>
    <button type="submit">Connexion</button>
</form>
{% if error_message %}
<span>{{ error_message }}</span>
{% endif %}
{% endblock %}
```

Ajout des vues login et logout
```
def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            print(f"Utilisateur trouvé : {user}")
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("polls:index"))
            else:
                return render(request, "authenticate/login.html", {"error_message": "You didn't enter a valid username or password"})

    return render(request, "authenticate/login.html")


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("polls:index"))
```

Dans polls/urls.py
```
path("account/", views.log_in, name="login"),
path("logout/", views.log_out, name="logout")
```

Dans settings.py
```
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
```

Dans base.html
```
<header>
        {% block header %}{% endblock %}
        {% if user.is_authenticated %}
            <span>Hi, {{ user.username }}</span>
            <button>
                <a href="{% url 'polls:logout' %}">Déconnexion</a>
            </button>
        {% else %}
            <a href="{% url 'polls:login' %}">Connexion</a>
        {% endif %}
</header>
```

Pour restreindre une vue à un utilisateur connecté
```
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:login"))
```

### Register

Ajout d'un template register.html
```
{% extends 'base.html' %}

{% block title %}Inscription{% endblock %}

{% block content %}
<h2>S'enregistrer</h2>

<form method="post">
    {% csrf_token %}
    {{ form }}
    <button type="submit">S'incrire</button>
</form>
{% endblock %}
```

Ajout d'une vue RegisterView
```
class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("polls:index")
    template_name = "authenticate/register.html"
```

Dans login.html
```
<div>
    <span>Pas de compte</span>
    <a href="{% url 'polls:register' %}">S'enregister</a>
</div>
```

Dans polls/urls.py
```
path("register/", views.RegisterView.as_view(), name="register"),
```
