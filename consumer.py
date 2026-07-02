from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'login',
    'order',
    bootstrap_servers='100.77.136.82:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    print(f"Topic: {message.topic} | Offset: {message.offset} | Data: {message.value}")
    print(type(message.value))
 