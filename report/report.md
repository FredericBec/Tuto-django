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
    ...     print(question)                     
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
            