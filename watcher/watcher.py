import os
import time
import subprocess

import yaml
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler


class ChangeHandler(RegexMatchingEventHandler):
    def __init__(self, run_command, project_path, ignore_regexes, *args, **kwargs):
        super().__init__(ignore_regexes=ignore_regexes, *args, **kwargs)
        self.run_command = run_command
        self.project_path = project_path
        self.grpc_process = None
        self.start_server()

    def on_any_event(self, event):
        print(f"Detected changes in {event.src_path}, restarting gRPC server...")
        self.restart_server()

    def start_server(self):
        self.grpc_process = subprocess.Popen(self.run_command, cwd=self.project_path)

    def restart_server(self):
        if self.grpc_process:
            self.grpc_process.terminate()
        self.start_server()


def load_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def make_regex_pattern(relative_path, project_path):
    absolute_path = os.path.join(project_path, relative_path)
    return fr"{absolute_path}.*"


def run(config_path):
    config = load_config(config_path)
    project_path = os.path.abspath(config["project_path"])
    run_command = config["run_command"]
    excluded_paths = config.get("excluded_paths", [])
    excluded_files = config.get("excluded_files", [])

    ignore_regexes = [make_regex_pattern(path, project_path) for path in excluded_paths]
    file_regexes = [os.path.join(project_path, pattern) for pattern in excluded_files]
    ignore_regexes.extend(file_regexes)

    event_handler = ChangeHandler(run_command, project_path, ignore_regexes=ignore_regexes)
    observer = Observer()
    observer.schedule(event_handler, project_path, recursive=True)

    print("Starting observer...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

