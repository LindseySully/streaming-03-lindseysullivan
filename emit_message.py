"""
Lindsey Sullivan - 9/7/23

Description:
This script sends one message on a named queue called "song".
It will execute every 1-3 seconds.

The resouce is the spotifytop200songslimversion.csv
This is slimmed down version of a larger data set that is smaller for easier streaming of data. 

"""
# Import from Standard Library
import sys

# Import for streaming csv files
import csv
import time
import os

# Setup path to directory of input file
os.chdir("/Users/lindseysullivan/Documents/School/Streaming-Data/Modules/streaming-03-lindseysullivan")

# Import packages for rabbitmq messaging
import pika

import json
# Configure logging
from util_logger import setup_logger

logger, logname = setup_logger(__file__)

# Declare program constants
HOST = "localhost"
INPUT_FILE_NAME = "spotifytop200songsslimversion.csv"
MAX_MESSAGES = 10 # Define the number of max messages

# ----------------------------------------------------------
# Define Program Functions
# ----------------------------------------------------------
def prepare_message_from_row(row):
    """
        Prepares a JSON message from a given row

    """
    song_name = row[10] # Index 10 corresponds to song name
    artist_name = row[3] # Index 3 corresponds to artist name
    # Create a dictionary of song name & artist name
    message_info = {
        "Song": song_name,
        "Artist(s)": artist_name,
    }
    # convert dictionary to JSON string
    json_message = json.dumps(message_info)
    
    return json_message

def stream_row(input_file_name):
    """
    Read input file and prepare data to stream

    """
    logger.info("Reading CSV file...")
    with open(input_file_name, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file, delimiter=",") # Create a CSV reader object
        next(reader,None)  # Skip header row
        for row in reader:  # Indent this line
            MESSAGE = prepare_message_from_row(row)
            time.sleep(3)  # Wait 3 seconds between messages



def send_message(host: str, queue_name: str, message, messages_sent, max_messages):
    """
        Creates and sends a message to the queue. Waits 3 seconds before sending
        another message.
        This processes looks at the MAX_MESSAGE constant to see how many messages
        a user would like to send.

        Parameters:
            queue_name (str): the name of the queue
            message (str): the message to be sent to the queue
            messages_sent: counter for number of messages
            max_messages: max number of messages to send

        """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))

        # use the connection to create a communication channel
        ch = conn.channel()

        # use the channel to declare a queue
        ch.queue_declare(queue=queue_name)

        # Read and prepare all messages to send
        messages = [prepare_message_from_row(row) for row in csv.reader(open(INPUT_FILE_NAME, "r",encoding="utf-8"))]
        messages = messages[1:]
        
        # Use the channel to publish a message to the queue
        while messages_sent < MAX_MESSAGES:
            current_message = messages[messages_sent % len(messages)]  # Cycle through the messages
            ch.basic_publish(exchange="", routing_key=queue_name, body=current_message)
            logger.info(f" [x] Sent message {messages_sent + 1}:{current_message}")  # Log a message for the user
            messages_sent += 1
            time.sleep(3)  # Wait 3 seconds between sending messages
        
        # close the connection after sending the number of messages defined in max_messages
        conn.close()
        logger.info("Connection closed after sending messages.")
        
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)

 # ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    messages_sent = 0 # counter for messages sent
    messages = [prepare_message_from_row(row) for row in csv.reader(open(INPUT_FILE_NAME, "r", encoding="utf-8"))]
    
    send_message(HOST, "song", messages[messages_sent % len(messages)], messages_sent, MAX_MESSAGES)

  