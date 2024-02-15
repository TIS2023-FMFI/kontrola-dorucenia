import os
from imbox import Imbox
import traceback
import datetime
from datetime import date
from .config import get_env

download_folder = 'website\\attachments'

def download_attachments():
    
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder, exist_ok=True)

    for filename in os.listdir(download_folder):
        try:
            os.remove(f"{download_folder}\\{filename}")
        except:
            pass
        
    mail = Imbox(get_env("MAIL_SERVER"), username=get_env("MAIL_USERNAME"), password=get_env("MAIL_PASSWORD"), ssl=True, ssl_context=None, starttls=False)
    today = date.today()
    messages = mail.messages(date__on=datetime.date(today.year, today.month, today.day))

    for (uid, message) in messages:
        mail.mark_seen(uid)

        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}\\{att_fn}"

                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            except:
                print(traceback.print_exc())

    mail.logout()
