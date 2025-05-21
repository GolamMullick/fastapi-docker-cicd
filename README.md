# 🚀 FastAPI + Docker + GitHub Actions CI/CD to AWS EC2

This project demonstrates how to build a FastAPI app, containerize it with Docker, push the image to Docker Hub, and deploy it automatically to an AWS EC2 instance using GitHub Actions.

---

## 🧰 Tech Stack

- Python 3.11
- FastAPI
- Docker
- GitHub Actions
- AWS EC2 (Ubuntu)

---

## 🔃 Clone the Repository

```bash
git clone https://github.com/golam1989/fastapi-docker-cicd.git
cd fastapi-docker-cicd
```

---

## 🚀 Run the App Locally with Docker

1. **Build the Docker Image**
   ```bash
   docker build -t golam1989/fastapi-profile .
   ```

2. **Run the Docker Container**
   ```bash
   docker run -d -p 8000:8000 golam1989/fastapi-profile
   ```

3. **Access the App**
   - Open in browser: [http://localhost:8000](http://localhost:8000)
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔄 GitHub Actions CI/CD Pipeline

Every push to the `main` branch will automatically:
- Build the Docker image
- Push it to Docker Hub
- SSH into your EC2 instance
- Pull the latest image
- Stop the old container
- Run the updated container

---

## 🔐 Required GitHub Secrets

Set these secrets in your GitHub repo:

| Secret Name       | Description                                      |
|-------------------|--------------------------------------------------|
| DOCKER_USERNAME   | Your Docker Hub username                         |
| DOCKER_PASSWORD   | Docker Hub password or personal access token      |
| EC2_HOST          | Public IP or DNS of your EC2 instance            |
| EC2_KEY           | Paste the full content of your `.pem` SSH key    |

---

## ⚙️ Setting Up the EC2 Instance (Ubuntu)

1. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

2. **Add the ubuntu user to the Docker group**
   ```bash
   sudo usermod -aG docker ubuntu
   sudo reboot
   ```
   After reboot, test:
   ```bash
   docker ps
   ```
   ✅ It should run without `sudo`.

3. **Open Required Ports in EC2 Security Group**

   Make sure these ports are open to `0.0.0.0/0` (or your IP):
   - 22 – for SSH
   - 80 – for HTTP (if running on port 80)
   - 8000 – for FastAPI (dev/test)

---

## 🌍 Access After Deployment

Once deployed via GitHub Actions, visit:

- `http://<your-ec2-public-ip>:8000`
- or `http://<your-ec2-public-ip>` (if container runs on port 80)