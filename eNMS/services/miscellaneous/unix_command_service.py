from subprocess import check_output
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from typing import Optional
from wtforms import HiddenField, StringField

from eNMS.forms import metaform
from eNMS.forms.automation import ServiceForm
from eNMS.forms.services import ValidationForm
from eNMS.models import register_class
from eNMS.models.automation import Service
from eNMS.models.inventory import Device


class UnixCommandService(Service, metaclass=register_class):

    __tablename__ = "UnixCommandService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    has_targets = True
    command = Column(String(255), default="")
    content_match = Column(String(255), default="")
    content_match_textarea = True
    content_match_regex = Column(Boolean, default=False)
    negative_logic = Column(Boolean, default=False)
    delete_spaces_before_matching = Column(Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "UnixCommandService"}

    def job(self, payload: dict, device: Optional[Device] = None) -> dict:
        command = self.sub(self.command, locals())
        match = self.sub(self.content_match, locals())
        self.logs.append(f"Running Unix command ({command}) on {device.name}")
        result = check_output(command.split()).decode()
        return {
            "success": self.match_content(result, match),
            "match": match,
            "negative_logic": self.negative_logic,
            "result": result,
        }


class UnixCommandForm(ServiceForm, ValidationForm, metaclass=metaform):
    form_type = HiddenField(default="UnixCommandService")
    command = StringField()