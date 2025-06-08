# Threads Video Downloader

A tool to extract downloadable video links from Threads posts. The backend is powered by FastAPI and Playwright, and the frontend is a minimal, SEO-friendly static website styled to resemble the Threads app.

## Usage

1. **Run the FastAPI backend:**
   ```bash
   uvicorn app:app --reload
   ```
2. **Serve the static website:**
   - You can use any static file server (e.g., Vercel, Netlify, GitHub Pages, or Python's `http.server`).
   - The frontend will POST to the FastAPI backend at `/extract`.

## Features
- Paste a Threads post URL and get a downloadable video link.
- Progress bar while processing.
- SEO-friendly and mobile responsive.
- Styled similar to the Threads app.

## Frontend

The `frontend` directory contains the static website. You can deploy it to any static hosting provider. Update the API endpoint in the frontend code if your FastAPI backend is hosted elsewhere.
