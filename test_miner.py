import socket
import json
import time


HOST = "127.0.0.1"
PORT = 3333


def send(sock, payload):

    message = json.dumps(payload)

    print("\n>>>", message)

    sock.sendall(
        (message + "\n").encode()
    )


def receive(sock):

    data = sock.recv(4096)

    if not data:
        return None

    message = data.decode().strip()

    print("\n<<<", message)

    return json.loads(message)



sock = socket.socket()

sock.connect(
    (HOST, PORT)
)


print("Connected to StratumDGB")



# Subscribe

send(sock, {

    "id": 1,

    "method": "mining.subscribe",

    "params": []

})


subscribe = receive(sock)



# Authorize

send(sock, {

    "id": 2,

    "method": "mining.authorize",

    "params": [
        "test.worker",
        "x"
    ]

})


receive(sock)



# Read messages until we get notify

job = None


while True:

    message = receive(sock)

    if not message:
        break


    if message.get("method") == "mining.notify":

        job = message["params"]

        break



if not job:

    print("No job received")

    sock.close()

    exit()



job_id = job[0]
ntime = job[7]


print("\nCurrent job:")
print("Job ID:", job_id)
print("ntime:", ntime)



# Submit fake share

submit = {

    "id": 3,

    "method": "mining.submit",

    "params": [

        "test.worker",

        job_id,

        "00000001",

        ntime,

        "deadbeef"

    ]

}


send(sock, submit)

receive(sock)



# Submit duplicate

print("\nSubmitting duplicate...\n")


submit["id"] = 4


send(sock, submit)

receive(sock)



time.sleep(1)

sock.close()
