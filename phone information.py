import platform
import socket

# Get basic OS information
os_info = platform.system(), platform.release(), platform.version()

# Get CPU architecture
cpu_arch = platform.machine()

# Get hostname and IP
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Print the gathered information
print(f"OS Info: {os_info}")
print(f"CPU Architecture: {cpu_arch}")
print(f"Host: {hostname}")
print(f"IP Address: {ip_address}")
