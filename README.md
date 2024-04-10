# Social-Network-Project
This document describes a social network project similar to Instagram, developed with the following technologies:

+ **Frontend:** HTML, CSS, JS, Django
+ **Backend:** Python, FastAPI
+ **Database:** PostgreSQL

## Features:

+ **Registration and Login:** Users will be able to create accounts and access the application with a username and password.
+ **Password Recovery:** Users will be able to recover their password in case they forget it.
+ **User Profile:** Users will be able to view and edit their profile, including profile picture, name, biography, etc.
+ **Posts:** Users will be able to share photos and videos with their friends and followers.
+ **Reactions:** Users will be able to react to posts with different emojis.
+ **Comments:** Users will be able to comment on other users' posts.
+ **Followers:** Users will be able to follow other users to see their posts.
+ **Search:** Users will be able to search for other users by name or username.

## Architecture:

The project will be implemented as a monolith with the following components:

+ **Web Server:** Apache or Nginx will serve the frontend static files and redirect requests to the Django application.
+ **Django Application:** It will handle the user interface requests and interact with the FastAPI API.
+ **FastAPI API:** It will export CRUD functionalities for users, posts, comments, etc. in JSON format.
+ **PostgreSQL Database:** It will store all the information of the social network, such as users, posts, comments, relationships between users, etc.
