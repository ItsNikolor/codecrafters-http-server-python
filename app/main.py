import socket
from time import sleep


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("localhost", 4221))
        server_socket.listen()
        server_socket.accept()

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            # while True:
            data = conn.recv(1024)
            # if not data:
            #     break
            conn.sendall('HTTP/1.1 200 OK\r\n\r\n')
        sleep(3)



    # server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client

    

    # server_socket.close()


if __name__ == "__main__":
    main()
