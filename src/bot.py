#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Handler import TokenHandler, TaberuManager, ParserHandler, SpoonacularAPI

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# initialize MVC
taberu = TaberuManager()
parser = ParserHandler(taberu)
tokenHandler = TokenHandler(taberu, parser)
spoonacularAPI = SpoonacularAPI()

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello, are you hungry? What do you have in your fridge?')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def analyzeUserInput(update, context):
    tokenHandler.tokenize(update, context)
    expressions = taberu.get_tokens()
    ingredients = []
    ingredients = taberu.get_values()
    cuisines = taberu.get_categories()
    types = taberu.get_classes()

    # run parser for each expression
    for expr in expressions:

        expr.append("final")
        parserOut = tokenHandler.parse_tokens(expr)

        logger.info("The parsed output is %s", parserOut)
        if parserOut == "bye":
            update.message.reply_text("Goodbye, see you soon!")
        elif parserOut == "hello":
                update.message.reply_text("How can I help you?")
        elif parserOut != "random" and parserOut != "ing" and parserOut != "category" and parserOut != "class":
            update.message.reply_text("I'm sorry, I didn't understand you. Can you put it another way? :) ")
        else:
            update.message.reply_text("Hold on for a second! Searching for recipes...")

            if parserOut == "random":
                recipe = spoonacularAPI.getAPIRequestRandom()

            if parserOut == "ing":
                recipe = spoonacularAPI.getAPIRequestByIngredient(ingredients[0][0])

            if parserOut == "category":
                recipe = spoonacularAPI.getAPIRequestByCuisine(cuisines[0][0])

            if parserOut == "class":
                recipe = spoonacularAPI.getAPIRequestByClass(types[0][0])

            update.message.reply_text(constructRecipeString(recipe))
            update.message.reply_text("Can I help you with something else? :)")



def constructRecipeString(recipe):
    h1 = "Here's a recipe that I can recommend: " + recipe.title + "\n"
    h2 = "\nIt can be prepared in " + str(recipe.readyInMinutes) + " minutes and for up to " + str(recipe.servings) + " servings!"
    bodyIng = "\n\nIngredients: \n"
    for ing in recipe.ingredients:
        bodyIng = bodyIng + "\t " + ing.name + " - " + str(ing.amount) + " " + str(ing.unit) + "\n"
    bodyLink = "\nHere's how you can prepare it: " + recipe.sourceUrl + "\n"
    return h1+h2+bodyIng+bodyLink


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1600098372:AAHN-67ALQ6kXDYLQDxBIsDMKctyeZtBVts", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # initialize keywords
    tokenHandler.parse_keywords()

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, analyzeUserInput))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
