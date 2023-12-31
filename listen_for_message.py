"""
Lindsey Sullivan - 9/7/23

Description:
This script continuously listens for messages on a named queue.
A terminal must be open and dedicated to this process.

Emit messages you must open a different terminal window.

Terminal controls:
- Ctrl + c to close a terminal and end the listening process
- Up Arrow to recall the last command executed in the terminal window

"""

# Import necessary modules from the Python Standard Library
import sys

# Import the pika library to facilitate communication with RabbitMQ
import pika

# Import CSV library to write messages to new file
import csv

# Import the custom logger setup utility (local file named util_logger.py)
from util_logger import setup_logger

# Setup custom logging
logger, logname = setup_logger(__file__)

# Define output CSV file
OUTPUT_CSV_FILE = "received_messages.csv"

# Open the CSV file for writing and write the header row
with open(OUTPUT_CSV_FILE, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Song","Artist(s)"])  # Write the header row

# ---------------------------------------------------------------------------
# Define program functions
# ---------------------------------------------------------------------------

def process_message(ch,method,properties,body):
    """
     Parameters:
    - ch: The channel object from RabbitMQ. It provides methods to interact with the protocol,
          but we don't need them in this particular callback.
    - method: Contains details about the delivery method and its properties,
              such as the delivery tag or the exchange/routing key.
              We don't use it in this example.
    - properties: Message properties like content_type or delivery_mode.
                  Not used here since we're focused on the message body.
    - body: The body of the message (the actual content).
    """

    message = body.decode() # convert binary to string
    logger.info(f"Received: {message}")
    
    # Parse the received message
    try:
        message_info = eval(message)  # Evaluate the string as a dictionary
        song_name = message_info.get("Song", "")
        artist_name = message_info.get("Artist(s)", "")
        
        # Write the message data to the CSV file
        with open(OUTPUT_CSV_FILE, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([song_name, artist_name])
        
        logger.info(f"Received message saved to {OUTPUT_CSV_FILE}")
    except Exception as e:
        logger.error(f"Error processing the received message: {e}")


# Define a main function to run the program
# If no argument is provided, set a default value to localhost
def main(hn: str = "localhost"):

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        logger.error("ERROR: connection to RabbitMQ server failed.")
        logger.error(f"Verify the server is running on host={hn}.")
        logger.error(f"The error says: {e}")
        sys.exit(1)
    
    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        #use the channel to declare a queue
        channel.queue_declare(queue="song")

        # use the channel to consume messages from the queue
        # on getting a message, execute the login in the callback function
        channel.basic_consume(
            queue="song", on_message_callback=process_message, auto_ack=True
        )

        # print a message to the console for the user
        logger.info(" [*] Waiting for messages. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()
    
    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        logger.error(
            "ERROR: An issue occurred while setting up or listening for messages."
        )
        logger.error(f"Error Details: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.warning("User interrupted the listening process. Exiting...")
        sys.exit(0)
    finally:
        logger.info("Closing connection. Goodbye.")
        connection.close()


# ---------------------------------------------------------------------------
# If this is the script we are running, then call some functions and execute code!
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()