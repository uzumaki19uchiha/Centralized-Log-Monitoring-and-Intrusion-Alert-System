from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# In-memory counters
ip_request_count = {}
ip_failed_count = {}
ip_ports = {}

class LogInput(BaseModel):
    source_ip: str
    destination_port: int
    status: str
    timestamp: str

@app.post("/log")
def receive_log(log: LogInput):

    ip = log.source_ip

    # Update request count
    ip_request_count[ip] = ip_request_count.get(ip, 0) + 1

    # Update failed login count
    if log.status == "failed_login":
        ip_failed_count[ip] = ip_failed_count.get(ip, 0) + 1
    else:
        ip_failed_count[ip] = ip_failed_count.get(ip, 0)

    # Track unique ports
    if ip not in ip_ports:
        ip_ports[ip] = set()

    ip_ports[ip].add(log.destination_port)

    request_count = ip_request_count[ip]
    failed_count = ip_failed_count[ip]
    unique_ports = len(ip_ports[ip])

    # Feature calculation
    error_ratio = failed_count / request_count

    features = [
        request_count,
        failed_count,
        unique_ports,
        error_ratio
    ]

    print("Features:", features)

    # -------------------------
    # Send features to ML model
    # -------------------------
    try:
        response = requests.post(
            "http://ml-model:6000/predict",
            json={"features": features},
            timeout=2
        )
        ml_result = response.json()
    except Exception as e:
        print("ML connection error:", e)
        ml_result = {"anomaly": False}

    # Return both features and ML result
    return {
        "features": features,
        "ml_result": ml_result
    }