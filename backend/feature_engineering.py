# backend/feature_engineering.py
import numpy as np

def get_keystroke_features(keystrokes):
    """Calculates features from the keystrokes array."""
    if len(keystrokes) < 2:
        return 0, 0, 0 # Return 0 for count, avg, and std

    keystroke_count = len(keystrokes)
    timestamps = [k['t'] for k in keystrokes]

    # Calculate flight times (time between key presses)
    flight_times = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]

    avg_flight_time = np.mean(flight_times)
    std_flight_time = np.std(flight_times)

    return keystroke_count, avg_flight_time, std_flight_time

def get_mouse_features(mouse_moves):
    """Calculates features from the mouse_moves array."""
    if len(mouse_moves) < 2:
        return 0, 0 # Return 0 for count and distance

    mouse_move_count = len(mouse_moves)

    # Calculate total distance traveled
    total_distance = 0
    for i in range(1, len(mouse_moves)):
        x1, y1 = mouse_moves[i-1]['x'], mouse_moves[i-1]['y']
        x2, y2 = mouse_moves[i]['x'], mouse_moves[i]['y']
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        total_distance += distance

    return mouse_move_count, total_distance


def engineer_features(data):
    """
    This is the core feature engineering function.
    It turns one raw session document into a flat row of numbers.
    """
    # 1. Keystroke Features
    ks_count, avg_flight_time, std_flight_time = get_keystroke_features(data.get('keystrokes', []))

    # 2. Mouse Features
    mm_count, total_mouse_dist = get_mouse_features(data.get('mouse_moves', []))

    # 3. Click Features
    click_count = len(data.get('clicks', []))

    # 4. Timing Features
    timestamps = data.get('timestamps', {'start': 0, 'end': 0})
    duration = timestamps.get('end', 0) - timestamps.get('start', 0)

    # Create a dictionary of all features
    features = {
        'ks_count': ks_count,
        'avg_flight_time': avg_flight_time,
        'std_flight_time': std_flight_time,
        'mm_count': mm_count,
        'total_mouse_dist': total_mouse_dist,
        'click_count': click_count,
        'session_duration_ms': duration
    }

    return features