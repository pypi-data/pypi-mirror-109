import math
import uuid
from textwrap import dedent

from gevent import sleep
from jumpscale.loader import j
from jumpscale.sals.chatflows.chatflows import GedisChatBot, chatflow_step
from jumpscale.sals.reservation_chatflow import DeploymentFailed, deployer, deployment_context, solutions


class Long(GedisChatBot):
    HUB_URL = "https://hub.grid.tf/tf-bootable"
    IMAGES = ["ubuntu-18.04", "ubuntu-20.04"]

    steps = [
        "ubuntu_name",
    ]

    title = "Long"

    def _ubuntu_start(self):
        deployer.chatflow_pools_check()
        deployer.chatflow_network_check(self)
        self.solution_id = uuid.uuid4().hex
        self.user_form_data = dict()
        self.query = dict()
        self.user_form_data["chatflow"] = "ubuntu"
        self.solution_metadata = {}

    @chatflow_step(title="Solution Name")
    def ubuntu_name(self):
        self._ubuntu_start()
        i = 0
        while i < 20:
            self.md_show(f"this is I: {i} ")
            print(self.solution_id, "loop ", i)
            i += 1
            sleep(1)
        
        self.md_show(f"tdone... I: {i} ")
        print(self.solution_id, "done", i)


chat = Long