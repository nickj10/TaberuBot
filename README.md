# Taberu Bot

## Descripción
Taberu Bot es un chatbot que nos ayudará a encontrar recetas.
Se ha desarrollado con Python 3.8. El entorno necesita las siguientes librerias:
* Telegram API
* login
*  json
*  requests
*  decouple
* nltk

Para instalar las dependencias, el proyecto dispone de un Pipfile para instalarlas con pipenv.

## Limitaciones
El bot únicamente reconoce como idioma el inglés. Sigue las instrucciones que se explicará más adelante.

## Preparacion del proyecto
Se recomienda usar una IDE como PyCharm.

1. Señalar la carpeta src (click derecho) y marcar directorio como **Source Root**.
2. Click derecho en el archivo bot.py y sobre la función main, selecciona "Run bot"
3. Abrir Telegram
4. Buscar el usuario @the_taberu_bot
5. Hablar con el bot según instruciones y funcionalidades

## Funcionalidades
* Pedir receta aleatoria (Ej: I want a random recipe, I need a recipe, Send me a aleatory recipe...)
* Pedir receta según categoría (árabe, española, francesa) (Ej: I want a italian recipe...)
* Pedir receta según clase (sopa, ensalada, ...) (Ej: I want a drink recipe...)
* Pedir receta según ingredientes (1 o más ingredientes) (Ej: I want a recipe with eggs, ...)

## Script ejemplo:
* Hello Taberubot!
* I want a random recipe
* Recommend me another aleatory recipe
* I dont like it recommend me something else
* Ok now give me an spanish recipe
* Thinking about it better send me a recipe with pork
* Thank you very much now I need a dessert recipe
* What can I eat for lunch?
* What are you doing?
* Oh yes almost forgot I want a drink recipe
* No thank u goodbye
