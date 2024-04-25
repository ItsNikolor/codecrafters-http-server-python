import socket
from time import sleep

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    print("Logs from your program will appear here!")

    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024).decode()
                print(f'Data = {data}')

                path = data.split('\r\n')[0].split(' ')[1]
                if path == '/':
                    conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
                else:
                    conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
                break
            
            
        # sleep(3)




if __name__ == "__main__":
    main()
