# 📝 Django Blog Final

Welcome to the **final version** of a Django-based blog application!  
This project is designed with modularity, scalability, and best practices in mind — perfect for learning or production-ready use. 🧠🚀

---

## ✨ Features

- 🧱 Modular Django app structure
- 🐳 Docker & Docker Compose integration
- 🌐 Nginx reverse proxy (no need to specify port in browser)
- 📜 API schema with `api.json` and `schema.yaml`
- 🗂️ Database diagram (`dbdiagram.png`)
- 🔁 GitHub Actions CI/CD workflow

---

## ⚙️ Prerequisites

Make sure you have the following installed:

- 🐳 [Docker](https://www.docker.com/)
- 🧩 [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/sdgmhz/djnago_blog_final.git
cd djnago_blog_final

Build and start the app using Docker Compose:
docker-compose up --build

The application should now be accessible in your browser at:
http://localhost
Thanks to the built-in Nginx reverse proxy, you don't need to specify any port manually. 🌐✨

🗂️ Project Structure
djnago_blog_final/
├── core/                  # 🧩 Main Django app
├── .github/workflows/     # ⚙️ GitHub Actions CI/CD
├── nginx/                 # 🌐 Nginx configuration
├── Dockerfile             # 🐳 Django app container
├── docker-compose.yml     # 📦 Multi-container orchestration
├── requirements.txt       # 📦 Python dependencies
├── api.json               # 📄 API schema (JSON)
├── schema.yaml            # 📄 Data schema (YAML)
├── dbdiagram.png          # 🧬 Database structure diagram
└── ...

🤝 Contributing
Interested in contributing?
Fork the repo, make your changes, and submit a pull request. Contributions are always welcome! 💡

📄 License
This project is licensed under the MIT License.
See the LICENSE file for full details. 📜
