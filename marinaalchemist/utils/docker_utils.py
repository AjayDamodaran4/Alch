import os
import docker
import json
import re
import subprocess
import time
from .config_reader import Config


class DockerUtils(object):
    container_name = Config.get_value_of_config_key("container_name")
    client = docker.from_env()
    container = client.containers.get(container_name)
    container_info = container.attrs
    ip_address = container_info['NetworkSettings']['IPAddress']

    def __int__(self, input_path=None, output_path=None):
        self.compose_file_path = Config.get_value_of_config_key("compose_file_path")
        self.input_path = input_path
        self.output_path = output_path

    def container_autorun(self, input_path, output_path):

        volumes = {
            input_path: {'bind': '/app/input', 'mode': 'rw'},
            output_path: {'bind': '/app/output', 'mode': 'rw'},
            Config.get_value_of_config_key("container_temp_path"): {'bind': '/app/temporary', 'mode': 'rw'},
            Config.get_value_of_config_key("container_prior_path"): {'bind': '/app/prior', 'mode': 'rw'}
        }

        environment = {
            'TZ': Config.get_value_of_config_key("TZ"),
            'runMode': Config.get_value_of_config_key("runMode"),
            'requestPort': Config.get_value_of_config_key("requestPort")
        }

        container = self.client.containers.run(
            Config.get_value_of_config_key("docker_image"),
            name=Config.get_value_of_config_key("container_name"),
            detach=True,
            volumes=volumes,
            environment=environment
        )



    #
    # def is_container_running(self):
    #     try:
    #         if self.container.status == 'running' and self.ip_address:
    #             print(f"Container {self.container_name} is running. IPaddress of the container is : {self.ip_address}")
    #             return True
    #
    #     except docker.errors.NotFound:
    #         print(f"Container {self.container_name} is not found or IPaddress of the container not available")
    #         print("Restart of container is required")
    #
    #     return False
    #
    # def start_container_if_not_running(self):
    #     if self.is_container_running():
    #         print(f"The container '{self.container_name}' is running.")
    #     else:
    #         try:
    #             cmd = f'docker container inspect {self.container_name}'
    #             result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #
    #             # Parse the JSON output of 'docker container inspect'
    #             container_info = json.loads(result.stdout)
    #             if container_info[0]["State"]["Status"] == "running":
    #                 cmd = f'docker-compose -f {self.compose_file_path} down -d'
    #                 subprocess.run(cmd, shell=True, check=True, text=True, cwd='/nuance/AJ')
    #                 print(f"The container '{self.container_name}' was running in the background, hence stopped!")
    #             # Execute 'docker-compose up' to start the container
    #             cmd = f'docker-compose -f {self.compose_file_path} up -d'
    #             subprocess.run(cmd, shell=True, check=True, text=True, cwd='/nuance/AJ')
    #             print(f"The container '{self.container_name}' was not running and has been started.")
    #         except subprocess.CalledProcessError as e:
    #             print(f"Error starting the container: {str(e)}")
    #
    # def check_container_logs(self):
    #     target_string = "uvicorn.error:Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)"
    #     max_check_time_seconds = 300  # Maximum checking time (seconds)
    #     check_interval_seconds = 10
    #     try:
    #         client = docker.from_env()
    #
    #         start_time = time.time()
    #         elapsed_time = 0
    #
    #         while elapsed_time < max_check_time_seconds:
    #             container = client.containers.get(self.container_name)
    #             logs = container.logs().decode("utf-8")
    #
    #             if target_string in logs:
    #                 print(f"Found the target string '{target_string}' in the container logs.")
    #                 break
    #
    #             time.sleep(check_interval_seconds)
    #             elapsed_time = time.time() - start_time
    #
    #         if elapsed_time >= max_check_time_seconds:
    #             print("Maximum check time reached. Target string not found in the container logs.")
    #
    #     except docker.errors.NotFound:
    #         print(f"Container '{self.container_name}' not found.")
    #     except Exception as e:
    #         print(f"Error: {str(e)}")
    #
    # def get_container_ip_address(self):
    #     try:
    #         # Run 'docker inspect' command to get JSON information about the container
    #         cmd = f'docker inspect {self.container_name}'
    #         result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #
    #         # Parse the JSON response
    #         container_info = json.loads(result.stdout)
    #
    #         # Extract the "IPAddress" from the JSON
    #         if isinstance(container_info, list) and len(container_info) > 0:
    #             if container_info and "NetworkSettings" in container_info[0]:
    #                 networks = container_info[0]["NetworkSettings"]["Networks"]
    #
    #                 # Get the first key under "Networks" (dynamically)
    #                 network_name = next(iter(networks))
    #
    #                 # Check if "IPAddress" is present and return it
    #                 if "IPAddress" in networks[network_name]:
    #                     ip_address = networks[network_name]["IPAddress"]
    #                     return ip_address
    #
    #             return None  # Return None if no IPAddress is found
    #
    #         else:
    #             print(f"Container '{self.container_name}' not found or IP address not available.")
    #
    #         return None
    #
    #     except Exception as e:
    #         print(f"Error: {str(e)}")
    #         return None
    #
    # """ Executing Simulator command in terminal"""
    #
    # def simulator_command(self, input_path, output_path):
    #     return f"python3 -m AiSvcTest -i {input_path} -o {output_path} -s http://{self.get_container_ip_address()}:8080 -V 2"
    #
    # def simulator_launch(self, input_path, output_path):
    #     try:
    #         command = f"python3 -m AiSvcTest -i {input_path} -o {output_path} -s http://{self.get_container_ip_address()}:8080 -V"
    #         subprocess.run(command, shell=True, check=True, text=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing the command: {str(e)}")
    #
    # """ Extracting Transaction number everytime simulator is run"""
    #
    # def extract_transaction_number(self, input_path, output_path):
    #     ip_address = self.get_container_ip_address()
    #     if ip_address:
    #         log_command = self.simulator_command(input_path, output_path)
    #         log_process = subprocess.Popen(log_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                                        text=True)
    #         log_output, _ = log_process.communicate()
    #
    #         # Define a regular expression pattern to match the dynamic number
    #         pattern = r"Created new Transaction: (\d+)"
    #
    #         # Search for the pattern in the log output
    #         match = re.search(pattern, log_output)
    #
    #         if match:
    #             transaction_number = match.group(1)  # Extract the dynamic number
    #             return transaction_number
    #
    #         else:
    #             print("Simulator Transaction number not found in logs.")
    #
    # def list_manifests(self, input_path, output_path):
    #     transaction_number = self.extract_transaction_number(input_path, output_path)
    #     if transaction_number:
    #         print(f"Transaction number extracted from logs: {transaction_number}")
    #
    #         # Navigate to the directory and list the available files
    #         output_directory = os.path.join("/nuance/output", transaction_number)
    #         if os.path.exists(output_directory):
    #             print(f"Listing files in directory: {output_directory}")
    #             files = os.listdir(output_directory)
    #             for file in files:
    #                 print(file)
    #         else:
    #             print(f"Directory '{output_directory}' does not exist.")
    #
    #


