from datetime import datetime
from pathlib import Path
from re import M, sub
from sqlalchemy import Boolean, ForeignKey, Integer
from wtforms import HiddenField, StringField

from eNMS import app
from eNMS.database.dialect import Column, MutableDict, SmallString
from eNMS.database.functions import factory
from eNMS.forms.automation import NapalmForm
from eNMS.models.automation import ConnectionService


class NapalmBackupService(ConnectionService):

    __tablename__ = "napalm_backup_service"
    pretty_name = "NAPALM Backup"
    parent_type = "connection_service"
    id = Column(Integer, ForeignKey("connection_service.id"), primary_key=True)
    driver = Column(SmallString)
    use_device_driver = Column(Boolean, default=True)
    timeout = Column(Integer, default=60)
    optional_args = Column(MutableDict)
    regex_pattern_1 = Column(SmallString)
    regex_replace_1 = Column(SmallString)
    regex_pattern_2 = Column(SmallString)
    regex_replace_2 = Column(SmallString)
    regex_pattern_3 = Column(SmallString)
    regex_replace_3 = Column(SmallString)

    __mapper_args__ = {"polymorphic_identity": "napalm_backup_service"}

    def job(self, run, payload, device):
        try:
            device.last_runtime = datetime.now()
            path_configurations = Path.cwd() / "git" / "configurations"
            path_device_config = path_configurations / device.name
            path_device_config.mkdir(parents=True, exist_ok=True)
            napalm_connection = run.napalm_connection(device)
            run.log("info", "Fetching NAPALM configuration", device)
            configuration = app.str_dict(napalm_connection.get_config())
            device.last_status = "Success"
            device.last_duration = (
                f"{(datetime.now() - device.last_runtime).total_seconds()}s"
            )
            for i in range(1, 4):
                configuration = sub(
                    getattr(self, f"regex_pattern_{i}"),
                    getattr(self, f"regex_replace_{i}"),
                    configuration,
                    flags=M,
                )
            if device.configuration == configuration:
                return {"success": True, "result": "no change"}
            device.last_update = str(device.last_runtime)
            factory(
                "configuration",
                device=device.id,
                runtime=device.last_runtime,
                duration=device.last_duration,
                configuration=configuration,
            )
            device.configuration = configuration
            with open(path_device_config / device.name, "w") as file:
                file.write(configuration)
            run.generate_yaml_file(path_device_config, device)
        except Exception as e:
            device.last_status = "Failure"
            device.last_failure = str(device.last_runtime)
            run.generate_yaml_file(path_device_config, device)
            return {"success": False, "result": str(e)}
        return {"success": True, "result": "Get Config via Napalm"}


class NapalmBackupForm(NapalmForm):
    form_type = HiddenField(default="napalm_backup_service")
    regex_pattern_1 = StringField("First regex to change config results")
    regex_replace_1 = StringField("Value to replace first regex")
    regex_pattern_2 = StringField("Second regex to change config results")
    regex_replace_2 = StringField("Value to replace second regex")
    regex_pattern_3 = StringField("Third regex to change config results")
    regex_replace_3 = StringField("Value to replace third regex")
    groups = {
        "Main Parameters": {
            "commands": [
                "regex_pattern_1",
                "regex_replace_1",
                "regex_pattern_2",
                "regex_replace_2",
                "regex_pattern_3",
                "regex_replace_1",
            ],
            "default": "expanded",
        },
        **NapalmForm.groups,
    }
