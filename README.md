
# ⚡ Petrocast Resilience

> **Autonomous Crude Oil Procurement & Maritime Chokepoint Intelligence Platform**

Petrocast Resilience is an enterprise decision intelligence system engineered for energy procurement teams, commodity traders, and refinery operators. It combines live market telemetry, maritime bottleneck threat assessment, statistical price forecasting with quantile bounds, and an autonomous AI  to optimize oil procurement schedules and mitigate physical supply chain risks.

---

## 🌟 Key Features

* **Live Market Telemetry**: Real-time tracking of global energy benchmarks and macroeconomic indicators (Brent Crude, WTI, Gold, VIX Volatility Index, USD/INR).
* **Maritime Chokepoint Risk Index**: Threat scoring (0–10 scale) and delay quantification across critical transit corridors:
  * Bab-el-Mandeb Strait (Red Sea corridor)
  * Strait of Hormuz
  * Suez Canal
  * Strait of Malacca
* **Quantile Price Forecasting**: Multi-horizon ($p10$ floor, $p50$ baseline, $p90$ worst-case price ceiling) probability cones spanning 1-Day, 1-Month, and 3-Month timelines.
* **Dual-Asset Switcher**: Seamless live toggle between **Brent** (global seaborne benchmark) and **WTI** (US sweet light benchmark).
* **Autonomous AI Orchestrator**: ReAct tool-calling agent powered by Google Gemini that runs real-time inventory math, evaluates freight routing penalties, queries vector-indexed maritime news via ChromaDB RAG, and produces concise executive action plans.

---

## 🏛️ System Architecture


```

petrocast-resilience/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # REST endpoints (market, chokepoints, forecast, agent)
│   │   ├── core/               # App configuration, logging, and security settings
│   │   ├── db/                 # Database models, schemas, and session engine
│   │   ├── services/           # ReAct agent tools, RAG pipeline, & forecast calculations
│   │   └── main.py             # FastAPI entrypoint & middleware configuration
│   ├── alembic/                # Database migrations (PostgreSQL / SQLite)
│   └── requirements.txt        # Backend dependencies
└── frontend/
├── src/
│   ├── app/                # Next.js App Router (Landing page & /console)
│   ├── components/         # Forecast chart, telemetry cards, & agent terminal
│   └── lib/                # API client configuration & data types
├── package.json            # Frontend dependencies
└── tailwind.config.ts      # Industrial dark-mode UI theme configuration

```

---

## 🛠️ Tech Stack

* **Frontend**: Next.js 14, React, Tailwind CSS, Recharts, Lucide Icons, Axios
* **Backend**: FastAPI, Pydantic v2, SQLAlchemy, Uvicorn
* **Database & Vector Store**: PostgreSQL / SQLite, ChromaDB (Vector Search & Maritime RAG)
* **AI & Statistics**: Google Gemini API, NumPy/SciPy Statistical Quantile Modeling

---

## 🚀 Quickstart Guide

### Prerequisites
* Python 3.10+
* Node.js 18+ and npm
* Google Gemini API Key

---

### 1. Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend

```

2. **Create and activate a virtual environment:**
```bash
# Windows (CMD):
python -m venv venv
venv\Scripts\activate

# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Set up environment variables:**
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY="your-gemini-api-key-here"
DATABASE_URL="sqlite:///./petrocast.db"

```


5. **Run database migrations:**
```bash
alembic upgrade head

```


6. **Start the FastAPI backend server:**
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

```


* Swagger Documentation: `http://127.0.0.1:8000/docs`



---

### 2. Frontend Setup

1. **Open a new terminal and navigate to the frontend directory:**
```bash
cd frontend

```


2. **Install dependencies:**
```bash
npm install

```


3. **Start the Next.js development server:**
```bash
npm run dev

```


* Application UI: `http://localhost:3000`



---

## 📊 Quantile Forecast Methodology

The forecast engine constructs probability bounds across horizons $T \in \{1\text{ day}, 30\text{ days}, 90\text{ days}\}$ using spot price $S_0$ and annualized volatility $\sigma$ derived from the VIX:

$$\text{Quantile Price} = S_0 \cdot \exp\left( \pm Z_p \cdot \sigma \cdot \sqrt{\frac{T}{365}} \right)$$

* **$p50$ (Median Line)**: Baseline price under normal market conditions.
* **$p90$ (Upper Band)**: 90th percentile worst-case price spike risk (used for budget buffers and hedging).
* **$p10$ (Lower Band)**: 10th percentile floor for strategic dip buying.

---

## 🛡️ License

Distributed under the MIT License.

```

```