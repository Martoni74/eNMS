from sqlalchemy import Boolean, ForeignKey, Integer
from wtforms import BooleanField, HiddenField, StringField

from eNMS.database.dialect import Column, LargeString, MutableDict, SmallString
from eNMS.forms.automation import ServiceForm
from eNMS.forms.services import ValidationForm
from eNMS.models.automation import Service


class PayloadValidationService(Service):

    __tablename__ = "payload_validation_service"

    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    has_targets = Column(Boolean, default=False)
    query = Column(SmallString)
    conversion_method = Column(SmallString, default="none")
    validation_method = Column(SmallString, default="text")
    content_match = Column(LargeString, default="")
    content_match_regex = Column(Boolean, default=False)
    dict_match = Column(MutableDict)
    negative_logic = Column(Boolean, default=False)
    delete_spaces_before_matching = Column(Boolean, default=False)

    __mapper_args__ = {"polymorphic_identity": "payload_validation_service"}

    def job(self, run, payload, device=None):
        result = run.eval(run.query, **locals())
        if self.conversion_method != "none":
            result = run.convert_result(result)
        match = (
            run.sub(run.content_match, locals())
            if run.validation_method == "text"
            else run.sub(run.dict_match, locals())
        )
        return {
            "query": run.query,
            "match": match,
            "negative_logic": run.negative_logic,
            "result": result,
            "success": run.match_content(result, match),
        }


class PayloadValidationForm(ServiceForm, ValidationForm):
    form_type = HiddenField(default="payload_validation_service")
    has_targets = BooleanField("Has Target Devices", default=True)
    query = StringField("Python Query")
    query_fields = ServiceForm.query_fields + ["query"]
