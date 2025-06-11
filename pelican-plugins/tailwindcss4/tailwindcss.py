import os
from os import path
import shutil
import subprocess

from pelican import signals

from .utils import commands, installs, utils

BASE_DIR = os.path.dirname(__file__)


def initialize(po):
    SETTINGS = po.settings
    TAILWIND_SETTINGS = SETTINGS.get("TAILWIND", None)
    THEME_PATH = path.abspath(path.join(po.path, ".."))

    package_json_template = os.path.join(BASE_DIR, "package.json.in")
    package_json = os.path.join(THEME_PATH, "package.json")

    print(f"{utils.LOG_PREFIX} Creating package.json")
    shutil.copyfile(package_json_template, package_json)

    print(f"{utils.LOG_PREFIX} Initialization required -- first start")
    commands.run_in_plugin("npm install", cwd=THEME_PATH)
    if TAILWIND_SETTINGS:
        print(f"{utils.LOG_PREFIX} Settings were found")
        installs.plugins(settings=TAILWIND_SETTINGS, cwd=THEME_PATH)


def generate_css(po):
    THEME_PATH = path.abspath(path.join(po.path, ".."))
    input_file_path = os.path.join(THEME_PATH, "input.css")
    output_file_path = os.path.join(THEME_PATH, "output/theme/output.css")

    input_output = f"-i {input_file_path} -o {output_file_path}"
    print(f"{utils.LOG_PREFIX} Build CSS ({output_file_path})")

    commands.run_in_plugin(f"npx @tailwindcss/cli {input_output}", cwd=THEME_PATH)


def register():
    signals.initialized.connect(initialize)
    signals.finalized.connect(generate_css)
