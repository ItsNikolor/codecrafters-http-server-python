import socket
from time import sleep

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


from enum import Enum


class Status(Enum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found"


class InputData:
    def __init__(self, data: str):
        data = data.split("\r\n")

        self.method, self.path, self.version = data[0].split(" ")


def response_data(
    status: Status,
    version: str,
    content_type: str = "",
    content_lenght: int = 0,
    body: str = "",
):
    status = f"{version} {status.value}\r\n"
    headers = (
        f"Content-Type: {content_type}\r\nContent-Length: {content_lenght}\r\n\r\n"
    )
    body = body

    response = status + headers + body + "\r\n" if body else status
    return response


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        with socket.create_server(
            (self.host, self.port), reuse_port=True
        ) as server_socket:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024).decode()
                    print(f"Data = {data}")
                    data = InputData(data)

                    if data.path.startswith("/echo/"):
                        response = response_data(
                            Status.OK,
                            data.version,
                            "text/plain",
                            3,
                            data.path[len("/echo/") :],
                        )
                    elif data.path == "/":
                        response = response_data(
                            Status.OK, data.version
                        )
                    else:
                        response = response_data(
                            Status.NOT_FOUND, data.version,
                        )
                    conn.sendall(response)
                    print(f"Data sent {response}")


def main():
    print("Logs from your program will appear here!")

    server = Server("localhost", 4221)
    server.start()


if __name__ == "__main__":
    main()
