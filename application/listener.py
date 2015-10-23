import logging


def message_received(body, message):
    logging.info("Received new error: %s", str(body))
    message.ack()


def listen(incoming_connection, run_forever=True):
    logging.info('Listening for new registrations')

    while True:
        try:
            incoming_connection.drain_events()
        except KeyboardInterrupt:
            logging.info("Interrupted")
            break
        if not run_forever:
            break
