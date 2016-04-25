import kombu
import sys
import json


def setup_queue(hostname):
    conn = kombu.Connection(hostname=hostname)
    producer = conn.SimpleQueue('errors')
    return conn, producer

if len(sys.argv) != 2:
    print("Invalid arguments", file=sys.stderr)
    sys.exit(2)

data = json.loads(sys.argv[1])
connection, queue = setup_queue("amqp://mquser:mqpassword@localhost:5672")
queue.put(data)
queue.close()
