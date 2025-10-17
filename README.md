

https://github.com/user-attachments/assets/28a76625-b41e-42dc-a099-9e2d1c39ce61

# Healthcare Symptom Checker

A full-stack web application that helps users check symptoms and get AI-powered insights using **GroqCloud API** with **Llama 3.1** model. Built with **FastAPI** for backend and **React + Vite** for frontend.  

---

## Features

- Input symptoms and receive AI-generated healthcare suggestions.
- Interactive frontend built with React + Vite.
- Backend API powered by **FastAPI** and **GroqCloud Llama 3.1**.
- Secure storage of API keys using `.env` files.
- Modular prompt templates for flexible AI responses.

---

## Tech Stack

**Frontend:**  
- React.js  
- Vite  
- Axios (for API requests)  

**Backend:**  
- Python 3.11+  
- FastAPI  
- Uvicorn (ASGI server)  
- GroqCloud API (Llama 3.1)  

**Other:**  
- dotenv for environment variables  
- Git for version control  

---

## Project Structure

```
healthcare/
├─ backend/ # FastAPI backend
│ ├─ app.py # Main API file
│ ├─ requirements.txt
│ └─ .env # API keys (ignored by Git)
├─ frontend/ # React + Vite frontend
│ ├─ src/
│ ├─ public/
│ ├─ package.json
│ └─ vite.config.js
├─ .gitignore
└─ README.md
```
## Getting Started

### **Backend**

1. Create a virtual environment:
  ``` bash
python -m venv venv
```
2. Activate it:
``` bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```
3.Install dependencies:
``` bash
pip install -r backend/requirements.txt
```
4.Add your .env file inside backend/ with your Groq API key:
``` bash
GROQ_API_KEY=your_api_key_here
```
5.Run the backend server:
``` bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
### **Frontend**
1.Navigate to the frontend folder:
``` bash
cd frontend
```
2.Install dependencies:
``` bash
npm install
```
3.Run the frontend:
``` bash
npm run dev
```
4.Open the app in your browser:
``` bash
http://localhost:5173
```
## output:

<img width="992" height="355" alt="image" src="https://github.com/user-attachments/assets/df4edf39-42b7-44e4-9754-88ffe86e086b" />
<img width="994" height="922" alt="image" src="https://github.com/user-attachments/assets/0707b583-79a5-48e0-ad3e-c3bf42da2b55" />


## Usage
1) Enter your symptoms in the input field.
2) The AI will process your input and give suggestions based on the prompt templates.
3) All API requests are handled securely via the backend.

## Security
1) Do NOT commit .env files containing API keys.
2) Use environment variables or GitHub secrets for deployment.

## Contributing
1) Fork the repository.
2) Create a new branch (git checkout -b feature-name).
3) Make your changes.
4) Commit and push (git commit -m "Add feature" && git push).
5) Open a Pull Request.
