# 🤖 Gemini AI Multi-Tool Workspace

A Streamlit web app that wraps the Google GenAI SDK (Gemini) into three handy tools:

- **💬 Basic Chat** — ask Gemini anything
- **✉️ Smart Email Writer** — generate ready-to-send emails from structured inputs (recipient, tone, purpose, key points)
- **💻 Code Explainer & Debugger** — explain a code snippet step-by-step, or identify and fix bugs

---

## 1. Requirements

- Python 3.9+
- A Google AI Studio API key (Gemini)

### Python dependencies

Create a `requirements.txt` with:

```
streamlit
python-dotenv
google-genai
```

Install them:

```bash
pip install -r requirements.txt
```

---

## 2. Getting a Gemini API Key from Google AI Studio

1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click **Get API key** (usually in the left sidebar or under your profile menu).
4. Click **Create API key**, and choose an existing Google Cloud project or let Google create one for you.
5. Copy the generated key — it will look something like `AIzaSy...`.
6. Keep it secret. Treat it like a password; don't commit it to version control.

> Note: Google AI Studio API keys are tied to a Google Cloud project and may incur usage costs once free quota is exceeded. Check the current pricing/quota in [AI Studio's billing page](https://aistudio.google.com/) before heavy use.

### Set up your `.env` file

In the project root, create a file named `.env`:

```
GEMINI_API_KEY=your_api_key_here
```

The `google-genai` SDK's `genai.Client()` automatically picks up the key from the `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) environment variable, which `python-dotenv`'s `load_dotenv()` loads into the environment at startup.

---

## 3. Running Locally

```bash
streamlit run app.py
```

Replace `app.py` with whatever you've named the script containing this code. Streamlit will start a local server, usually at `http://localhost:8501`.

---

## 4. Running with Docker

### 4.1 Project structure

```
.
├── app.py
├── requirements.txt
├── .env                # not copied into the image — passed at runtime
└── Dockerfile
```

### 4.2 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0"]
```

> If `curl` isn't available in the slim image and you want the healthcheck to work, add `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*` before `EXPOSE`.

### 4.3 .dockerignore

Create a `.dockerignore` to keep the image lean and avoid baking in secrets:

```
.env
__pycache__/
*.pyc
.git
.venv
```

### 4.4 Build the image

```bash
docker build -t gemini-multitool .
```

### 4.5 Run the container

Pass your API key as an environment variable at runtime rather than baking it into the image:

```bash
docker run -d \
  --name gemini-multitool \
  -p 8501:8501 \
  -e GEMINI_API_KEY=your_api_key_here \
  gemini-multitool
```

Then open `http://localhost:8501` in your browser.

### 4.6 Using docker-compose (optional)

`docker-compose.yml`:

```yaml
version: "3.8"
services:
  gemini-multitool:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d --build
```

This keeps your `.env` file out of the image while still supplying it to the container at runtime.

---

## 5. App Overview

| Tab | Function | Description |
|---|---|---|
| Basic Chat | `basic_chat(prompt_text)` | Sends a free-form prompt to `gemini-2.5-flash` and displays the response. |
| Smart Email Writer | `write_email(...)` | Builds a structured prompt from purpose, recipient, tone, key points, and sender name, then returns a ready-to-send email. |
| Code Explainer & Debugger | `explain_code(...)` | Switches between an "explain" mode (step-by-step walkthrough) and a "debug" mode (finds and fixes bugs) based on a system instruction. |

All three features use the `google-genai` SDK's `client.models.generate_content()` call against the `gemini-2.5-flash` model.

---

## 6. Troubleshooting

- **`ValueError` / authentication errors**: confirm `GEMINI_API_KEY` is set and valid, and that `.env` is in the same directory you're running the app from (or passed correctly into the container).
- **Blank responses**: check your API quota/usage in Google AI Studio; you may have hit a rate limit.
- **Docker container exits immediately**: run `docker logs gemini-multitool` to see the Streamlit error output.
