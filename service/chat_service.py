from model.chat import Chat
from model.user import User
from telegram.ext import JobQueue
from telegram import ParseMode
from service import jira_service
from utils.markdown import markdown_prepare
from utils import date_util


def init_bot(job_queue: JobQueue):
    for chat in Chat.select(Chat):
        add_job(job_queue, chat)


def set_user(bot, update, args, job_queue: JobQueue, chat_data):
    user = User.get_or_create(name=args[0])[0]

    t_id = update.message.chat_id

    chats = Chat.select().where(Chat.t_id == t_id)
    if len(chats) > 0:
        chat = chats[0]
        chat.user = user
        chat.save()
    else:
        chat = Chat.create(t_id=t_id, user=user)

    jira_service.init_user_issues(user)

    add_job(job_queue, chat)

    update.message.reply_text('You will get issues notifications from user: ' + user.name)


def send_issue(bot, job):
    chat = job.context
    for issue in jira_service.get_new_issues(username=chat.user.name):
        text = "*Project*: " + markdown_prepare(issue.project_name) + "\n" + \
               "*Issue*: [" + markdown_prepare(issue.alias) + "]" + "(" + markdown_prepare(issue.link) + ")" + \
               (" *was created* on *" + issue.created + "*" if issue.created == issue.updated
                else " *was updated* on *" + issue.updated + "*") + "\n" + \
               "*Components*: " + markdown_prepare(issue.components) + "\n" + \
               "*Status*: " + markdown_prepare(issue.status) + "\n" + \
               "*Author*: " + markdown_prepare(issue.author) + "\n" + \
               "*Assignee*: " + markdown_prepare(issue.assignee) + "\n" + \
               "*Caption*: " + markdown_prepare(issue.caption) + "\n" + \
               "*Description*: " + markdown_prepare(issue.description) + "\n"

        bot.send_message(chat_id=chat.t_id, text=text, parse_mode=ParseMode.MARKDOWN)


def add_job(job_queue: JobQueue, chat: Chat):
    jobs = job_queue.jobs()
    for job in [job for job in jobs if job.context.id == chat.id]:
        job.enabled = False
        job.schedule_removal()

    job_queue.run_repeating(send_issue, 5, context=chat)
