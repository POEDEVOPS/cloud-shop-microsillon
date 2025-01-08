# Présentation du projet

Générateur de sites de vente en ligne de musique d'un style donné (ex : vente d'albums de Rock uniquement).

# Technologies utilisées

## Coté applicatif

* Application web : html - css + framework bootstrap - vanilla js
* Application serveur : serveur node js avec module Express
* Persistence : BDD Postgresql

## Coté Devops

* Code : visual studio code
* Build : gitlab
* Integrate : docker image nodejs
* Test : postman - script python de test de création de la BDD
* Release : Kubernetes on premise
* Deploy : gitlab
* Operate : ELK

# Variables d'environnements GITLAB

Toutes les variables sont masquées complètement sauf mention contraire.

## Clés API DISCOGS

CONSUMER_KEY

CONSUMER_SECRET

ACCESS_KEY

ACCESS_TOKEN

## POSTGRESQL CREDENTIALS

POSTGRES_DB (visible)

POSTGRES_USER (visible)

POSTGRES_PASSWORD

## DEFAULT USERS PASSWORD 

USER_ADMIN_PW

USER_GUEST_PW

## SHOP DATA

SHOP_NAME (visible)

TOTAL_ALBUMS (visible)

MUSIC_STYLE (visible)




