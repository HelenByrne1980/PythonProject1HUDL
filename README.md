# HUDL Login Automation

This project automates the login process for [hudl.com](https://www.hudl.com) using Selenium WebDriver in Python. It includes:

- Handling cookie and privacy popups
- Secure credential storage using a  file
- Login verification with screenshot capture
- Screenshot output saved with timestamps

## Setup

1. Clone this repo
2. Create a  file with your credentials:

HUDL_EMAIL=your-email@example.com
HUDL_PASSWORD=your-password

markdown
Copy
Edit

3. Install dependencies:

pip install -r requirements.txt

markdown
Copy
Edit

4. Run the script:

python main.py

markdown
Copy
Edit

## Notes

- Do **not** commit  files
- Uses  to auto-manage ChromeDriver
- Screenshots will be saved in the  folder

