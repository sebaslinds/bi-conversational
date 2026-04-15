from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sales.csv"

load_dotenv(BASE_DIR / ".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_summary():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    total_revenue = df["revenue"].sum()
    total_orders = df["orders"].sum()
    avg_basket = round(total_revenue / total_orders, 2)
    by_month = df.groupby(df["date"].dt.strftime("%Y-%m"))["revenue"].sum()
    by_month = {k: int(v) for k, v in by_month.items()}
    by_category = df.groupby("category")["revenue"].sum()
    by_category = {k: int(v) for k, v in by_category.items()}

    by_region = df.groupby("region")["revenue"].sum()
    by_region = {k: int(v) for k, v in by_region.items()}
    return {
        "total_revenue": int(total_revenue),
        "total_orders": int(total_orders),
        "avg_basket": float(avg_basket),
        "revenue_by_month": by_month,
        "revenue_by_category": by_category,
        "revenue_by_region": by_region,
    }


@app.get("/data")
def get_data():
    return load_summary()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)
    summary = load_summary()
    system_prompt = f"""
Tu es un analyste BI expert.

Réponds en français, de façon concise.

Données :
- Revenu total : {summary['total_revenue']}
- Commandes : {summary['total_orders']}
- Panier moyen : {summary['avg_basket']}
- Par mois : {summary['revenue_by_month']}
- Par catégorie : {summary['revenue_by_category']}
- Par région : {summary['revenue_by_region']}

Ta réponse doit TOUJOURS contenir :
1. 📊 1 insight clé
2. 📈 1 tendance
3. 💡 1 recommandation business concrète
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message},
        ],
        max_output_tokens=1000,
    )
    return {"response": response.output_text}
