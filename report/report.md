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
   1. tous les attributs des classes sont visibles.
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


            