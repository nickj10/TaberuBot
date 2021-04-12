Taberu Bot es un chatbot que nos ayudará a encontrar recetas.
Está realizado con Python 3.8
El entorno necesita las librerias: login, Telegram, decouple, json, requests

El bot únicamente reconoce como idioma el inglés.

Preparacion del proyecto:
1. Señalar la carpeta src (click derecho) y marcar directorio como Source Root
2. Click derecho en el archivo bot.py y "Run bot"
3. Abrir telegram
4. Buscar el usuario @the_tarebu_bot
5. Hablar con el bot según instruciones y funcionalidades

Instrucciones de uso:
-Una frase por mensaje
-Solo frases enunciativas (nada de preguntas, la gramática no lo soporta), 1 verbo por frase

Funcionalidades:
-Pedir receta aleatoria (Ej: I want a random recipe, I need a recipe, Send me a aleatory recipe...)
-Pedir receta según categoría (árabe, española, francesa) (Ej: I want a italian recipe...)
-Pedir receta según clase (sopa, ensalada, ...) (Ej: I want a drink recipe...)
-Pedir receta según ingredientes (actualmente solo 1 ingrediente) (Ej: I want a recipe with eggs, ...)

En keywords.txt están los verbos, ingredientes, clases de comida, ... que acepta el bot
