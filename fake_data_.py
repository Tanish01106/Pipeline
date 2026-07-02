from faker import Faker
import random
import time
from datetime import datetime, timedelta
 
fake = Faker("en_IN")
 
# ─── User Archetypes ─────────────────────────────────────────────
 
USER_TYPES = {
    "loyal":        0.25,   
    "casual":       0.35,   
    "bot":          0.08,   
    "fraudster":    0.07,   
    "one_time":     0.15,   
    "night_owl":    0.10,   
}

PRODUCTS = {
    "Phone":        25000,
    "MacBook":      120000,
    "Laptop":       75000,
    "SSD":          8000,
    "iPad":         60000,
    "Earbuds":      3000,
    "Smartwatch":   15000,
    "Keyboard":     2500,
    "Monitor":      22000,
    "Charger":      1200,
}
 
DEVICES = ["Windows_11", "MacOS", "Windows_10", "Linux", "iOS", "Android"]
 
PAYMENT_METHODS = ["UPI", "Credit_Card", "Debit_Card", "NetBanking", "COD", "Wallet"]
 
# Cities with weights (metro cities more likely)
CITIES = {
    "Mumbai": 0.18, "Delhi": 0.16, "Bangalore": 0.14,
    "Hyderabad": 0.10, "Chennai": 0.09, "Pune": 0.08,
    "Kolkata": 0.07, "Ahmedabad": 0.06, "Jaipur": 0.05,
    "Chandigarh": 0.04, "Others": 0.03
}
 
# Persistent user pool — 
USER_POOL = {}
user_id_counter = 1001
 
# ─── User Pool ───────────────────────────────────────────────────
 
def get_or_create_user():
    """User pool se user lo ya naya banao"""
    global user_id_counter
 
    
    if USER_POOL and random.random() < 0.60:
        uid = random.choice(list(USER_POOL.keys()))
        return USER_POOL[uid], False  # (user_data, is_new)

    user_type = random.choices(  
        list(USER_TYPES.keys()), 
        weights=list(USER_TYPES.values()) 
    )[0]  

    city = random.choices(list(CITIES.keys()), weights=list(CITIES.values()))[0]
 
    user = {
        "user_id": user_id_counter,
        "name": fake.name(),
        "email": fake.email(),
        "phone": int(fake.numerify("9#########")),
        "city": city,
        "user_type": user_type,
        "home_ip": fake.ipv4(),
        "device": random.choice(DEVICES),
        "registered_at": fake.date_time_between(start_date="-2y", end_date="-1d").isoformat(),
        "loyalty_score": _loyalty_score(user_type),
    }
 
    USER_POOL[user_id_counter] = user
    user_id_counter += 1
    return user, True
 
 
def _loyalty_score(user_type):
    if user_type == "loyal":       return random.randint(75, 100)
    if user_type == "casual":      return random.randint(30, 74)
    if user_type == "one_time":    return random.randint(1, 15)
    if user_type == "bot":         return random.randint(0, 5)
    if user_type == "fraudster":   return random.randint(5, 20)
    if user_type == "night_owl":   return random.randint(20, 60)
    return 0
 
 
# ─── Time Helpers ────────────────────────────────────────────────
 
def realistic_time(user_type):
    """User type ke hisaab se login time"""
    now = datetime.now()
    hour = now.hour
 
    if user_type == "night_owl":
        
        hour = random.choice([23, 0, 1, 2, 3, 4])
    elif user_type == "bot":
        
        hour = random.randint(0, 23)
    elif user_type == "fraudster":
        
        hour = random.choice([1, 2, 3, 4, 5, 22, 23, 0])
    else:
        
        hour = random.choice([8, 9, 10, 11, 18, 19, 20, 21] * 3 + list(range(0, 24)))
 
    t = now.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))
    return t.strftime("%Y-%m-%d %H:%M:%S")
 
 
# ─── Login Data ──────────────────────────────────────────────────
 
def login_data():
    user, is_new = get_or_create_user()
    user_type = user["user_type"]
 
    
    if user_type == "fraudster":
        ip = fake.ipv4()  
    elif user_type == "bot":
        ip = user["home_ip"]  
    else:
        ip = user["home_ip"] if random.random() < 0.85 else fake.ipv4()
 
    if user_type in ["fraudster", "bot"]:
        login_status = random.choices([1, 0], weights=[0.4, 0.6])[0]
    else:
        login_status = random.choices([1, 0], weights=[0.92, 0.08])[0]
 
    failed_attempts = 0
    if login_status == 0:
        failed_attempts = random.randint(1, 5) if user_type == "fraudster" else 1
 
    if user_type == "bot":
        session_duration = round(random.uniform(0.1, 2.0), 2)
    elif user_type == "loyal":
        session_duration = round(random.uniform(15.0, 90.0), 2)
    elif user_type == "one_time":
        session_duration = round(random.uniform(2.0, 10.0), 2)
    else:
        session_duration = round(random.uniform(5.0, 45.0), 2)
 
    return {
        "user_id":          user["user_id"],
        "name":             user["name"],
        "email":            user["email"],
        "phone":            user["phone"],
        "city":             user["city"],
        "address":          fake.address().replace("\n", ", "),
        "ip_address":       ip,
        "device":           user["device"],
        "user_type":        user_type,         
        "login_status":     login_status,      
        "failed_attempts":  failed_attempts,
        "session_duration": session_duration,  
        "login_time":       realistic_time(user_type),
        "is_new_user":      int(is_new),
        "loyalty_score":    user["loyalty_score"],
    }
 
 
# ─── Order Data ──────────────────────────────────────────────────
 
def order_data(login):
    user_type = login["user_type"]
 
    if user_type == "loyal":
        product = random.choices(
            list(PRODUCTS.keys()),
            weights=[3, 5, 4, 1, 4, 2, 3, 1, 2, 1]  
        )[0]
        quantity = random.choices([1, 2, 3], weights=[0.5, 0.35, 0.15])[0]
    elif user_type == "bot":
        
        product = random.choice(["Phone", "MacBook", "iPad"])
        quantity = random.randint(5, 20)  
    elif user_type == "fraudster":
        
        product = random.choice(["MacBook", "Phone", "iPad"])
        quantity = random.randint(1, 3)
    else:
        product = random.choice(list(PRODUCTS.keys()))
        quantity = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
 
    base_price = PRODUCTS[product]
 
    # Discount logic
    if user_type == "loyal":
        discount_pct = random.choice([5, 10, 15, 20])  # Loyalty discount
    elif login["login_status"] == 0:
        discount_pct = 0  # Failed login
    else:
        discount_pct = random.choices([0, 5, 10], weights=[0.6, 0.3, 0.1])[0]
 
    final_price = int(base_price * quantity * (1 - discount_pct / 100))
 
    
    login_dt = datetime.strptime(login["login_time"], "%Y-%m-%d %H:%M:%S")
    order_delay = timedelta(minutes=random.uniform(1, login["session_duration"]))
    order_time = (login_dt + order_delay).strftime("%Y-%m-%d %H:%M:%S")
 
    return {
        "user_id":       login["user_id"],
        "name":          login["name"],
        "email":         login["email"],
        "phone":         login["phone"],
        "city":          login["city"],
        "product":       product,
        "quantity":      quantity,
        "unit_price":    base_price,
        "discount_pct":  discount_pct,
        "final_price":   final_price,
        "order_time":    order_time,
        "user_type":     user_type,         
        "loyalty_score": login["loyalty_score"],
    }
 
 
# ─── Payment Data ────────────────────────────────────────────────
 
def payment_data(order):
    user_type = order["user_type"]
 
    if user_type == "loyal":
        method = random.choices(PAYMENT_METHODS, weights=[4, 3, 2, 2, 0, 1])[0]
    elif user_type == "fraudster":
        method = random.choices(PAYMENT_METHODS, weights=[1, 4, 3, 1, 0, 1])[0]  # Cards prefer
    elif user_type == "bot":
        method = "Credit_Card"  
    else:
        method = random.choices(PAYMENT_METHODS, weights=[3, 2, 2, 1, 1, 1])[0]

    # Payment status
    if user_type == "fraudster":
        status = random.choices(
            ["success", "failed", "declined", "flagged"],
            weights=[0.3, 0.3, 0.25, 0.15]
        )[0]
    elif user_type == "bot":
        status = random.choices(
            ["success", "failed", "declined"],
            weights=[0.2, 0.4, 0.4]
        )[0]
    else:
        status = random.choices(
            ["success", "failed", "pending"],
            weights=[0.88, 0.08, 0.04]
        )[0]
 
    order_dt = datetime.strptime(order["order_time"], "%Y-%m-%d %H:%M:%S")
    pay_delay = timedelta(minutes=random.uniform(0.5, 5))
    payment_time = (order_dt + pay_delay).strftime("%Y-%m-%d %H:%M:%S")
 
    if user_type == "fraudster" and random.random() < 0.2:
        txn_id = f"TXN-DUPE-{random.randint(10000, 99999)}"  
    else:
        txn_id = f"TXN-{fake.unique.random_int(min=100000, max=9999999)}"
 
    return {
        "user_id":        order["user_id"],
        "name":           order["name"],
        "email":          order["email"],
        "phone":          order["phone"],
        "city":           order["city"],
        "product":        order["product"],
        "quantity":       order["quantity"],
        "amount":         order["final_price"],
        "payment_method": method,
        "status":         status,
        "txn_id":         txn_id,
        "payment_time":   payment_time,
        "user_type":      user_type,          
        "loyalty_score":  order["loyalty_score"],
    }


