"""
Contains useful commands for interacting
with the command line directly
"""

import subprocess
import sys

# All encodings that Python supports are here https://docs.python.org/3/library/codecs.html#standard-encodings
# Here, we try and take the most popular 10 of them, so that looping through the list
# in order will make you likely to encounter them, and not take forever
# NOTE: from here, it seems utf-8 is the most common ! https://unix.stackexchange.com/questions/112216/which-terminal-encodings-are-default-on-linux-and-which-are-most-common
PYTHON_ENCODINGS = [
    'utf_8',
    'utf_16',
    'utf_32',
    'ascii',
    'big5',
    'big5hkscs',
    'euc_jp',
    'euc_kr',
    'gbk',
    'hz',
    # Latin 1 can decode like everything, so we put it last
    'latin_1',
]

def get_process_output(completed_process: subprocess.CompletedProcess) -> str:
    """
    A helper function that makes it safe to decode the output
    from the terminal. Uses a try catch as different systems
    used different encodings, and so we want to make sure we 
    don't fail install if we don't need to!
    """
    # First, try with no decoding!
    try:
        return completed_process.stdout.decode() + completed_process.stderr.decode()
    except:
        pass

    for encoding in PYTHON_ENCODINGS:
        try:
            return completed_process.stdout.decode(encoding) + completed_process.stderr.decode(encoding)
        except Exception as e:
            continue

    # If we cannot convert, we just take the raw bytes as a string
    return str(completed_process.stdout) + str(completed_process.stderr)

def run_command(command_array):
    """
    An internal command that should be used to run all commands
    that run on the command line, so that output from failing
    commands can be captured.
    """
    completed_process = subprocess.run(command_array, capture_output=True)
    if completed_process.returncode != 0:
        raise Exception(
            get_process_output(completed_process)
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