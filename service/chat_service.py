import logging
from datetime import datetime

from peewee import DoesNotExist
from telegram import ParseMode
from telegram.ext import JobQueue

from config import JIRA_REQUESTS_SECONDS_PERIOD
from model import Chat, Permission, User
from service import jira_service


def init_bot(job_queue: JobQueue):
    for chat in Chat.select(Chat):
        add_job(job_queue, chat)


def help_command(bot, update):
    bot.send_message(text="Use next commands to work with bot:" + "\n" +
                          "/set <username> - to setup user who's issues you "
                          "want to get" + "\n" +
                          "/me - to see your user_id",
                     chat_id=update.message.chat_id)


def my_id_command(bot, update):
    bot.send_message(
        text="Your userId - *{0}*".format(update.message.from_user.id),
        chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN)


def set_user(bot, update, args, job_queue: JobQueue):
    if update.message.from_user.id not in [p.t_id for p in
                                           Permission.select(Permission.t_id)]:
        update.message.reply_text(
            "You don't have permission to get issues from this jira-service")
        return

    user, _ = User.get_or_create(name=args[0])
    user.last_updated = datetime.now()
    user.save()

    t_id = update.message.chat_id

    try:
        chat = Chat.get(t_id=t_id)
    except DoesNotExist:
        chat = Chat.create(t_id=t_id)

    chat.user = user
    chat.save()

    add_job(job_queue, chat)

    update.message.reply_text(
        'You will get issues notifications from user: ' + user.name)


def send_issue(bot, job):
    chat = job.context
    chat_id = chat.t_id
    try:
        for issue in jira_service.get_new_issues(username=chat.user.name):
            bot.send_message(chat_id=chat_id, text=issue.get_info(),
                             parse_mode=ParseMode.MARKDOWN)
    except Exception:
        logging.exception(
            "{0}: Exception in sending issues to user with id:{1}".format(
                datetime.now(), chat_id))


def add_job(job_queue: JobQueue, chat: Chat):
    for job in job_queue.jobs():
        if job.context.id == chat.id:
            job.enabled = False
            job.schedule_removal()

    job_queue.run_repeating(send_issue, int(JIRA_REQUESTS_SECONDS_PERIOD),
                            context=chat)
