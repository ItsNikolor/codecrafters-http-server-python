import os
import socket
import threading
import argparse


from enum import Enum


class Status(Enum):
    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")
    CREATED = (201, "Created")


class InputData:
    def __init__(self, data: str):
        data = data.split("\r\n")

        self.method, self.path, self.version = data[0].split(" ")

        for line in data:
            if line.startswith("User-Agent:"):
                self.user_agent = line[len("User-Agent: ") :]

        self.body = data[-1]


def response_data(
    status: Status,
    version: str,
    content_type: str = "text/plain",
    body: str = "",
):
    response_status = f"{version} {' '.join(status.value)}\r\n"

    if status == Status.NOT_FOUND or body == "":
        response = response_status + "\r\n"
    else:
        headers = f"Content-Type: {content_type}\r\nContent-Length: {len(body.encode())}\r\n\r\n"

        response = response_status + headers + body

    return response.encode()


class Server:
    def __init__(self, host, port, directory):
        self.host = host
        self.port = port
        self.directory = directory

    def start(self):
        with socket.create_server(
            (self.host, self.port), reuse_port=True
        ) as server_socket:
            while True:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=self.handle_request, args=(conn, addr))
                thread.start()

    def handle_request(self, conn, addr):
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode()
            print(f"Data = {data}")
            data = InputData(data)

            if data.method == "POST":
                filename = data.path[len("/files/") :]
                with open(os.path.join(self.directory, filename), "wb") as file:
                    file.write(data.body.encode())

                response = response_data(Status.CREATED, data.version)

            elif data.path.startswith("/echo/"):
                response = response_data(
                    Status.OK,
                    data.version,
                    "text/plain",
                    data.path[len("/echo/") :],
                )
            elif data.path.startswith("/files/"):
                filename = data.path[len("/files/") :]
                if os.path.isfile(os.path.join(self.directory, filename)):
                    with open(os.path.join(self.directory, filename), "rb") as file:
                        response = response_data(
                            Status.OK,
                            data.version,
                            "application/octet-stream",
                            file.read().decode(),
                        )
                else:
                    response = response_data(Status.NOT_FOUND, data.version)
            elif data.path == "/user-agent":
                response = response_data(
                    Status.OK, data.version, "text/plain", data.user_agent
                )
            elif data.path == "/":
                response = response_data(Status.OK, data.version)
            else:
                response = response_data(
                    Status.NOT_FOUND,
                    data.version,
                )
            print(f"Data sent {response}")
            conn.sendall(response)


def main():
    print(
        f"Logs from your program will appear here! Starting server on localhost:4221..."
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default="")
    args = parser.parse_args()

    server = Server("localhost", 4221, args.directory)
    server.start()


if __name__ == "__main__":
    main()
