# PPPoEHelper
<<<<<<< HEAD
# PPPoEHelper
=======
# PPPoEHelper

This Python script automates the process of configuring, starting, and monitoring a PPPoE server. It parses the PPPoE server logs to extract and display user credentials (username and password).

## Features

- Checks if PPPoE server is installed and installs it if necessary.
- Configures the PPPoE server with essential options.
- Starts the PPPoE server on a specified network interface.
- Monitors the server log file for user credentials.
- Cleans up temporary files after execution.

## Requirements

- Linux-based operating system.
- Root privileges.
- Python 3.
- PPPoE server package installed (automatically installed by the script if missing).

To install additional Python dependencies, run:

```bash
pip install -r requirements.txt
```

## Hardware Setup

Before running the script, ensure the following hardware setup:

1. Connect an Ethernet cable to the WAN port of your modem/router.
2. Plug the other end of the Ethernet cable into your computer.
3. Identify which Ethernet interface (e.g., `eth0`, `eth1`) corresponds to the connected cable. This will be selected during script execution.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/pppoe-helper.git
cd pppoe-helper
```

2. Ensure the script has executable permissions:

```bash
chmod +x pppoe.py
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script as root:

```bash
sudo python3 pppoe.py
```

### Steps in the Script

1. **Check PPPoE Server**: The script checks if the PPPoE server is installed. If not, it attempts to install it.
2. **Configure Server**: Creates a configuration file for the PPPoE server at `/etc/ppp/pppoe-server-options`.
3. **Start Server**: Starts the PPPoE server on the selected network interface.
4. **Monitor Logs**: Monitors the log file at `/var/log/pppoe-server-log` for user credentials.
5. **Display Credentials**: Once found, displays the username and password.
6. **Clean Up**: Deletes the configuration and log files after execution.

### Example Output

```plaintext
Checking if PPPoE server is installed...
PPPoE server is installed.
Enter the network interface (e.g., eth1): eth1
PPPoE server started successfully!
Waiting for log file to be created at /var/log/pppoe-server-log...
Log file detected!

[Credentials Found]
Kullanıcı Adı: user@example
Parola: password123

Cleaning up...
Deleted: /etc/ppp/pppoe-server-options
Deleted: /var/log/pppoe-server-log
```

## Notes

- Ensure the Ethernet cable is properly connected.
- Choose the correct network interface during script execution.
- The script must be run with root privileges.

## Disclaimer

This script is for educational and internal use only. Use it responsibly and ensure compliance with all applicable laws and regulations.
>>>>>>> f15e355 (Initial commit: PPPoE Helper tool)

