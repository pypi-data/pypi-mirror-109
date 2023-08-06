# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

import re
import time
import uuid
import importlib
from urllib.error import HTTPError
import socket
import subprocess
import requests

from digital_hydrant import logging
import digital_hydrant.config
from digital_hydrant.__version__ import version
from digital_hydrant.commands import shutdown, restart


class Ping:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mac_addr = ":".join(re.findall("..", "%012x" % uuid.getnode()))

        self.api_token = digital_hydrant.config.config.get("api", "token")
        self.api_url = digital_hydrant.config.config.get("api", "url")
        self.first_ping = True

    def get_system_details(self):
        self.first_ping = False
        public_ip = requests.get("https://api.ipify.org").text
        private_ip = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("10.255.255.255", 1))
            private_ip = s.getsockname()[0]
        except Exception as err:
            pass
        finally:
            s.close()

        details = {
            "publicIp": public_ip,
            "privateIp": private_ip,
            "version": version,
        }

        options = {
            "s": "kernelName",
            "n": "nodename",
            "r": "kernelRelease",
            "v": "kernelVersion",
            "m": "machine",
            "p": "processor",
            "i": "hardware",
            "o": "operatingSystem",
        }

        for option, name in options.items():
            output = subprocess.run(
                f"uname -{option}", shell=True, stdout=subprocess.PIPE
            ).stdout.decode("utf-8")

            if output:
                details[name] = output.strip("\n")

        return details

    def __exec__(self):
        while True:
            importlib.reload(digital_hydrant.config)
            self.wait = digital_hydrant.config.config.getint(
                "ping", "wait", fallback=180
            )
            self.logger.setLevel(
                digital_hydrant.config.config.get("logging", "level", fallback="INFO")
            )

            self.logger.info("Ping server")

            try:
                details = self.get_system_details() if self.first_ping else {}

                headers = {"Authorization": f"Bearer {self.api_token}"}
                response = requests.put(
                    f"{self.api_url}/ping",
                    json=details,
                    headers=headers,
                )
                response.raise_for_status()

                response_data = response.json()

                params = None
                # handle new config from the server
                if "config" in response_data.keys() and isinstance(
                    response_data["config"], dict
                ):
                    params = digital_hydrant.config.update_config(
                        response_data["config"]
                    )
                else:
                    params = {}
                    for section in digital_hydrant.config.config.sections():
                        temp_dict = {}
                        for option in digital_hydrant.config.config.options(section):
                            temp_dict[option] = digital_hydrant.config.config.get(
                                section, option
                            )

                        params[section] = temp_dict

                complete_response = requests.put(
                    f"{self.api_url}/ping/complete", json=params, headers=headers
                )
                complete_response.raise_for_status()

                if "commandQueue" in response_data.keys() and isinstance(
                    response_data["commandQueue"], list
                ):
                    for command in response_data["commandQueue"]:
                        if command["type"] == "shutdown":
                            shutdown()
                        elif command["type"] == "restart":
                            restart()

            except requests.exceptions.ConnectionError:
                self.logger.error("Network error on ping")

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    res = e.response.json()
                    if "msBeforeNext" in res:
                        sleep = res["msBeforeNext"] / 1000
                        if sleep > self.wait:
                            time.sleep(sleep)
                self.logger.error(f"Failed to ping server\n{e}")
            time.sleep(self.wait)
