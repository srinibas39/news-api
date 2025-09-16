# Deploying Your Flask Backend to Render

## 1. Prepare Your Code
- Ensure your `app.py`, `requirements.txt`, `Procfile`, and `.env.example` are present in the `python-backend` folder.
- Do NOT commit your real `.env` file with secrets. Use `.env.example` for sharing the structure.

## 2. Push to GitHub
- Initialize a git repo if needed:
  ```sh
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin <your-github-repo-url>
  git push -u origin main
  ```

## 3. Deploy on Render
- Go to https://render.com and sign in.
- Click "New +" → "Web Service".
- Connect your GitHub repo and select the `python-backend` folder.
- Set the build and start commands:
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn app:app`
- Add an environment variable:
  - `API_KEY` = your NewsData.io API key
- Click "Create Web Service" and wait for deployment.

## 4. Get Your Public URL
- After deployment, Render will give you a public URL (e.g., `https://your-backend.onrender.com`).
- Use this URL in your Chrome extension's `popup.js` for API requests.

---

## Troubleshooting
- If you get errors, check the Render logs for missing dependencies or environment variables.
- Make sure your `requirements.txt` includes `gunicorn`, `flask`, `requests`, `python-dotenv`, and `flask-cors`.
