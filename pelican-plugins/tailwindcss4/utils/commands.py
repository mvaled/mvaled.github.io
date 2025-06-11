import subprocess


def run_in_plugin(command: str, cwd: str):
    subprocess.run(args=command, cwd=cwd, shell=True, check=False)
