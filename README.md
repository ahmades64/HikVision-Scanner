# HikVision-Scanner
HikVision Scanner is a Python-based tool designed to scan a given IP range, detect HikVision security cameras, and attempt authentication using default credentials. This tool is useful for network administrators and security researchers to identify vulnerable devices and ensure they are properly secured.
HikVision Scanner - Description

✅ IP Range Scanning: Quickly scans a specified range of IP addresses to identify active HikVision cameras.
✅ Port Checking: Tests common HikVision camera ports (80, 554, 8000) to determine if a device is accessible.
✅ Device Detection: Uses HikVision-specific API endpoints (/ISAPI/Security/userCheck, /ISAPI/System/deviceInfo) to confirm if an IP belongs to a HikVision camera.
✅ Authentication Testing: Attempts login using default credentials (admin:admin12345) via HTTP Basic Authentication.
✅ Logging: Saves identified camera IPs and successful logins to text files for further analysis.
How It Works:

    The user inputs the start and end IP range.
    The script scans each IP to check if HikVision-related ports are open.
    If an open port is found, the tool sends requests to HikVision API endpoints to verify if the device is a HikVision camera.
    If a HikVision camera is detected, the script attempts authentication using a predefined list of usernames and passwords.
    Successful logins are saved in a separate file (successful_hikvision_logins.txt).

Legal Disclaimer:

This tool is intended for educational and security research purposes only. Unauthorized access to systems you do not own or have explicit permission to test is illegal and unethical. The developer is not responsible for any misuse of this tool.
Installation & Usage:

    Clone the repository:

git clone https://github.com/ahmades64/HikVision-Scanner.git
cd HikVision-Scanner

Install dependencies:

pip install requests

Run the scanner:

    python HikVisionScanner.py

Make sure you have permission before scanning any network! 🚀
