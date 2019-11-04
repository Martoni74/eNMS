from sqlalchemy import Boolean, Float, ForeignKey, Integer
from wtforms import HiddenField

from eNMS.database.dialect import Column, LargeString, SmallString
from eNMS.forms.fields import SubstitutionField
from eNMS.forms.automation import NetmikoForm
from eNMS.models.automation import ConnectionService


class NetmikoPromptsService(ConnectionService):

    __tablename__ = "netmiko_prompts_service"
    pretty_name = "Netmiko Prompts"
    parent_type = "connection_service"
    id = Column(Integer, ForeignKey("connection_service.id"), primary_key=True)
    enable_mode = Column(Boolean, default=True)
    config_mode = Column(Boolean, default=False)
    command = Column(SmallString)
    confirmation1 = Column(LargeString, default="")
    response1 = Column(SmallString)
    confirmation2 = Column(LargeString, default="")
    response2 = Column(SmallString)
    confirmation3 = Column(LargeString, default="")
    response3 = Column(SmallString)
    driver = Column(SmallString)
    use_device_driver = Column(Boolean, default=True)
    fast_cli = Column(Boolean, default=False)
    timeout = Column(Integer, default=10.0)
    delay_factor = Column(Float, default=1.0)
    global_delay_factor = Column(Float, default=1.0)

    __mapper_args__ = {"polymorphic_identity": "netmiko_prompts_service"}

    def job(self, run, payload, device):
        netmiko_connection = run.netmiko_connection(device)
        command = run.sub(run.command, locals())
        run.log("info", f"Sending '{command}' with Netmiko", device)
        commands = [command]
        results = {"commands": commands}
        result = netmiko_connection.send_command_timing(
            command, delay_factor=run.delay_factor
        )
        response1 = run.sub(run.response1, locals())
        confirmation1 = run.sub(run.confirmation1, locals())
        results[command] = {"result": result, "match": confirmation1}
        if confirmation1 not in result:
            results.update({"success": False, "result": result, "match": confirmation1})
            return results
        elif response1:
            result = netmiko_connection.send_command_timing(
                response1, delay_factor=run.delay_factor
            )
            confirmation2 = run.sub(run.confirmation2, locals())
            commands.append(confirmation2)
            results[response1] = {"result": result, "match": confirmation2}
            response2 = run.sub(run.response2, locals())
            if confirmation2 not in result:
                results.update(
                    {"success": False, "result": result, "match": confirmation2}
                )
                return results
            elif response2:
                result = netmiko_connection.send_command_timing(
                    response2, delay_factor=run.delay_factor
                )
                confirmation3 = run.sub(run.confirmation3, locals())
                commands.append(confirmation3)
                results[response2] = {"result": result, "match": confirmation3}
                response3 = run.sub(run.response3, locals())
                if confirmation3 not in result:
                    results.update(
                        {"success": False, "result": result, "match": confirmation3}
                    )
                    return results
                elif response3:
                    result = netmiko_connection.send_command_timing(
                        response3, delay_factor=run.delay_factor
                    )
        return {"commands": commands, "result": result}


class NetmikoPromptsForm(NetmikoForm):
    form_type = HiddenField(default="netmiko_prompts_service")
    command = SubstitutionField()
    confirmation1 = SubstitutionField()
    response1 = SubstitutionField()
    confirmation2 = SubstitutionField()
    response2 = SubstitutionField()
    confirmation3 = SubstitutionField()
    response3 = SubstitutionField()
    groups = {
        "Main Parameters": {
            "commands": [
                "command",
                "confirmation1",
                "response1",
                "confirmation2",
                "response2",
                "confirmation3",
                "response3",
            ],
            "default": "expanded",
        },
        **NetmikoForm.groups,
    }
