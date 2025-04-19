# Plateforme E-Learning

Une plateforme d'apprentissage en ligne moderne construite avec Django et Tailwind CSS, offrant des cours en ligne, un chatbot IA et des certificats de formation.

## Fonctionnalités

- Inscription et authentification des utilisateurs
- Gestion des cours et des modules
- Chatbot IA pour l'assistance aux étudiants
- Génération de certificats
- Interface utilisateur moderne avec Tailwind CSS
- Chat en temps réel avec WebSockets

## Prérequis

- Python 3.8 ou supérieur
- Redis (pour le chat en temps réel)
- Compte OpenAI (pour le chatbot IA)

## Installation

1. Clonez le dépôt :

```bash
git clone https://github.com/votre-username/e-learning.git
cd e-learning
```

2. Créez un environnement virtuel et activez-le :

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

4. Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```
DEBUG=True
SECRET_KEY=votre_secret_key_ici
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
OPENAI_API_KEY=votre_clé_api_openai
```

5. Appliquez les migrations :

```bash
python manage.py migrate
```

6. Créez un superutilisateur :

```bash
python manage.py createsuperuser
```

7. Lancez le serveur Redis :

```bash
redis-server
```

8. Dans un autre terminal, lancez le serveur de développement :

```bash
python manage.py runserver
```

## Structure du Projet

```
e-learning/
├── elearning/              # Configuration du projet
├── users/                  # Gestion des utilisateurs
├── courses/               # Gestion des cours
├── certificates/          # Gestion des certificats
├── chatbot/              # Chatbot IA
├── templates/            # Templates HTML
├── static/              # Fichiers statiques
└── media/              # Fichiers médias
```

## Utilisation

1. Accédez à l'interface d'administration à l'adresse `http://localhost:8000/admin/`
2. Créez des cours et des modules
3. Les utilisateurs peuvent s'inscrire et suivre les cours
4. Le chatbot IA est disponible pour répondre aux questions des étudiants
5. Les certificats sont générés automatiquement à la fin de chaque formation

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
