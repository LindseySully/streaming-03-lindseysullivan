# Streaming-03-Bonus Project
## Student Name: Lindsey Sullivan
## Date: 9/7/2023

## Bonus Project Overview

## Prerequisties
1. Git
1. Python 3.7+ (3.11+ preferred)
1. VS Code Editor
1. VS Code Extension: Python (by Microsoft)
1. RabbitMQ Server installed and running locally

## Virtual Environment Setup
Create a local Python virtual environment to isolate our project's third-party dependencies from other projects.

1. Open a terminal window in VS code.
1. Use the built-in Python utility venv to create a new virtual environment named `.venv` in the current directory.

```shell
python -m venv .venv
```

In the same VS Code terminal window, activate the virtual environment:

`source .venv/bin/activate`

Verify .venv name in the terminal prompt and then run the following command:

`python -m pip install -r requirements`

You may get a message to update your pip version, follow the command provided to update

`python -m pip install --upgrade pip`

Use the following utility files to verify you are set up correctly:
- util_about.py
- util_aboutenv.py
- util_aboutrabbit.py

The run the following:

```shell
python util_about.py
python util_aboutenv.py
python util_aboutrabbit.py
pip list
```


## emit_message.py

This program is responsible for emit_messages from a dedicated CSV file via RabbitMQ. The program completes the following:
1. Sets constants for the input file, host, and number of messages
    - The user may specify the max amount of messages to send. This limits the continually streaming of messages from the CSV file which contains 5,000 lines.
1. Defines functions for:
    - prepare_message_from_row(row)
        - prepares the CSV file information to be trasmitted into a binary message for a given row
        - limits the message information to the song name and artist name.
    - stream_row(input_file_name)
        - takes the input file name and prepares the data to stream.
        - skips the header row and reads the csv file contents.

    - send_message(host,queue_name, message, messages_sent, max_messages)
        - Creates and sends a message to the queue, waits 3 seconds before transmitting another message. 
        - Looks at the MAX_MESSAGE constant defined in the program to determine the number of messages to send before closing the connection.
        - Parameters of messages_sent is the counter to ensure the connection closes after sending the amount of messages defined in the constant value.

1. Sends a message until messages_sent reaches the value defined in the MAX_MESSAGES constant.

## listen_for_message.py

This program is responsible for establishing a process to listen for messages continuously from the "song" queue. The connection is closed via the users input of ctrl + c. 


## Additional Notes:

To review the queues for the file you can use rabbitmq web-based platform to check which queues are active and their activity. This greatly helps with debugging if messages are being sent or not. 

Two terminals:
![Alt text](<Screenshots/Terminal Output.png>)