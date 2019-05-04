from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from wtforms import (
    BooleanField,
    FloatField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
)
from wtforms.widgets import TextArea

from eNMS.controller import controller
from eNMS.forms import metaform
from eNMS.forms.automation import ServiceForm
from eNMS.models import register_class
from eNMS.models.automation import Service
from eNMS.models.inventory import Device


class NetmikoConfigurationService(Service, metaclass=register_class):

    __tablename__ = "NetmikoConfigurationService"

    id = Column(Integer, ForeignKey("Service.id"), primary_key=True)
    has_targets = True
    content = Column(String(255), default="")
    enable_mode = Column(Boolean, default=False)
    driver = Column(String(255), default="")
    driver_values = controller.NETMIKO_DRIVERS
    use_device_driver = Column(Boolean, default=True)
    fast_cli = Column(Boolean, default=False)
    timeout = Column(Integer, default=1.0)
    delay_factor = Column(Float, default=1.0)
    global_delay_factor = Column(Float, default=1.0)

    __mapper_args__ = {"polymorphic_identity": "NetmikoConfigurationService"}

    def job(self, payload: dict, device: Device) -> dict:
        netmiko_handler = self.netmiko_connection(device)
        if self.enable_mode:
            netmiko_handler.enable()
        config = self.sub(self.content, locals())
        self.logs.append(f"Pushing configuration on {device.name} (Netmiko)")
        netmiko_handler.send_config_set(
            config.splitlines(), delay_factor=self.delay_factor
        )
        netmiko_handler.disconnect()
        return {"success": True, "result": f"configuration OK {config}"}


class NetmikoConfigurationForm(ServiceForm, metaclass=metaform):
    form_type = HiddenField(default="NetmikoConfigurationService")
    content = StringField(widget=TextArea(), render_kw={"rows": 5})
    enable_mode = BooleanField()
    driver = SelectField(choices=controller.NETMIKO_DRIVERS)
    use_device_driver = BooleanField(default=True)
    fast_cli = BooleanField()
    timeout = IntegerField()
    delay_factor = FloatField()
    global_delay_factor = FloatField()