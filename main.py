from fastapi import FastAPI
from pydantic import BaseModel
import json
from kafka import KafkaProducer
from typing import Optional
 
app = FastAPI()

# ─── Models ──────────────────────────────────────────────────────
 
class Login(BaseModel):
    user_id: int
    name: str
    email: str
    phone: int
    city: str
    address: str
    ip_address: str
    device: str
    user_type: str
    login_status: int           
    failed_attempts: int
    session_duration: float     
    login_time: str
    is_new_user: int
    loyalty_score: int
 
class Order(BaseModel):
    user_id: int
    name: str
    email: str
    phone: int
    city: str
    product: str
    quantity: int
    unit_price: int
    discount_pct: int
    final_price: int
    order_time: str
    user_type: str
    loyalty_score: int
 
class Payment(BaseModel):
    user_id: int
    name: str
    email: str
    phone: int
    city: str
    product: str
    quantity: int
    amount: int
    payment_method: str
    status: str
    txn_id: str
    payment_time: str
    user_type: str
    loyalty_score: int

producer = KafkaProducer(
    bootstrap_servers=['100.77.136.82:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


# ─── Endpoints ───────────────────────────────────────────────────
 
@app.post("/login")
def post_login(data: Login):
    payload = data.model_dump()
    producer.send("login",payload)
    return payload


@app.post("/order")
def post_order(data: Order):
    payload = data.model_dump()
    producer.send("order",payload)
    return payload

 
@app.post("/payment")
def post_payment(data: Payment):
    payload = data.model_dump()
    producer.send("payment",payload)
    return payload
 
