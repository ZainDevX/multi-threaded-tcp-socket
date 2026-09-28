import socket
import threading


# Server configuration
HOST = "127.0.0.1"
PORT = 5000

# Lock used to synchronize access to shared server resources
lock = threading.Lock()


def handle_client(client_socket, client_address):
    """
    Handle communication with a single client.

    Each connected client runs inside its own thread.
    """

    client_ip, client_port = client_address
    thread_name = threading.current_thread().name

    print(
        f"[{thread_name}] Client connected: "
        f"{client_ip}:{client_port}"
    )

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)

            # Empty data means the client disconnected
            if not data:
                break

            message = data.decode("utf-8")

            print(
                f"[{thread_name}] "
                f"{client_ip}:{client_port} -> {message}"
            )

            # Synchronize access to the shared response operation
            lock.acquire()

            try:
                response = f"Server received: {message}"
                client_socket.sendall(response.encode("utf-8"))
            finally:
                # Always release the lock
                lock.release()

    except ConnectionResetError:
        print(
            f"[{thread_name}] "
            f"Connection lost: {client_ip}:{client_port}"
        )

    except Exception as error:
        print(
            f"[{thread_name}] "
            f"Error while handling {client_ip}:{client_port}: {error}"
        )

    finally:
        # Close the client socket when the session ends
        client_socket.close()

        print(
            f"[{thread_name}] "
            f"Client disconnected: {client_ip}:{client_port}"
        )


def start_server():
    """Create and start the multi-threaded TCP server."""

    # Create a TCP socket using IPv4
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Allow the server to reuse the address after restarting
    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    # Bind the socket to the configured host and port
    server_socket.bind((HOST, PORT))

    # Start listening for incoming connections
    server_socket.listen()

    print("=" * 55)
    print("Multi-Threaded TCP Server")
    print("=" * 55)
    print(f"Server listening on {HOST}:{PORT}")
    print("Waiting for client connections...")
    print("Press Ctrl+C to stop the server.")
    print("=" * 55)

    try:
        while True:
            # Wait for a new client connection
            client_socket, client_address = server_socket.accept()

            # Create a dedicated thread for the new client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )

            # Start the client-handling thread
            client_thread.start()

            print(
                f"Active threads: "
                f"{threading.active_count()}"
            )

    except KeyboardInterrupt:
        print("\nServer shutting down...")

    finally:
        # Close the main server socket
        server_socket.close()
        print("Server stopped.")


if __name__ == "__main__":
    start_server()