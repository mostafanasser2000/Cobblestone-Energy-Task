import matplotlib.pyplot as plt
from typing import List, Optional


class DataStreamVisualizer:
    def __init__(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.points: List[float] = []
        self.anomalies: List[Optional[float]] = []

    def update(self, new_point: float, is_anomaly: bool) -> None:
        self.points.append(new_point)
        self.anomalies.append(new_point if is_anomaly else None)

        self.ax.clear()
        self.ax.plot(self.points, label="Data Stream")

        # Plot only anomaly points (non-None values)
        anomaly_indices = [i for i, v in enumerate(self.anomalies) if v is not None]
        anomaly_values = [v for v in self.anomalies if v is not None]

        if anomaly_values:
            self.ax.scatter(
                anomaly_indices,
                anomaly_values,
                color="red",
                label="Anomaly Points",
            )

        self.ax.legend()
        plt.pause(0.1)
