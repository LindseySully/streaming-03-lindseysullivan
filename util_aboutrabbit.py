"""
======================= INSTRUCTOR-GENERATED FILE =======================

This is an auxiliary script designed to assist you in verifying RabbitMQ is 
installed and running for your project. 
It is NOT part of the main project tasks.

You do NOT need to understand every detail or modify this file. 

Before diving into the main project, run this script. 
It will check RabbitMQ, log results to the terminal, 
and save them in a file named `aboutrabbit.txt`. 
If you face issues with RabbitMQ, review this file and share 
its contents to help with debugging.

USAGE:
To use, execute this script. In VS Code select Terminal / New Terminal and 
run the following command: python util_aboutrabbit.py
- OR On Windows:         py util_aboutrabbit.py
- OR On macOS/Linux:     python3 util_aboutrabbit.py

@Author: Denise Case
@Updated: 2023-08

==========================================================================

"""

# Import from Python Standard Library

import datetime
import logging
import subprocess
import sys

# Import from third party libraries
# Must be installed into our virtual environment first

import pika

# Set up basic logging

OUTPUT_FILENAME = "aboutrabbit.txt"
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.FileHandler(OUTPUT_FILENAME, mode="w"), logging.StreamHandler()],
)

# Declare additional program constants

DIVIDER = "=" * 70  # A string divider for cleaner output formatting

# Define program functions

import os


def get_choco_rabbitmq_path():
    """Find the path of RabbitMQ installation by Chocolatey."""
    # Define the general directory where Chocolatey installs software
    # Use a raw string to avoid issues with backslashes (preface with r)
    base_choco_dir = r"C:\ProgramData\chocolatey\lib\rabbitmq\tools"

    # Check if the base choco directory exists
    if os.path.exists(base_choco_dir):
        # List all folders in the directory
        folders = os.listdir(base_choco_dir)

        # Find folders starting with 'rabbitmq_server'
        rabbitmq_folders = [f for f in folders if f.startswith("rabbitmq_server")]

        # Sort them to get the latest version (assuming version numbers are used in the naming)
        rabbitmq_folders.sort(reverse=True)

        # Get the path of the latest version
        if rabbitmq_folders:
            latest_version_path = os.path.join(
                base_choco_dir, rabbitmq_folders[0], "sbin"
            )
            # Return the path if it exists
            if os.path.exists(latest_version_path):
                return latest_version_path

    # Return None if no valid path was found
    return None


def is_rabbitmq_installed():
    """Return True if RabbitMQ is installed, False otherwise."""
    try:
        cmd = "rabbitmqctl.bat" if sys.platform == "win32" else "rabbitmqctl"
        subprocess.check_output([cmd, "status"])
        return True
    except subprocess.CalledProcessError:
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False


def is_rabbitmq_running():
    """Return True if RabbitMQ is running, False otherwise."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        connection.close()
        return True
    except pika.exceptions.AMQPConnectionError:
        return False


def get_rabbitmq_start_command():
    """Return the command to start RabbitMQ based on the OS."""
    if sys.platform == "win32":
        return "net start RabbitMQ"
    elif sys.platform == "darwin":  # macOS
        return "brew services start rabbitmq"
    elif sys.platform == "linux":
        # This is a general approach and might not work for all distributions.
        # Adjust as needed for your specific distribution.
        return "sudo systemctl start rabbitmq-server"
    else:
        return None


def check_and_log_rabbitmq_status():
    """Check and log RabbitMQ status."""
    installed = is_rabbitmq_installed()
    logging.info(DIVIDER)

    if not installed:
        logging.error("ERROR: RabbitMQ is NOT installed. Please install RabbitMQ.")
        return

    logging.info("Yay! RabbitMQ is installed.")
    if not is_rabbitmq_running():
        logging.warning("RabbitMQ is NOT running. Please start RabbitMQ.")
        start_command = get_rabbitmq_start_command()
        if start_command:
            logging.info(f"Try the following command: {start_command}")
        else:
            logging.error("Platform not recognized.")


# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    logging.info(DIVIDER)
    logging.info("Welcome to the Python Debugging Information Utility ABOUTRABBIT.PY")
    logging.info(
        f"Date and Time: {datetime.date.today()} at {datetime.datetime.now().strftime('%I:%M %p')}"
    )
    check_and_log_rabbitmq_status()
    logging.info(DIVIDER)
