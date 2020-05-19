"""Realizing telegram bot that can tell you info about current state of COVID-19."""
# other libraries
import logging
import country_converter as coco
# telegram imports
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardRemove, ParseMode
# our modules
from build_plot import create_plot
from country import Country

#         GLOBAL VARIABLES
# ==========================================
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

COLLECTING_DATA = {}
# ==========================================

#          LOGGING
# ==========================================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# ==========================================

#     OTHER CODE
# ==========================================
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi! My name is CORBOT and I'll help you to track COVID-19.\n"
                              "Enter /help to learn about my features.\n",
                              reply_markup=ReplyKeyboardRemove())


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("/plot - comparative statistics "
                              "of the two countries on the number of new patients.\n"
                              "/deaths - the number of deaths "
                              "from the coronavirus in the selected country at the moment.\n"
                              "/confirmed - the number of confirmed patients "
                              "from the coronavirus in the selected country at the moment.\n"
                              "/recovered - the number of recovered people "
                              "from the coronavirus in the selected country at the moment.\n"
                              "/country_total - displays general statistics "
                               "of the country at the moment.\n"
                              "/reference - receiving a daily subscription "
                              "to information about coronavirus.\n"
                              "/del_reference - to stop using subscription.\n"
                              "/add_country - adds country to your subscription.\n"
                              "/del_country - deletes country from your subscription.\n",
                              reply_markup=ReplyKeyboardRemove())


def wrong(update, context):
    """Working when user prints wrong command."""
    update.message.reply_text("Invalid input. Enter some command to start."
                              "\nTo learn about commands enter /help")


def cancel(update, context):
    """Cancels user's command"""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Thanks for using our bot!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def get_all_stats(country):
    """
    :param country: the name of the country
    :return: statistics about the coronavirus in country
    """
    CC = coco.CountryConverter()
    output = f"==== {country} ====\n"
    try:
        if country.lower() == 'usa':
            country = 'United states'
        country_data = Country(CC.convert(country, to='ISO2'))
    except ValueError:
        output += 'Such a name does not exist\n'
        return output

    date = str(country_data.df['Confirmed'].index[-1])[:-15]

    output += f"Confirmed cases: <b>{country_data.df['Confirmed'].iloc[-1]}" \
              f"</b>;\n"
    output += f"Recovered: <b>{country_data.df['Recovered'].iloc[-1]}</b>;\n"
    output += f"Deaths: <b>{country_data.df['Deaths'].iloc[-1]}</b>;\n"
    output += f"<i>Date: {date}</i>\n"
    return output


def choice(update, context):
    """Accepts the name of the country."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Enter the name of the country (in English)')
    return TYPING_REPLY


#           Block for PLOT
# ===========================================
def plot_choice(update, context):
    """Accepts names of two countries."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Enter the names of the two countries '
        'with a comma to get a graph '
        '(example: Ukraine;Spain)\nTo exit print /cancel')
    return TYPING_REPLY


def get_plot(update, context):
    """Creates plot and sends it to the user."""
    CC = coco.CountryConverter()
    text = update.message.text.split(';')
    for i in text:
        try:
            if i.lower() == 'usa':
                i = 'United states'
            Country(CC.convert(i, to='ISO2'))
        except ValueError:
            update.message.reply_text(f'Such a name does not exist - {i}.\n'
                                      f'Please try again.')
            return ConversationHandler.END
    if len(text) == 1:
        update.message.reply_text('Please, enter two countries!')
    else:
        create_plot(text[0], text[1])

        chat_id = update.message.chat_id
        context.bot.send_photo(chat_id=chat_id,
                               photo=open('telegram_plot_data/plot_png.png',
                                          'rb'))
    return ConversationHandler.END
# ===========================================


#           Block for DEATHS
# ===========================================
def deaths(update, context):
    """:return: the info about deaths in country to user."""
    message = update.message.text
    CC = coco.CountryConverter()
    try:
        if message.lower() == 'usa':
            message = 'United states'
        country = Country(CC.convert(message, to='ISO2'))
    except ValueError:
        update.message.reply_text('Such a name does not exist')
        return ConversationHandler.END
    date = str(country.df['Deaths'].index[-1])[:-15]
    update.message.reply_text(f"Deaths: {country.df['Deaths'].iloc[-1]}"
                              f"\nDate: {date}")
    return ConversationHandler.END


# ===========================================


#         Block for CONFIRMED ILL
# ===========================================
def confirmed(update, context):
    """:return: the info about confirmed cases
    (patients) in country to user."""
    message = update.message.text
    CC = coco.CountryConverter()
    try:
        if message.lower() == 'usa':
            message = 'United states'
        country = Country(CC.convert(message, to='ISO2'))
    except ValueError:
        update.message.reply_text('Such a name does not exist')
        return ConversationHandler.END
    date = str(country.df['Confirmed'].index[-1])[:-15]
    update.message.reply_text(f"Confirmed cases: "
                              f"{country.df['Confirmed'].iloc[-1]}"
                              f"\nDate: {date}")
    return ConversationHandler.END


# ===========================================

#         Block for RECOVERED
# ===========================================
def recovered(update, context):
    """:return: the info about recovered people in country to user."""
    message = update.message.text
    CC = coco.CountryConverter()
    try:
        if message.lower() == 'usa':
            message = 'United states'
        country = Country(CC.convert(message, to='ISO2'))
    except ValueError:
        update.message.reply_text('Such a name does not exist')
        return ConversationHandler.END
    date = str(country.df['Recovered'].index[-1])[:-15]
    update.message.reply_text(f"Recovered: {country.df['Recovered'].iloc[-1]}"
                              f"\nDate: {date}")
    return ConversationHandler.END


# ===========================================

#         Block for COUNTRY TOTAL
# ===========================================
def get_country_total(update, context):
    """:return: the all info about coronavirus in country to user."""
    message = update.message.text
    text = get_all_stats(message)
    update.message.reply_text(text, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


# ===========================================

#     Block for REFERENCE
# ===========================================
def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id

    CC = coco.CountryConverter()
    global COLLECTING_DATA

    message = update.message.text

    if message == '/cancel':
        update.message.reply_text('You have canceled the input!')
        return ConversationHandler.END
    try:
        if message.lower() == 'usa':
            message = 'United states'
        Country(CC.convert(message, to='ISO2'))
    except ValueError:
        update.message.reply_text('Such a name does not exist')
        return ConversationHandler.END
    try:
        if message in COLLECTING_DATA[chat_id]:
            update.message.reply_text('You have already '
                                      'selected this country!')
        else:
            COLLECTING_DATA[chat_id].append(message)
    except KeyError:
        COLLECTING_DATA[chat_id] = [message]

    try:
        due = 1440
        # Add job to queue and stop current one if there is a timer already
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_repeating(alarm,
                                                  interval=due,
                                                  context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text('Daily reference was already set!')

    except (IndexError, ValueError):
        update.message.reply_text('Error, please try again!')

    update.message.reply_text(get_all_stats(message), parse_mode=ParseMode.HTML)
    update.message.reply_text('You can add another country.\n'
                              'But if you wont to stop, enter, /cancel')


def alarm(context):
    """Sends the message about coronavirus."""
    global COLLECTING_DATA
    job = context.job
    chat_id = context.job.context
    text = ""
    for country in COLLECTING_DATA[chat_id]:
        text += get_all_stats(country)
    context.bot.send_message(job.context,
                             text=text,
                             parse_mode=ParseMode.HTML)


def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no daily references!')
        return

    chat_id = update.message.chat_id
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    if chat_id in COLLECTING_DATA:
        del COLLECTING_DATA[chat_id]
    update.message.reply_text('Timer successfully unset!')


def add_country(update, context):
    """Adds country to job queue."""
    CC = coco.CountryConverter()
    global COLLECTING_DATA
    chat_id = update.message.chat_id
    message = update.message.text

    try:
        if message.lower() == 'usa':
            message = 'United states'
        Country(CC.convert(message, to='ISO2'))
    except ValueError:
        update.message.reply_text('Such a name does not exist')
        return ConversationHandler.END

    try:
        if message in COLLECTING_DATA[chat_id]:
            update.message.reply_text('You have already '
                                      'selected this country!')
        else:
            COLLECTING_DATA[chat_id].append(message)
    except KeyError:
        COLLECTING_DATA[chat_id] = [message]

    text = 'You have added a country!\nYour current list of countries:\n'
    for country in COLLECTING_DATA[chat_id]:
        text += country + ', '
    text = text[:-2] + '.'

    update.message.reply_text(text)
    return ConversationHandler.END


def del_country(update, context):
    """Deletes country from job queue"""
    global COLLECTING_DATA
    chat_id = update.message.chat_id
    message = update.message.text

    try:
        if message in COLLECTING_DATA[chat_id]:
            COLLECTING_DATA[chat_id].remove(message)
        else:
            update.message.reply_text(f'There is no country '
                                      f'on your list named {message}!')
            return ConversationHandler.END
    except ValueError:
        update.message.reply_text(f'There is no country '
                                  f'on your list named {message}!')
        return ConversationHandler.END
    except KeyError:
        update.message.reply_text(f'Please, first of all, add country by /reference!')
        return ConversationHandler.END

    if len(COLLECTING_DATA[chat_id]) == 0:
        update.message.reply_text(f'Now you have no '
                                  f'countries on your list at all!')
        unset(update, context)
    else:
        text = 'You have deleted a country!\nYour ' \
               'current list of countries:\n'
        for country in COLLECTING_DATA[chat_id]:
            text += country + ', '
        text = text[:-2] + '.'
        update.message.reply_text(text)
    return ConversationHandler.END


# ===========================================

def main():
    """Main function for realizing a telegram bot."""
    updater = Updater(token='TOKEN_HERE',
                      use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # ===========================================
    plot_handler = ConversationHandler(
        entry_points=[CommandHandler('plot', plot_choice)],

        states={
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          get_plot)
                           ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(plot_handler)
    # ===========================================
    deaths_handler = ConversationHandler(
        entry_points=[CommandHandler('deaths', choice)],

        states={
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          deaths)
                           ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(deaths_handler)
    # ===========================================
    confirmed_handler = ConversationHandler(
        entry_points=[CommandHandler('confirmed', choice)],

        states={
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          confirmed)
                           ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(confirmed_handler)
    # ===========================================
    recovered_handler = ConversationHandler(
        entry_points=[CommandHandler('recovered', choice)],

        states={
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          recovered)
                           ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(recovered_handler)
    # ===========================================
    country_total_handler = ConversationHandler(
        entry_points=[CommandHandler('country_total', choice)],

        states={
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          get_country_total)
                           ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(country_total_handler)
    # ===========================================
    reference_handler = ConversationHandler(
        entry_points=[CommandHandler('reference', choice)],

        states={
            TYPING_REPLY: [MessageHandler(Filters.text, set_timer,
                                          pass_job_queue=True,
                                          pass_chat_data=True)
                           ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(reference_handler)
    dispatcher.add_handler(CommandHandler("del_reference", unset, pass_chat_data=True))
    # ===========================================
    add_country_handler = ConversationHandler(
        entry_points=[CommandHandler('add_country', choice)],
        states={TYPING_REPLY: [MessageHandler(Filters.text, add_country)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(add_country_handler)
    # ===========================================
    del_country_handler = ConversationHandler(
        entry_points=[CommandHandler('del_country', choice)],
        states={TYPING_REPLY: [MessageHandler(Filters.text, del_country)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(del_country_handler)
    # ===========================================
    dispatcher.add_handler(MessageHandler(Filters.text, wrong))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
