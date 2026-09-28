import socket


# Server configuration
HOST = "127.0.0.1"
PORT = 5000


def start_client():
    """Connect to the TCP server and continuously exchange messages."""

    # Create a TCP socket using IPv4
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))

        print("=" * 50)
        print("TCP Client")
        print("=" * 50)
        print(f"Connected to server at {HOST}:{PORT}")
        print("Type 'exit' to close the connection.")
        print("=" * 50)

        while True:
            # Get a message from the user
            message = input("You: ")

            # Exit the communication loop when requested
            if message.lower() == "exit":
                print("Closing connection...")
                break

            # Send the message to the server
            client_socket.sendall(
                message.encode("utf-8")
            )

            # Receive the server response
            response = client_socket.recv(1024)

            # Stop if the server closes the connection
            if not response:
                print("Server closed the connection.")
                break

            print(f"Server: {response.decode('utf-8')}")

    except ConnectionRefusedError:
        print(
            "Unable to connect to the server. "
            "Make sure server.py is running first."
        )

    except ConnectionResetError:
        print("The server closed the connection unexpectedly.")

    except KeyboardInterrupt:
        print("\nClient interrupted by user.")

    except Exception as error:
        print(f"An error occurred: {error}")

    finally:
        # Always close the client socket
        client_socket.close()
        print("Client connection closed.")


if __name__ == "__main__":
    start_client()