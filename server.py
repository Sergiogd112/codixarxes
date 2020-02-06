def do_some_stuffs_with_input(input_string):
    print("Processing that nasty input!")
    return input_string[::-1]


def client_thread(conn, ip, port, MAX_BUFFER_SIZE=4096):
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    import sys
    siz = sys.getsizeof(input_from_client_bytes)

    if siz >= MAX_BUFFER_SIZE:
        print('The lenght of the input is probably too long: {}'.format(siz))
    input_from_client = input_from_client_bytes.decode('utf8').rstrip()
    res = do_some_stuffs_with_input(input_from_client)
    print('Result of processing {} is: {}'.format(input_from_client, res))

    vysl = res.encode('utf8')
    conn.sendall(vysl)
    conn.close()
    print("Connection {} : {} ended".format(ip, port))


def start_server():
    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_STREAM, socket.SO_REUSEADDR, 1)

    try:
        soc.bind(('127.0.0.1', 12345))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error:' + str(sys.exc_info()))
        sys.exit()

    soc.listen()
    print('Socket now listening')

    from threading import Thread

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting Connection from' + ip + ':' + port)
        try:
            Thread(target=client_thread(), args=(conn, ip, port)).start()
        except:
            print('Terrible error!')
            import traceback
            traceback.print_exc()
    soc.close()


start_server()
