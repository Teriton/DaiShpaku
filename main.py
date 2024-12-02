import databaseManager as dbm
import design as dn

from pathlib import Path

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)

# REGISTERING FORM --------------------------------------------------------------------------------

START,ENTERING_NAME, ENTER_GENDER, ENTERING_BIO, ENTERING_PHOTO = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message.from_user.username == None):
        await update.message.reply_text(
        "Не указано имя полязователя в настройках профиля."
    )
        return START
    
    if dbm.check_user(update.message.from_user.username):
        await update.message.reply_text(
        "Тебя еще не поимел Шпэк?! Время исправить"
    )
        await update.message.reply_text(
        "Введите ваше имя"
    )
        return ENTERING_NAME
    else:
        await main_menu(update, context)
        return ConversationHandler.END

async def entering_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(update.message.text) > 20:
        await update.message.reply_text("Я конечно не осуждаю твое имя, но чет оно слишком долгое, лимит 20 символов, попробуй еще раз")
        return ENTERING_NAME
    dbm.add_user(update.message.text,"",update.message.from_user.username,"")
    reply_keyboard = [["Мужчина", "Женщина"]]
    await update.message.reply_text("Дай знать шпэку кто ты", reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,input_field_placeholder="Мужчина или Женщина?"))
    return ENTER_GENDER

async def entering_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message.text == "Мужчина"):
        dbm.update_gender(update.message.from_user.username,'M')
    if (update.message.text == "Женщина"):
        dbm.update_gender(update.message.from_user.username,'F')
    await update.message.reply_text("Раскажи что нибудь о себе Шпэку")
    return ENTERING_BIO

async def entering_bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(update.message.text) > 100:
        await update.message.reply_text("Внушительно, однако давай уложимся в 100 символов")
        return ENTERING_BIO
    dbm.update_bio(update.message.from_user.username,update.message.text)
    await update.message.reply_text("Скидывай свою фоточку, если не хочешь можно /cancel прописать")
    return ENTERING_PHOTO

async def entering_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    file = await update.message.photo[len(update.message.photo)-1].get_file()
    await file.download_to_drive("./photos/{}.jpg".format(update.message.from_user.username))
    await main_menu(update,context)
    return ConversationHandler.END

# update.message.reply_photo("./photos/{}.jpg".format(update.message.from_user.username), "Узнал себя?")
# MAIN MENU --------------------------------------------------------------------------------

SEARCH, INTERESTED, CHANGE = range(3)

async def send_profile(update:Update, context: ContextTypes.DEFAULT_TYPE, name, bio, current_user_id,reply_keyboard):
    current_user_name = dbm.get_tg_id_by_id(current_user_id)
    if Path("./photos/{}.jpg".format(current_user_name)).is_file():
        await update.message.reply_photo("./photos/{}.jpg".format(current_user_name), dn.formated_profile(name, bio),
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    else:
        await update.message.reply_text(dn.formated_profile(name, bio),
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name_of_state="Человек"
    if dbm.get_interested_in_gender_by_tg_id(update.message.from_user.username) == "M":
        name_of_state="мужчины"
    elif dbm.get_interested_in_gender_by_tg_id(update.message.from_user.username) == "F":
        name_of_state="женщины"
    elif dbm.get_interested_in_gender_by_tg_id(update.message.from_user.username) == "A":
        name_of_state="все живое"
    
    await update.message.reply_text("""Выберите фунцию:
/search - посмотреть на людей
режим поиска - {}
/interested - табой интересуется {} человек
/change - изменить режим поиска
/refresh - обновить данные
/settings - настройка порофиля
                                    """.format(name_of_state,len(dbm.get_list_interested_users(dbm.get_id_by_tg_id(update.message.from_user.username)))))
    
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    random_profile = dbm.get_random_user(dbm.get_interested_in_gender_by_tg_id(update.message.from_user.username))
    reply_keyboard = [["🚪","💘","🚫"]]
    if update.message.text == "💘":
        if dbm.check_upvote(dbm.get_id_by_tg_id(update.message.from_user.username),dbm.get_current_user_by_tg_id(update.message.from_user.username)) == 0:
            dbm.upvote(dbm.get_id_by_tg_id(update.message.from_user.username),dbm.get_current_user_by_tg_id(update.message.from_user.username))
    await send_profile(update,context,random_profile[0][2],random_profile[0][3],random_profile[0][0],reply_keyboard)
    # await update.message.reply_text(dn.formated_profile(random_profile[0][2], random_profile[0][3]),
    #                                 reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    dbm.update_current_user(update.message.from_user.username,random_profile[0][0])
    return SEARCH

async def interested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    interested_users = dbm.get_list_interested_users(dbm.get_id_by_tg_id(update.message.from_user.username))
    if len(interested_users) == 0:
        await update.message.reply_text("Прости, но ты никому не нужен(",)
        await main_menu(update, context)
        return ConversationHandler.END
    reply_keyboard = [["🚪","💘","🚫"]]
    if update.message.text == "💘":
        await update.message.reply_text(
            "Уху это match, время написать этому счастливчику @{}".format(
                dbm.get_tg_id_by_id(dbm.get_current_user_by_tg_id(update.message.from_user.username))
                )
            )
        dbm.delete_upvote(dbm.get_current_user_by_tg_id(update.message.from_user.username),dbm.get_id_by_tg_id(update.message.from_user.username))
    elif update.message.text == "🚫":
        dbm.delete_upvote(dbm.get_current_user_by_tg_id(update.message.from_user.username),dbm.get_id_by_tg_id(update.message.from_user.username))
        
    interested_users = dbm.get_list_interested_users(dbm.get_id_by_tg_id(update.message.from_user.username))
    if len(interested_users) == 0:
        await update.message.reply_text("Фанатов больше нет, смирись")
        await main_menu(update, context)
        return ConversationHandler.END
    
    await send_profile(update,context,interested_users[0][4],interested_users[0][5],interested_users[0][0],reply_keyboard)
    dbm.update_current_user(update.message.from_user.username,interested_users[0][0])
    return INTERESTED

async def change_interested(update:Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["♂️","♀️","⚧️"]]
    if update.message.text == "♂️":
        dbm.update_interested_in_gender(update.message.from_user.username, "M")
        await main_menu(update,context)
        return ConversationHandler.END
    elif update.message.text == "♀️":
        dbm.update_interested_in_gender(update.message.from_user.username, "F")
        await main_menu(update,context)
        return ConversationHandler.END
    elif update.message.text == "⚧️":
        dbm.update_interested_in_gender(update.message.from_user.username, "A")
        await main_menu(update,context)
        return ConversationHandler.END
    await update.message.reply_text("Кого ты уже подыскать собрался?",
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    return CHANGE

# SETTINGS --------------------------------------------------------------------------------

SETTINGS,NAME, BIO, PHOTO, GENDER = range(5)

async def void_settings(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Имя","Описание"],["Фото","Гендер"],["Выйти"]]
    await update.message.reply_text("Выбери какую пенетрацию мы проводима",
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    return SETTINGS

async def settings(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Имя","Описание"],["Фото","Гендер"],["Выйти"]]
    if update.message.text == "Имя":
        await update.message.reply_text("Каково твое имя?")
        return NAME
    elif update.message.text == "Описание":
        await update.message.reply_text("И теперь чем ты известен?")
        return BIO
    elif update.message.text == "Фото":
        await update.message.reply_text("Кидай фоточку мне в колекцию")
        return PHOTO
    elif update.message.text == "Гендер":
        reply_keyboard = [["Мужчина", "Женщина"]]
        await update.message.reply_text("КТО ТЫ ПО ГЕНДЕРУ!?",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True,input_field_placeholder="Мужчина или Женщина?"))
        return GENDER
    
    await update.message.reply_text("Выбери какую пенетрацию мы проводима",
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
    return SETTINGS

async def change_name(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(update.message.text) > 20:
        await update.message.reply_text("Я конечно не осуждаю твое имя, но чет оно слишком долгое, лимит 20 символов, попробуй еще раз")
        return NAME
    dbm.update_name(update.message.from_user.username,update.message.text)
    await void_settings(update,context)
    return SETTINGS

async def change_bio(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if len(update.message.text) > 100:
        await update.message.reply_text("Внушительно, однако давай уложимся в 100 символов")
        return BIO
    dbm.update_bio(update.message.from_user.username,update.message.text)
    await void_settings(update,context)
    return SETTINGS

async def change_gender(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if (update.message.text == "Мужчина"):
        dbm.update_gender(update.message.from_user.username,'M')
    if (update.message.text == "Женщина"):
        dbm.update_gender(update.message.from_user.username,'F')
    await void_settings(update,context)
    return SETTINGS

async def change_photo(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    file = await update.message.photo[len(update.message.photo)-1].get_file()
    await file.download_to_drive("./photos/{}.jpg".format(update.message.from_user.username))
    await void_settings(update,context)
    return SETTINGS

def main() -> None:
    application = Application.builder().token("7521993568:AAGbrKztgd-nj9hP4He3IlqIKWKwolRjix0").build()
    status = dbm.connect_to_database()
    if (status):
        print("Something went wrong with db.")
        return -1

    register_from_heandler = ConversationHandler(
        entry_points=[MessageHandler(filters.ALL, start),CommandHandler("start", start)],
        states={
            START: [CommandHandler("start", start)],
            ENTERING_NAME: [MessageHandler(filters.TEXT,entering_name)],
            ENTER_GENDER: [MessageHandler(filters.Regex("^(Мужчина|Женщина)$"),entering_gender)],
            ENTERING_BIO: [MessageHandler(filters.TEXT,entering_bio)],
            ENTERING_PHOTO: [MessageHandler(filters.PHOTO, entering_photo)]
        },
        fallbacks=[CommandHandler("cancel",start)]
    )
    main_menu_heandler = CommandHandler("refresh", main_menu)
    search_heandler = ConversationHandler(
        entry_points=[CommandHandler("search", search)],
        states={
            SEARCH: [MessageHandler(filters.Regex("^(🚫|💘)$"), search)],
        },
        fallbacks=[MessageHandler(filters.Regex("^(🚪)$"),start)]
    )

    interested_heandler = ConversationHandler(
        entry_points=[CommandHandler("interested", interested)],
        states={
            INTERESTED: [MessageHandler(filters.Regex("^(🚫|💘)$"), interested)],
        },
        fallbacks=[MessageHandler(filters.Regex("^(🚪)$"),start)]
    )

    change_interested_heandler = ConversationHandler(
        entry_points=[CommandHandler("change", change_interested)],
        states={
            CHANGE: [MessageHandler(filters.Regex("^(♂️|♀️|⚧️)$"), change_interested)],
        },
        fallbacks=[MessageHandler(filters.Regex("^(🚪)$"),start)]
    )

    settings_heandler = ConversationHandler(
        entry_points=[CommandHandler("settings", settings)],
        states={
            SETTINGS:[MessageHandler(filters.Regex("^(Имя|Описание|Фото|Гендер)$"), settings)],
            NAME: [MessageHandler(filters.ALL, change_name)],
            BIO: [MessageHandler(filters.ALL, change_bio)],
            GENDER: [MessageHandler(filters.Regex("^(Мужчина|Женщина)$"), change_gender)],
            PHOTO: [MessageHandler(filters.PHOTO, change_photo)]
        },
        fallbacks=[MessageHandler(filters.Regex("^(Выйти)$"),start)]
    )

    application.add_handler(settings_heandler)
    application.add_handler(search_heandler)
    application.add_handler(change_interested_heandler)
    application.add_handler(interested_heandler)
    application.add_handler(main_menu_heandler)
    application.add_handler(register_from_heandler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()