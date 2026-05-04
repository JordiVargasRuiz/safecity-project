from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SafeCity Alerts - Producción CUCEI", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": "postgres-service",
    "database": "safecity_alerts",
    "user": "postgres",
    "password": "safepass123",
    "connect_timeout": 5
}

# --- RUTA POST ---
@app.post("/alerts")
async def create_alert(incident: dict, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO alerts (tipo, ubicacion, lat, lon) VALUES (%s, %s, %s, %s)", 
            (incident.get('tipo'), incident.get('ubicacion'), incident.get('lat'), incident.get('lon'))
        )
        conn.commit()
        cur.close()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error POST: {e}")
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

@app.get("/alerts")
async def get_alerts():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT tipo, ubicacion, 
            fecha AT TIME ZONE 'UTC' AT TIME ZONE 'America/Mexico_City', 
            lat, lon 
            FROM alerts 
            ORDER BY fecha DESC 
            LIMIT 15
        """)
        
        rows = cur.fetchall()
        
        alerts = []
        for r in rows:
            alerts.append({
                "tipo": r[0],
                "ubicacion": r[1],
                "fecha": r[2].strftime("%I:%M %p") if r[2] else "--:--",
                "lat": r[3],
                "lon": r[4]
            })
        return alerts
    except Exception as e:
        logger.error(f"Error en GET: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()