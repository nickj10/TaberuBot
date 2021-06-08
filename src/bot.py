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
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Handler import ParserHandler, SpoonacularAPI, NLPHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# initialize MVC
parser = ParserHandler()
spoonacularAPI = SpoonacularAPI()
nlpHandler = NLPHandler()

#RESPONSES
CONTINUE_RESPONSES = ["Can I help you with something else? :)", "If you need anything else, do not hesitate to ask me", "Wow, I think it's an exquisite recipe , do you need anything else? ", "Bof, how hungry has I gotten, are we looking for something else?"]
INGREDIENTS_RESPONSES = ["Would you like to add any more ingredients?", "Do you think we can add any more ingredients to the recipe? ", "Have you forgotten an ingredient for your meal?" ]
ERROR_INGREDIENTS_RESPONSES = ["Well, I have not understood those ingredients, can you repeat? :)", "Is that an existing ingredient? Repeat please ", "I think that ingredient is not in my database, why not try again? " ]


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello, are you hungry? What do you have in your fridge?')


def help(update, context):
    """Send a message when the command /help is issued."""
    str = "What can this bot do? \nThis a bot that helps you find delicious recipes in a blink of an eye!\n\n " \
            + "Commands: \n" + "\t/start: to ask for a recipe.\n\t/info: to get to know about my developers."
    update.message.reply_text(str)

def info_command(update, context):
    """Send a message when the command /info is issued."""
    str = "Taberu Bot is an open source chatbot. It's free with an unlimited service, plus it will help you make delicious recipes!" \
        + "\n\nDevelopers:\nOmar Ntifi\nNicole Marie Jimenez\nKaye Ann Ignacio\n\n" \
        + "Leave them some feedback, they will be glad to hear from you!\nhttps://github.com/nickj10/TaberuBot"
    update.message.reply_text(str)

def executeUserRequest(function_id, args):
    if function_id == 0:
        return spoonacularAPI.getAPIRequestRandom()
    elif function_id == 1:
        return spoonacularAPI.getAPIRequestByIngredient(args)
    elif function_id == 2:
        return spoonacularAPI.getAPIRequestByCuisine(args)
    elif function_id == 3:
        return spoonacularAPI.getAPIRequestByClass(args)
    else:
        return None
def sendRecipe(update, context, recipe):
    if recipe == None:
        update.message.reply_text(nlpHandler.sendRandomNotUnderstandable())
    else:
        update.message.reply_text(constructRecipeString(recipe))
        update.message.reply_text(random.choice(CONTINUE_RESPONSES))

def analyzeUserInput(update, context):

    if nlpHandler.waiting_ing:
        extra_ings, add = nlpHandler.addMoreIngredients(update.message.text)
        if not extra_ings and add:
            update.message.reply_text(random.choice(ERROR_INGREDIENTS_RESPONSES))
            return
        nlpHandler.waiting_args = nlpHandler.waiting_args + extra_ings
        recipe = executeUserRequest(1, args=nlpHandler.waiting_args)
        nlpHandler.waiting_ing = False
        nlpHandler.waiting_args = ""
        sendRecipe(update, context, recipe)
        return

    tags_list, semantic_list, greeting = nlpHandler.analyzeText(update, context)
    if not tags_list and not semantic_list:
        return
    ok = False
    i = 0
    for tags in tags_list:
        args = []
        function_id = -1
        ok, function_id, args = parser.parse(tags, semantic_list[i])
        if ok:
            if function_id == 1:
                update.message.reply_text(random.choice(INGREDIENTS_RESPONSES))
                nlpHandler.waiting_ing = True
                nlpHandler.waiting_args = args
            else:
                recipe = executeUserRequest(function_id, args)
                sendRecipe(update, context, recipe)
        elif greeting:
            break
        else:
            update.message.reply_text(nlpHandler.sendRandomErrorMessage())
        i = i + 1




def constructRecipeString(recipe):
    h1 = "Here's a recipe that I can recommend: " + recipe.title + "\n"
    h2 = "\nIt can be prepared in " + str(recipe.readyInMinutes) + " minutes and for up to " + str(
        recipe.servings) + " servings!"
    bodyIng = "\n\nIngredients: \n"
    for ing in recipe.ingredients:
        bodyIng = bodyIng + "\t " + ing.name + " - " + str(ing.amount) + " " + str(ing.unit) + "\n"
    bodyLink = "\nHere's how you can prepare it: " + recipe.sourceUrl + "\n"
    return h1 + h2 + bodyIng + bodyLink


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
    dp.add_handler(CommandHandler("info", info_command))



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
