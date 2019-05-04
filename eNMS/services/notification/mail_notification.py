from flask_mail import Message
from sqlalchemy import Column, ForeignKey, Integer, String
from wtforms import HiddenField, StringField
from wtforms.widgets import TextArea

from eNMS.database import get_one
from eNMS.forms import metaform
from eNMS.forms.automation import ServiceForm
from eNMS.modules import mail_client
from eNMS.models import register_class
from eNMS.models.automation import Service


class MailNotificationService(Service, metaclass=register_class):

    __tablename__ = "MailNotificationService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    title = Column(String(255), default="")
    sender = Column(String(255), default="")
    recipients = Column(String(255), default="")
    body = Column(String(255), default="")

    __mapper_args__ = {"polymorphic_identity": "MailNotificationService"}

    def job(self, _) -> dict:
        parameters = get_one("Parameters")
        if self.recipients:
            recipients = self.recipients.split(",")
        else:
            recipients = parameters.mail_sender.split(",")
        sender = self.sender or parameters.mail_sender
        self.logs.append(f"Sending mail {self.title} to {sender}")
        message = Message(
            self.title, sender=sender, recipients=recipients, body=self.body
        )
        mail_client.send(message)
        return {"success": True, "result": str(message)}


class MailNotificationForm(ServiceForm, metaclass=metaform):
    form_type = HiddenField(default="MailNotificationService")
    title = StringField()
    sender = StringField()
    recipients = StringField()
    body = StringField(widget=TextArea(), render_kw={"rows": 5})