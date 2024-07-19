# System Setup
## SQL Setup
1. open SSMS
2. run the server query

## Backend
1. cd 'to/your/path'
2. git clone https://github.com/yikai03/AIDashboard.git
3. Open your project in vscode or any platform
4. cd ./backend
5. pip install -r requirements.txt
6. Download Ollama following https://ollama.com/
7. pip install ollama

## Frontend
1. cd ./frontend
2. npm install

# Starting System
## Backend
1. cd ./backend
2. uvicorn server:app

## Frontend
1. Open another terminal
2. cd ./frontend
3. npm run dev

> [!IMPORTANT]
Make sure your backend (localhost:8000) and frontend (localhost:3000) is both running

