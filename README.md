# 🚀 FastAPI App with Docker & CI/CD on AWS EC2

This project demonstrates how to build a **FastAPI** application, containerize it with **Docker**, and deploy it automatically to an **AWS EC2** instance using **GitHub Actions** CI/CD pipeline.

---

## 🧰 Tech Stack

- 🐍 Python 3.11
- ⚡ FastAPI
- 🐳 Docker
- ☁️ AWS EC2 (Ubuntu)
- 🔁 GitHub Actions

---

## 📂 Project Structure

.
├── app/
│ └── main.py # FastAPI application
├── requirements.txt # Python dependencies
├── Dockerfile # Docker build instructions
├── .github/
│ └── workflows/
│ └── deploy.yml # GitHub Actions CI/CD pipeline
└── README.md

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
2. Run locally (optional)
bash
Copy
Edit
pip install -r requirements.txt
uvicorn main:app --reload
3. Build & Run Docker locally
bash
Copy
Edit
docker build -t fastapi-profile .
docker run -d -p 80:80 fastapi-profile