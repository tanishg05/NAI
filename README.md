# Nutrition AI Assistant

A complete, demo-ready full-stack AI nutrition assistant utilizing large language models (LLMs) to generate personalized, macro-balanced diet plans and provide real-time recommendations, swaps, and alerts.

## Project Structure
This repository contains two main services:
- **Backend:** FastAPI (Python 3.11+) with PostgreSQL and Redis, integrated with the Groq API.
- **Frontend:** React 18, Vite, and TailwindCSS.

## Implemented in this Repo (Phase 1)
- **Diet Planner Agent:** Generates detailed day-by-day plans tailored to user profiles, health goals, and dietary preferences.
- **Recommendation Agent:** Suggests healthy swaps and real-time adjustments based on plan adherence and logged activities.
- **Orchestrator:** A lightweight router managing these agents.

## Full Architecture (Target)
The full architecture will eventually scale to 6 agents:
1. Profile & Health
2. Food Vision
3. Nutrition Analysis
4. Diet Planning (Implemented)
5. Recommendation (Implemented)
6. Progress & Feedback

*(See `docs/architecture.md` for more details on where the unimplemented agents plug in).*

## Quickstart

### 1. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- A free Groq API key from [console.groq.com](https://console.groq.com)

### 2. Configuration
Create `.env` files from their respective examples:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
Open `backend/.env` and insert your `GROQ_API_KEY`.

### 3. Run with Docker Compose
From the root of the project:
```bash
docker-compose up --build
```
- Backend is available at `http://localhost:8000` (Swagger UI at `/docs`)
- Frontend is available at `http://localhost:5173`

## License
MIT
