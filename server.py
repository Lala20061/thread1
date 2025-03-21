# Import necessary modules
import socket      # Provides low-level networking interface
import sys         # For system-specific parameters and functions
from concurrent.futures import ThreadPoolExecutor  # For managing a pool of threads

# Prompt the user to enter the host they wish to scan
host = input("Please enter the host name or IP address to scan: ")

# Define the range of ports to scan
start_port = 1      # Starting port number
end_port = 1024     # Ending port number
# Note: change end_port to 65535 to scan all possible ports

# Inform the user that the scan is starting
print(f"Starting scan on host {host} from port {start_port} to {end_port}")

# Define a function that will scan a single port
def scan_port(port):
    """
    Attempts to connect to the given host on the specified port.
    Prints a message if the port is open.
    """
    try:
        # Create a new socket using IPv4 and TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a timeout for the connection attempt to avoid hanging
        sock.settimeout(1)  # Timeout in seconds

        # Try to connect to the host on the specified port
        result = sock.connect_ex((host, port))
        if result == 0:
            # If the connection attempt returns 0, the port is open
            print(f"Port {port} is open")
        else:
            # If the connection attempt fails, the port is closed or filtered
            pass

        # Close the socket to free up the port
        sock.close()
    except KeyboardInterrupt:
        # Allow the user to interrupt the scan with Ctrl+C
        print("\nScanning interrupted by user.")
        sys.exit()
    except socket.gaierror:
        # Handle errors when the hostname couldn't be resolved
        print(f"Hostname '{host}' could not be resolved. Exiting.")
        sys.exit()
    except socket.error:
        # Handle other socket errors
        print(f"Couldn't connect to server '{host}'. Exiting.")
        sys.exit()

# Use a ThreadPoolExecutor to manage a pool of threads
# The 'with' statement ensures that resources are cleaned up promptly
with ThreadPoolExecutor(max_workers=100) as executor:
    # Submit scan_port tasks to the executor for each port in the specified range
    # max_workers specifies the maximum number of threads to run concurrently
    for port in range(start_port, end_port + 1):
        # Submit the scan_port function to be executed with the current port number
        executor.submit(scan_port, port)
        # Note: executor.submit schedules the function to be executed and returns immediately

# After all tasks are submitted, the executor waits for them to complete
# Once all threads have completed, the program continues here

# Inform the user that the scanning has completed
print("Scanning completed.")