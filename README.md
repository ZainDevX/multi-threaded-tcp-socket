# Multi-Threaded TCP Socket Programming

A Python-based client-server networking project demonstrating **TCP socket programming, concurrent client handling, and thread synchronization** using Python's built-in `socket` and `threading` modules.

This project implements a TCP server capable of handling multiple clients simultaneously. Each connected client is assigned a dedicated worker thread, while a synchronization lock protects shared server resources from concurrent access.

---

## Overview

Traditional single-threaded servers process one client at a time, which can cause other clients to wait while an active connection is being handled.

This project addresses that limitation by using a **multi-threaded server architecture**:

```text
                    ┌─────────────────────┐
                    │     TCP Server      │
                    │                     │
                    │  Listening Socket   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌───────────┐    ┌───────────┐
        │ Client 1  │    │ Client 2  │    │ Client 3  │
        │ Thread-1  │    │ Thread-2  │    │ Thread-3  │
        └───────────┘    └───────────┘    └───────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                         Shared Resources
                               │
                         Threading Lock
```

For every incoming connection, the server creates a new `threading.Thread()` instance. This allows multiple clients to communicate with the server concurrently without blocking one another.

---

## Key Features

- TCP-based client-server communication
- Multi-client concurrent connection handling
- Dedicated thread for every connected client
- Continuous two-way message exchange
- Graceful client disconnection
- Thread-safe access to shared resources
- `Lock.acquire()` / `Lock.release()` synchronization
- Client IP address and port tracking
- Active thread identification
- Clean separation between server and client implementations
- Built entirely with Python's standard library

---

## Project Structure

```text
multi-threaded-tcp-socket/
│
├── server.py
├── client.py
└── README.md
```

### `server.py`

Responsible for:

- Creating the TCP listening socket
- Binding the server to a host and port
- Accepting incoming client connections
- Creating a dedicated thread for each client
- Receiving and responding to messages
- Displaying client network information
- Managing synchronized shared resources
- Handling client disconnections

### `client.py`

Responsible for:

- Establishing a TCP connection with the server
- Continuously sending user messages
- Receiving server responses
- Maintaining the communication session
- Allowing the user to terminate the connection gracefully

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| `socket` | TCP network communication |
| `threading` | Concurrent client handling |
| `threading.Thread` | Dedicated worker thread per client |
| `threading.Lock` | Thread synchronization |
| TCP/IP | Reliable client-server communication |

No external Python packages are required.

---

# How It Works

## 1. Server Initialization

The server creates a TCP socket using:

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Where:

- `AF_INET` specifies IPv4 addressing.
- `SOCK_STREAM` specifies TCP communication.

The socket is then bound to the configured host and port and placed into listening mode.

---

## 2. Accepting Clients

The server continuously waits for incoming connections:

```python
client_socket, client_address = server_socket.accept()
```

When a client connects, the server receives:

- Client socket
- Client IP address
- Client port number

The server then creates a new worker thread for that connection.

Conceptually:

```text
Incoming Connection
        │
        ▼
   accept()
        │
        ▼
Create Thread
        │
        ▼
handle_client()
```

---

## 3. Multi-Threaded Client Handling

Each connected client is handled independently through a dedicated thread.

```python
client_thread = threading.Thread(
    target=handle_client,
    args=(client_socket, client_address)
)

client_thread.start()
```

This means the main server thread can immediately return to listening for additional connections while the newly created worker thread handles the client.

For example:

```text
Main Server Thread
       │
       ├── Client A → Thread-1
       │
       ├── Client B → Thread-2
       │
       ├── Client C → Thread-3
       │
       └── Client D → Thread-4
```

This architecture allows several clients to communicate with the server at the same time.

---

# Thread Synchronization

Because multiple worker threads can execute concurrently, shared resources may be accessed by more than one thread at the same time.

To prevent race conditions, the project uses Python's `threading.Lock`.

A shared resource can be protected using:

```python
lock.acquire()

try:
    # Access shared resource
    ...
finally:
    lock.release()
```

The lock ensures that only one thread enters the protected section at a time.

### Synchronization Flow

```text
Thread A ──► acquire() ──► Critical Section ──► release()
                                                  │
Thread B ──► waits ──────────────────────────────┘
                                                  │
                                                  ▼
                                          Thread B acquires lock
```

This provides controlled access to shared server resources and reduces the possibility of inconsistent state caused by concurrent execution.

---

# Client Communication

The client maintains an interactive communication loop.

The user can continuously:

1. Enter a message.
2. Send it to the server.
3. Receive the server's response.
4. Continue communicating.
5. Exit when finished.

Conceptually:

```text
User Input
    │
    ▼
Client Socket
    │
    ▼
TCP Network
    │
    ▼
Server Worker Thread
    │
    ▼
Server Response
    │
    ▼
Client
    │
    └──────► Continue
```

The connection remains active until the user explicitly chooses to terminate the session.

---

# Server Information Display

For every active connection, the server displays useful connection information such as:

```text
Thread Name
Client IP Address
Client Port Number
```

Example:

```text
[Thread-1] Client connected: 127.0.0.1:54321
[Thread-2] Client connected: 127.0.0.1:54322
```

This makes the concurrent execution model visible during testing and demonstrates that different clients are being handled by separate threads.

---

# Running the Project

## Requirements

Make sure Python 3 is installed:

```bash
python --version
```

or:

```bash
python3 --version
```

No third-party dependencies are required.

---

## Step 1 — Start the Server

Open a terminal and run:

```bash
python server.py
```

The server will start listening for incoming TCP connections.

Example:

```text
Server started on 127.0.0.1:5000
Waiting for connections...
```

Keep this terminal running.

---

## Step 2 — Start a Client

Open another terminal:

```bash
python client.py
```

The client will establish a TCP connection with the server.

---

## Step 3 — Connect Multiple Clients

To demonstrate concurrent execution, open additional terminals and run:

```bash
python client.py
```

multiple times.

For example:

```text
Terminal 1 → Server
Terminal 2 → Client 1
Terminal 3 → Client 2
Terminal 4 → Client 3
```

The server should create a separate worker thread for each connected client.

---

# Testing Concurrent Connections

A basic concurrency test can be performed by running several clients simultaneously.

Expected server-side behavior:

```text
Server started...
Waiting for connections...

[Thread-1] Client connected: 127.0.0.1:xxxxx
[Thread-2] Client connected: 127.0.0.1:xxxxx
[Thread-3] Client connected: 127.0.0.1:xxxxx
```

Each client should be able to exchange messages independently while the other clients remain connected.

This demonstrates that the server is not restricted to processing a single client at a time.

---

# Terminal Output


### Server Output

<p align="center">
  <img
    src="https://github.com/user-attachments/assets/4dde5f5b-4ac4-4d73-a178-f09a908b5559"
    alt="Multi-threaded TCP server and client demonstration"
    width="700"
  />
</p>

### Client 1 Output

<p align="center">
  <img
    src="https://github.com/user-attachments/assets/c0f0ad4a-fe50-4aef-bfd0-cbb51010c23b"
    alt="Multi-threaded TCP server and client demonstration"
    width="700"
  />
</p>

### Client 2 Output

<p align="center">
  <img
    src="https://github.com/user-attachments/assets/152e7a26-c84a-4aca-b2ee-30c8220fb225"
    alt="Multi-threaded TCP server and client demonstration"
    width="700"
  />
</p>


### Screenshots

Add screenshots demonstrating:

- Server running
- Multiple clients connected simultaneously
- Different thread names
- Client IP addresses and port numbers
- Successful message exchange
- Graceful client disconnection

---

# Concurrency Model

The project uses a **thread-per-client** concurrency model.

```text
                    TCP Server
                        │
                  accept connection
                        │
             ┌──────────┴──────────┐
             │                     │
        Client 1               Client 2
             │                     │
          Thread-1              Thread-2
             │                     │
             ▼                     ▼
        Message Loop          Message Loop
             │                     │
             └──────────┬──────────┘
                        │
                  Shared Resource
                        │
                  Threading Lock
```

The main server thread is responsible for accepting connections, while worker threads handle individual client sessions.

This separation allows the server to remain responsive to new connection requests.

---

# Why Thread Synchronization Is Required

When multiple threads operate concurrently, they may attempt to modify or access shared data at the same time.

For example:

```text
Thread A ──┐
           ├──► Shared Resource
Thread B ──┤
           │
Thread C ──┘
```

Without synchronization, simultaneous access can produce a **race condition**, where the final state depends on the unpredictable order in which threads execute.

Using a lock:

```text
Thread A ──► LOCK ──► Shared Resource ──► UNLOCK
                                              │
Thread B ─────────────────────────────────────┘
```

ensures controlled access to the critical section.

---

# TCP Communication

This project uses **TCP (Transmission Control Protocol)** rather than UDP.

TCP provides:

- Connection-oriented communication
- Reliable data delivery
- Ordered data transmission
- Error detection and retransmission
- Persistent communication between client and server

The communication flow is:

```text
Client                         Server
  │                              │
  │──── TCP Connection ─────────►│
  │                              │
  │──── Message ────────────────►│
  │                              │
  │◄──── Response ───────────────│
  │                              │
  │──── Message ────────────────►│
  │                              │
  │◄──── Response ───────────────│
  │                              │
  │──── Disconnect ─────────────►│
  │                              │
```

---

# Learning Outcomes

This project demonstrates practical understanding of:

- TCP socket programming
- Client-server architecture
- IPv4 networking
- Python socket APIs
- Python multithreading
- Concurrent connection handling
- Thread lifecycle management
- Thread synchronization
- Mutual exclusion using locks
- Race-condition prevention
- Network debugging using IP addresses and ports
- Designing a continuously running network service

---

# Challenges Addressed

### Single Client Limitation

A basic sequential server can become blocked while communicating with one client.

**Solution:**  
Create a dedicated thread for every client connection.

### Concurrent Access to Shared Data

Multiple worker threads may access shared resources simultaneously.

**Solution:**  
Use `threading.Lock` around critical sections.

### Connection Management

Clients may disconnect unexpectedly or terminate their sessions.

**Solution:**  
Handle connection termination gracefully and release associated resources.

---

# Project Demonstration

The final demonstration should show that:

- The server starts successfully.
- Multiple clients can connect at the same time.
- Each client receives its own worker thread.
- Thread names are visible in the server terminal.
- Client IP addresses and port numbers are displayed.
- Multiple clients can exchange messages concurrently.
- Synchronization is performed using a lock.
- Clients can terminate their sessions without crashing the server.

---

# Academic Context

**Course:** Parallel and Distributed Computing  
**Course Code:** CSC-334  
**Lab:** 03 — Socket Programming with Multi-Threading

The implementation focuses on applying concepts of **concurrency, parallel execution, inter-thread synchronization, and network communication** in a practical client-server environment.

---

# Conclusion

This project provides a practical implementation of a concurrent TCP server using Python's standard networking and threading capabilities.

By assigning each client connection to an independent worker thread and protecting shared resources through synchronization locks, the system demonstrates the fundamental principles behind **multi-threaded network services**.

The project serves as a compact example of how socket programming and concurrency can be combined to build a responsive server capable of handling multiple clients simultaneously.

---

## Author

**Zain**

Computer Science / Software Engineering Student

> This project was developed as part of the Parallel and Distributed Computing coursework and is structured to demonstrate practical implementation of TCP socket programming, multi-threading, and thread synchronization.