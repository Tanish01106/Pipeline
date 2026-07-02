import requests
from fake_data_ import login_data, order_data, payment_data
import time
import random
 
BASE_URL = "http://127.0.0.1:8000"
 
print("🚀 Starting data stream...")

sent = 0
while True:
    try:
        
        login = login_data()
        r1 = requests.post(f"{BASE_URL}/login", json=login)
        
        if r1.status_code != 200:
            print(f"Login failed: {r1.status_code}")
            continue
         
        if login["login_status"] == 1:
            order = order_data(login)
            r2 = requests.post(f"{BASE_URL}/order", json=order)
 
            if r2.status_code == 200:
                
                payment = payment_data(order)
                r3 = requests.post(f"{BASE_URL}/payment", json=payment)
        
        sent += 1
        if sent % 100 == 0:
            print(f"✅ {sent} events sent | Last user: {login['user_id']} ({login['user_type']})")
 

        if login["user_type"] == "bot":
            time.sleep(0.001)
        else:
            time.sleep(random.uniform(0.05, 0.3))   
 
    except KeyboardInterrupt:
        print(f"\n⛔ Stopped. Total events sent: {sent}")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
