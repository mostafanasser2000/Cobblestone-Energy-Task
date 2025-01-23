import json
import numpy as np
from typing import Dict
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError
from settings import BOOTSTRAP_SERVERS, KAFKA_TOPIC
import time

class JsonDataProducer:
    def __init__(self, props):
        self.producer = KafkaProducer(**props)

    def publish_data(self, topic: str) -> None:
        for i in range(1000):
            seasonal_variation = 0.5 * np.sin(i * 0.01)
            value = np.sin(i * 0.1) + seasonal_variation

            # Introduce random spike as an anomaly with 1% probability
            if np.random.rand() < 0.01:
                value += np.random.rand() * 5

            data: Dict = {"value": float(value)}

            try:
                record = self.producer.send(
                    topic=topic,
                    key=str(i).encode(),
                    value=json.dumps(data).encode(),
                )

            except KafkaTimeoutError as e:
                print(e)
            
            time.sleep(0.1)
        self.producer.flush()
        self.producer.close()


if __name__ == "__main__":
    configs = {
        "bootstrap_servers": BOOTSTRAP_SERVERS,
    }
    producer = JsonDataProducer(props=configs)
    producer.publish_data(topic=KAFKA_TOPIC)
