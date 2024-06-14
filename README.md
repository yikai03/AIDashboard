# System Setup
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

## Gemini API Key
1. go to https://aistudio.google.com/app/apikey
2. create an API key
3. create a .env file in backend folder
4. enter GENAI_API_KEY = <Your API key>
5. ensure the .gitignore file have .env written

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

