import socket
from time import sleep

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    print("Logs from your program will appear here!")


    logger.info('Im here')
    print('Im here')

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    with socket.create_server(("localhost", 4221), reuse_port=True) as server_socket:
        logger.info('Im here')
        print('Im here')

        # server_socket.bind(("localhost", 4221))
        # server_socket.listen()
        server_socket.accept()

        logger.info('Im here')
        print('Im here')
        conn, addr = server_socket.accept()
        logger.info('Connected by {}'.format(addr))
        with conn:
            print(f"Connected by {addr}")
            # while True:
            data = conn.recv(1024)
            # if not data:
            #     break
            conn.sendall('HTTP/1.1 200 OK\r\n\r\n')
        sleep(3)



if __name__ == "__main__":
    main()
