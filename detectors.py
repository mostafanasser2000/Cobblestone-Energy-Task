import numpy as np


def calculate_mad(window, scaler=1.4826):
    """
    Algorithm to calculate median absolute deviation
    """
    data = np.array(window)
    # get median of data
    median = np.median(data)
    # calculate deviation for each point point from median
    deviations = np.abs(median - data) * scaler
    # get median of deviations
    mad = np.median(deviations)
    return median, mad


class MADDetector:
    """MAD (Median absolute deviation from median) to detect anomalies"""

    def __init__(self, window_size=10, threshold=3):
        self.widow_size = window_size
        self.threshold = threshold
        self._data_window = []
        self._median = 0
        self._mad = 0

    def add_point(self, point: float):
        """Add new point and check if it's an anomaly"""
        self._data_window.append(point)

        if len(self._data_window) > self.widow_size:
            self._data_window.pop(0)

        if len(self._data_window) >= self.widow_size:
            return self.is_anomaly(point)

        return False

    def is_anomaly(self, point):
        # formula
        self._median, self._mad = calculate_mad(self._data_window)
        modified_z_score = (0.675 * np.abs(point - self._median)) / self._mad
        return modified_z_score > self.threshold
