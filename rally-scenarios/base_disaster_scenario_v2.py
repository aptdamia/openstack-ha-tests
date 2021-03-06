import json
import requests
import time

from rally.common import log as logging
from rally.benchmark.scenarios import base

LOG = logging.getLogger(__name__)


class BaseDisasterScenario(base.Scenario):

    # def __init__(self, context=None, admin_clients=None, clients=None):

    def boot_vm(self, name):
        nova = self.admin_clients("nova")
        kwargs = {"auto_assign_nic": True}
        vm = nova.servers.create(name=name,
                                 image=self.context["shaker_image"],
                                 flavor=self.context["default_flavor"],
                                 **kwargs)
        return vm

    # TODO(vrovachev): delete duplicate method on this or on context
    def run_command(self, node, command, recover_command=None,
                    recover_timeout=0):
        if recover_command is not None:
            action = {"node": node, "command": recover_command,
                      "timeout": recover_timeout}
            self.context["recover_commands"].append(action)

        LOG.debug("command from BaseDisasterScenario = %s", command)
        LOG.debug("%s", node)
        res = base.shaker.run_program(node, command)

        LOG.debug("res = %s", res)
        return res

    def power_off_controller(self, controller_id):
        control_node = self.context["power_control_node"]
        controller = self.context["controllers"][controller_id]

        self.run_command(control_node["shaker_agent_id"],
                         command=controller["hardware_power_off_cmd"],
                         recover_command=controller["hardware_power_on_cmd"],
                         recover_timeout=controller["power_on_timeout"])
        time.sleep(controller["power_off_timeout"])

    def power_off_main_controller(self):
        pass
