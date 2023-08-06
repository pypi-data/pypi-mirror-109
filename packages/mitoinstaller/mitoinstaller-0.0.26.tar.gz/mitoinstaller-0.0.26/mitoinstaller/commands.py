"""
Contains useful commands for interacting
with the command line directly
"""

import subprocess
import sys

def run_command(command_array):
    """
    An internal command that should be used to run all commands
    that run on the command line, so that output from failing
    commands can be captured.
    """
    completed_process = subprocess.run(command_array, capture_output=True)
    if completed_process.returncode != 0:
        raise Exception(
            completed_process.stdout.decode() + completed_process.stderr.decode()
        )

def jupyter_labextension_list():
    """
    Returns the stdout, stderr pair for the currently
    installed jupyterlab extensions.
    """

    sys_call = [sys.executable, "-m", "jupyter", "labextension", "list"]

    completed_process = subprocess.run(sys_call, capture_output=True)
    return completed_process.stdout.decode(), completed_process.stderr.decode()


def uninstall_labextension(extension):
    """
    Uninstall a labextension
    """

    sys_call = [sys.executable, "-m", "jupyter", "labextension", "uninstall", extension]
    run_command(sys_call)


def uninstall_pip_packages(*packages):
    """
    This function uninstalls the given packages in a single pass
    using pip, through the command line.
    """

    sys_call = [sys.executable, "-m", "pip", "uninstall", "-y"]

    for package in packages:
        sys_call.append(package)
    
    run_command(sys_call)


def install_pip_packages(*packages):
    """
    This function installs the given packages in a single pass
    using pip, through the command line.

    https://stackoverflow.com/questions/12332975/installing-python-module-within-code
    """

    sys_call = [sys.executable, "-m", "pip", "install"]

    for package in packages:
        sys_call.append(package)
    sys_call.append('--upgrade')

    run_command(sys_call)

def upgrade_mito_installer():
    """
    Upgrades the mito installer package itself
    """
    run_command([sys.executable, "-m", "pip", "install", 'mitoinstaller', '--upgrade', '--no-cache-dir'])


def check_running_jlab_3_processes():
    """
    Returns true if there are running JLab 3 processes, 
    returns false if there are not.

    Useful for telling the user to refresh their servers
    if they install Mito
    """
    sys_call = [sys.executable, "-m", "jupyter", "server", "list"]
    completed_process = subprocess.run(sys_call, capture_output=True)
    return len(completed_process.stdout.decode().strip().splitlines()) > 1

def check_running_jlab_not_3_processes():
    """
    Returns true if there are running JLab processes, 
    returns false if there are not.

    Useful for telling the user to refresh their servers
    if they install Mito
    """
    sys_call = [sys.executable, "-m", "jupyter", "notebook", "list"]
    completed_process = subprocess.run(sys_call, capture_output=True)
    return len(completed_process.stdout.decode().strip().splitlines()) > 1

def check_running_jlab_processes():
    """
    Returns true if there are running JLab processes from any version
    returns false if there are not.
    """
    return check_running_jlab_3_processes() or check_running_jlab_not_3_processes()

def exit_with_error(install_or_upgrade, error=None):
    full_error = f'\n\nSorry, looks like we hit a problem during {install_or_upgrade}. ' + \
        ('' if error is None else ("It seems we " + error + '.')) + \
        '\nWe\'re happy to help you fix it, just shoot an email to jake@sagacollab.com and copy in the output above.\n'

    print(full_error)
    exit(1)