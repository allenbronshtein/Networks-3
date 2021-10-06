# ________________________IMPORTS_______________________#

import sys
import socket
import os

# ________________________CONSTS_______________________#


FILES_DIR_STR = "files"
INDEX_HTML_STR = "files/index.html"
RESULT_HTML_STR = "files/result.html"
HTTP_OK_STR = "HTTP/1.1 200 OK\r\n"
HTTP_MOVED_STR = "HTTP/1.1 301 Moved Permanently\r\n"
HTTP_NOT_FOUND_STR = "HTTP/1.1 404 Not Found\r\n"
CONNECTION_STR = "Connection: "
CONNECTION_CLOSE_STR = "Connection: close"
CONTENT_LEN_STR = "Content-Length: "
LOCATION_RESULT_STR = "Location: /result.html\r\n\r\n"
BUFFER_SIZE = 1024
SUFFIX = "\r\n\r\n"


# _____________________FUNCTIONS_______________________#

def read_send_(directory):
    with open(directory, "rb") as f:
        content = f.read(BUFFER_SIZE)
        while content:
            client_socket.send(content)
            content = f.read(BUFFER_SIZE)


def read_send_bytes(directory):
    with open(directory, "rb") as f:
        content = f.read(BUFFER_SIZE)
        while content:
            client_socket.send(content)
            content = f.read(BUFFER_SIZE)


def message(mes):
    client_socket.send(mes.encode())


# ___________________________________________________ #
# ___________________________________________________ #
#                    MAIN START                       #
# ___________________________________________________ #
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '0.0.0.0'
server_port = int(sys.argv[1])
server.bind((server_ip, server_port))
server.listen(5)
while 1:
    client_socket, client_address = server.accept()
    try:
        client_socket.settimeout(1)
        print("Connection from: ", client_address)
        data = client_socket.recv(BUFFER_SIZE).decode()
        while not data == "":
            print(data)
            file_path = data.split("\n")[0].split()[1]
            connection_kind = data.split("\n")[2].split(":")[1][1:]
            # ~~~~~~~~~~~~~~~~~~~~~~START REQUEST INDEX.HTML~~~~~~~~~~~~~~~~~~~~~~~~~~#
            if file_path == "/":
                message(HTTP_OK_STR + CONNECTION_STR + connection_kind + '\r\n' + CONTENT_LEN_STR + str(
                    os.path.getsize(INDEX_HTML_STR)) + SUFFIX)
                read_send_(INDEX_HTML_STR)
            # ~~~~~~~~~~~~~~~~~~~~~~~~END REQUEST INDEX.HTML~~~~~~~~~~~~~~~~~~~~~~~~~~#

            # ~~~~~~~~~~~~~~~~~~~~~~~START REQUEST FILE READ~~~~~~~~~~~~~~~~~~~~~~~~~~#
            elif os.path.exists(FILES_DIR_STR + file_path):
                message(HTTP_OK_STR + CONNECTION_STR + connection_kind + '\r\n' + CONTENT_LEN_STR + str(
                    os.path.getsize(FILES_DIR_STR + file_path)) + SUFFIX)
                if ".jpg" in file_path or ".ico" in file_path:
                    read_send_bytes(FILES_DIR_STR + file_path)
                else:
                    read_send_(FILES_DIR_STR + file_path)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~END REQUEST FILE READ~~~~~~~~~~~~~~~~~~~~~~~~~~#

            # ~~~~~~~~~~~~~~~~~~~~~~~~START REQUEST REDIRECT~~~~~~~~~~~~~~~~~~~~~~~~~~#
            elif file_path == "/redirect":
                message(HTTP_MOVED_STR + CONNECTION_CLOSE_STR + '\r\n' + LOCATION_RESULT_STR)
                read_send_(RESULT_HTML_STR)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~END REQUEST REDIRECT~~~~~~~~~~~~~~~~~~~~~~~~~~#

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~START REQUEST 404~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            else:
                message(HTTP_NOT_FOUND_STR + CONNECTION_CLOSE_STR + SUFFIX)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END REQUEST 404~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

            data = client_socket.recv(BUFFER_SIZE).decode()
    except socket.timeout:
        print("No Response")
        client_socket.close()
# ___________________________________________________ #
#                     MAIN END                        #
# ___________________________________________________ #