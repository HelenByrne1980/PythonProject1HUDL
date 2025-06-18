# HUDL Login Automation

This project automates login validation for [hudl.com](https://www.hudl.com) using Selenium in Python. It includes tests for:

- ✅ Successful login
- ❌ Invalid email
- ❌ Invalid password
- ❌ Blank email field

---

## 📁 Project Structure

```
PythonProject1HUDL/
├── .env.template          # Example environment file (no secrets committed)
├── .gitignore
├── README.md
├── requirements.txt       # Dependencies
├── utils/
│   └── driver_setup.py    # Shared setup for WebDriver and WebDriverWait
└── tests/
    ├── test_valid_login.py
    ├── test_invalid_email.py
    ├── test_invalid_password.py
    └── test_blank_email.py
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/HelenByrne1980/PythonProject1HUDL.git
cd PythonProject1HUDL
```

2. **Create a `.env` file**
```bash
cp .env.template .env
```
Then update it with your valid Hudl email and password:
```
HUDL_EMAIL=your-email@domain.com
HUDL_PASSWORD=your-password
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run tests**
```bash
python tests/test_valid_login.py
python tests/test_invalid_email.py
python tests/test_invalid_password.py
python tests/test_blank_email.py
```

---

## 🔒 Security

- The `.env` file is excluded via `.gitignore` and never pushed.
- A `.env.template` is provided for safe sharing.

---

## 🧪 Tech Stack

- Python
- Selenium
- WebDriver Manager
- dotenv
- PyCharm

---

## 🤝 Author

**Helen Byrne**  
[GitHub Profile](https://github.com/HelenByrne1980)


