# 🏦 Lootera Bank - Modern Digital Banking Application

A complete, clean, and modern banking web application built with Python Flask and modern HTML/CSS. Designed to look and feel like a real fintech product.

![Lootera Bank](https://img.shields.io/badge/Lootera-Bank-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![Python](https://img.shields.io/badge/Python-3.7+-yellow)

## ✨ Features

- 🔐 **Secure Login** - Account number + 4-digit PIN authentication
- 👤 **Account Creation** - Easy signup with initial deposit
- 💰 **Deposit Money** - Add funds to your account instantly
- 💸 **Withdraw Money** - Withdraw cash with balance validation
- 🔄 **Transfer Funds** - Send money to other accounts securely
- 📜 **Transaction History** - View complete transaction records
- 📱 **Mobile Responsive** - Works on all devices
- 💾 **Persistent Storage** - Data saved to local file

## 🛠 Tech Stack

- **Backend**: Python 3.7+, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Inter (Google Fonts)

## 📁 Project Structure

```
lootera-bank/
│
├── app.py                 # Flask application with all routes
├── accounts.txt           # Data storage file (auto-created)
├── README.md              # This file
├── requirements.txt       # Python dependencies
│
├── templates/             # HTML templates
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── create.html        # Account creation
│   ├── dashboard.html     # User dashboard
│   ├── deposit.html       # Deposit form
│   ├── withdraw.html      # Withdraw form
│   ├── transfer.html      # Transfer form
│   └── history.html       # Transaction history
│
└── static/
    └── style.css          # Modern fintech styling
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd lootera-bank
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to: `http://localhost:5000`

## 🎯 Usage Guide

### Creating an Account

1. Click "Create Account" or "Open Account" on the landing page
2. Enter your full name
3. Enter an initial deposit amount (minimum ₹1)
4. Set a 4-digit PIN
5. Confirm your PIN
6. Save your account number (displayed after creation)

### Logging In

1. Click "Login" on the landing page
2. Enter your 8-digit account number
3. Enter your 4-digit PIN
4. Click "Login"

### Making Transactions

**Deposit:**
- From dashboard, click "Deposit"
- Enter amount and confirm

**Withdraw:**
- From dashboard, click "Withdraw"
- Enter amount (must not exceed balance)
- Confirm withdrawal

**Transfer:**
- From dashboard, click "Transfer"
- Enter recipient's 8-digit account number
- Enter amount to transfer
- Confirm transfer

**View History:**
- From dashboard, click "History"
- View all your transactions with icons

## 🔒 Security Features

- Session-based authentication
- PIN validation (exactly 4 digits)
- Balance validation for withdrawals
- Self-transfer prevention
- Account number validation
- Input sanitization

## 🎨 Design Features

- Modern gradient color scheme (blue/green theme)
- Card-based layouts with shadows
- Smooth hover animations
- Responsive grid system
- Professional typography (Inter font)
- Font Awesome icons
- Flash message notifications
- Mobile-first responsive design

## 📝 API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/login` | GET/POST | Login page |
| `/create` | GET/POST | Create account |
| `/dashboard` | GET | User dashboard |
| `/deposit` | GET/POST | Deposit money |
| `/withdraw` | GET/POST | Withdraw money |
| `/transfer` | GET/POST | Transfer funds |
| `/history` | GET | View transactions |
| `/logout` | GET | Logout user |

## 💾 Data Format

Accounts are stored in `accounts.txt` with the following format:
```
account_number,name,balance,pin,history_entry1|history_entry2|...
```

Example:
```
12345678,John Doe,5000,1234,Account created with ₹5000|Deposited ₹1000
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Change port in app.py
app.run(debug=True, host="0.0.0.0", port=5001)
```

**Missing dependencies:**
```bash
pip install flask
```

**Data file issues:**
- Delete `accounts.txt` to reset all data
- The file will be recreated automatically

## 🔮 Future Enhancements

- [ ] Email notifications
- [ ] Password reset functionality
- [ ] Account statement PDF export
- [ ] Multi-currency support
- [ ] Bill payments
- [ ] Mobile app (React Native/Flutter)
- [ ] Database integration (PostgreSQL/MySQL)

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- Built with [Flask](https://flask.palletsprojects.com/)
- Icons by [Font Awesome](https://fontawesome.com/)
- Fonts by [Google Fonts](https://fonts.google.com/)

---

**Made with ❤️ by Lootera Bank Team**

*Secure. Fast. Modern Banking.*
