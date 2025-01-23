from typing import List
from json import loads
from kafka import KafkaConsumer
from settings import BOOTSTRAP_SERVERS, KAFKA_TOPIC
from detectors import MADDetector
from visualizer import DataStreamVisualizer


class JsonDataConsumer:
    def __init__(self, props) -> None:
        self.consumer = KafkaConsumer(**props)
        self.visualizer = DataStreamVisualizer()

    def consume_from_kafka(self, topics: List[str], batch_size: int = 5) -> None:
        detector = MADDetector()
        self.consumer.subscribe(topics)
        batch = []

        while True:
            try:
                records = self.consumer.poll(timeout_ms=1000)
                if not records:
                    continue

                for topic_partition, messages in records.items():
                    for message in messages:
                        decoded_data = message.value
                        batch.append(decoded_data["value"])

                        if len(batch) >= batch_size:
                            self.process_batch(batch, detector)
                            batch = []

                if batch:  # Process remaining batch
                    self.process_batch(batch, detector)
                    batch = []

            except KeyboardInterrupt:
                break

        self.consumer.close()

    def process_batch(self, batch: List[float], detector: MADDetector) -> None:
        for point in batch:
            is_anomaly = detector.add_point(point)
            self.visualizer.update(point, is_anomaly)


if __name__ == "__main__":
    config = {
        "bootstrap_servers": BOOTSTRAP_SERVERS,
        "auto_offset_reset": "earliest",
        "enable_auto_commit": True,
        "key_deserializer": lambda key: int(key.decode()),
        "value_deserializer": lambda x: loads(x.decode()),
        "group_id": "consumer.group.id.stream_data.1",
    }

    json_consumer = JsonDataConsumer(props=config)
    json_consumer.consume_from_kafka(topics=[KAFKA_TOPIC])
