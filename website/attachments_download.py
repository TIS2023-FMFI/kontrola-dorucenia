import os
from imbox import Imbox
import traceback
import datetime
from datetime import date

download_folder = 'attachments'

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)

for filename in os.listdir(download_folder):
    if os.path.isfile(os.path.join(download_folder, filename)):
        os.remove(os.path.join(download_folder, filename))
    
mail = Imbox("mail.webglobe.sk", username="ovl-kontrola-dorucenia@gefcoslovakia.sk", password="FbI;y@c0s2c=GX", ssl=True, ssl_context=None, starttls=False)
today = date.today()
messages = mail.messages(date__on=datetime.date(today.year, today.month, today.day))

for (uid, message) in messages:
    mail.mark_seen(uid)

    for idx, attachment in enumerate(message.attachments):
        try:
            att_fn = attachment.get('filename')
            download_path = f"{download_folder}/{att_fn}"

            with open(download_path, "wb") as fp:
                fp.write(attachment.get('content').read())
        except:
            print(traceback.print_exc())

mail.logout()
