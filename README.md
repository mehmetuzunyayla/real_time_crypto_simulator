# 🚀 Real-Time Crypto Trading Simulator

Welcome to the **Real-Time Crypto Trading Simulator**, a full-stack web application that allows users to trade cryptocurrencies in real time using live price data. This project features a **Flask backend** and a **React frontend**, along with **WebSocket integration** for live price updates.

## 🌟 Features
- **Live Cryptocurrency Price Updates** (via WebSocket)
- **Spot Trading** (Buy & Sell Coins)
- **Wallet Balance Tracking**
- **Trade History with PnL Calculation**
- **User Authentication (JWT-based)**
- **Deposit Funds ($1000 Button)**
- **Dynamic Price Validation (±1% of Live Price Allowed)**
- **Dark Mode UI with Bootstrap Styling**

---

## 🛠 Tech Stack
- **Backend**: Flask, Flask-SocketIO, SQLAlchemy, PostgreSQL
- **Frontend**: React.js, Bootstrap
- **Database**: PostgreSQL
- **WebSockets**: Live price updates via Binance API

---

## 🚀 Installation Guide

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/mehmetuzunyayla/real_time_crypto_simulator.git
cd crypto-trade-simulator
```

### **2️⃣ Backend Setup (Flask)**
#### **🔹 Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

#### **🔹 Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **🔹 Configure Environment Variables**
Create a `.env` file in the backend directory and set:
```env
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/crypto_db
```

#### **🔹 Run Flask Backend**
```bash
flask db upgrade  # Apply database migrations
flask run  # Start the server
```

---

### **3️⃣ Frontend Setup (React.js)**
#### **🔹 Install Dependencies**
```bash
cd frontend
npm install
```

#### **🔹 Start React App**
```bash
npm start
```

---

## 📌 Usage Instructions
1. **Register/Login** to the application.
2. **Deposit Funds** using the `$1000 Deposit` button in the profile.
3. **Select a Coin** from the dropdown menu.
4. **Check Live Price Updates** in the chart.
5. **Place Trades** (Buy/Sell coins with price validation).
6. **Monitor Wallet & Trade History** (PnL calculation updates dynamically).

---

## 📸 Screenshots
#### **🔹 Home Page (Live Prices)**
![Home Page](screenshots/homepage.png)

#### **🔹 Trading Page**
![Trade Page](screenshots/tradepage.png)

#### **🔹 Profile Page**
![Profile Page](screenshots/profilepage.png)

---

## ⚡ API Endpoints

### **🔹 Authentication**
- `POST /auth/register` → Register a new user
- `POST /auth/login` → Login user (JWT token)

### **🔹 Wallet**
- `GET /wallets/` → Get user wallet info
- `POST /wallets/update` → Deposit funds

### **🔹 Trades**
- `POST /trades/` → Execute a trade
- `GET /trades/history` → Fetch trade history
- `POST /trades/{trade_id}/close` → Close a trade

### **🔹 Price Updates (WebSocket)**
- Connects to `ws://127.0.0.1:5000/price_update`
- Receives `{ coin_symbol: { price: value } }`

---

## 🎯 Future Improvements
- **Stop-Loss & Take-Profit Orders**
- **More Intervals**
- **Future Trades**
- **Advanced Chart Indicators**
- **More Trading Strategies**
- **Real API Trading Mode**

---

## 📜 License
This project is **open-source** and available under the [MIT License](LICENSE).

---

## 🤝 Contributing
Feel free to **fork** this repo and contribute!
```bash
git clone https://github.com/mehmetuzunyayla/real_time_crypto_simulator.git
```
1. Create a new branch (`git checkout -b feature-branch`)
2. Make changes and commit (`git commit -m "Added a new feature"`)
3. Push to GitHub (`git push origin feature-branch`)
4. Open a **Pull Request** 🚀

---

## 🌟 Acknowledgements
- **Binance API** for price updates
- **Flask-SocketIO** for WebSockets
- **React.js** for the frontend

---


