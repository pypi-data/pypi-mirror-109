import numpy as np

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    formula:
    (0°C × 9/5) + 32 = 32°F
    :param celsius:
    :return:
    """
    return (celsius * 9 / 5) + 32

def int_list_between(low:int, high:int)->list:
    return np.arange(low, high, dtype=int)
