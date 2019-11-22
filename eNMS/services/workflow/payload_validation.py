from sqlalchemy import ForeignKey, Integer
from wtforms import HiddenField, StringField

from eNMS.database.dialect import Column, SmallString
from eNMS.forms.automation import ServiceForm
from eNMS.models.automation import Service


class PayloadValidationService(Service):

    __tablename__ = "payload_validation_service"
    pretty_name = "Payload Validation"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    query = Column(SmallString)

    __mapper_args__ = {"polymorphic_identity": "payload_validation_service"}

    def job(self, run, payload, device=None):
        return {"query": run.query, "result": run.eval(run.query, **locals())}


class PayloadValidationForm(ServiceForm):
    form_type = HiddenField(default="payload_validation_service")
    query = StringField("Python Query")
    query_fields = ServiceForm.query_fields + ["query"]
