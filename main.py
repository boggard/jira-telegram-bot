import logging
from setproctitle import setproctitle

from telegram.ext import CommandHandler, Updater

from config import LOG_ERROR_FILE, PROC_TITLE, PROXY_URL, TOKEN
from model import init_database
from service import chat_service


def main():
    setproctitle(PROC_TITLE)
    logging.basicConfig(filename=LOG_ERROR_FILE, level=logging.ERROR)

    request_keys = {"proxy_url": PROXY_URL}
    updater = Updater(TOKEN, request_kwargs=request_keys)

    init_database()
    chat_service.init_bot(updater.job_queue)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("set", chat_service.set_user,
                                  pass_args=True,
                                  pass_job_queue=True))
    dp.add_handler(CommandHandler("help", chat_service.help_command))
    dp.add_handler(CommandHandler("me", chat_service.my_id_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
