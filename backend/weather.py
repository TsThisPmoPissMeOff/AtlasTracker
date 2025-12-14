from meteostat import Point, Daily
from datetime import datetime

def match_weather(image_bytes, exif_data):
    """
    Match image weather (snow, clouds) with historical weather.
    Returns a dict mapping candidate coordinates to weather match score.
    """
    results = {}
    try:
        # Extract timestamp from EXIF
        timestamp_str = exif_data.get("EXIF DateTimeOriginal")
        if not timestamp_str:
            return results
        dt = datetime.strptime(timestamp_str, "%Y:%m:%d %H:%M:%S")

        # Placeholder: score candidates by simple historical weather probability
        # Real implementation can parse clouds, snow from image using CV
        for lat in range(-90, 91, 5):
            for lon in range(-180, 181, 10):
                point = Point(lat, lon)
                data = Daily(point, dt, dt).fetch()
                if data.empty:
                    score = 0
                else:
                    # simple scoring: less precipitation = higher score
                    prcp = data['prcp'].iloc[0]
                    score = 1.0 if prcp == 0 else 0.5
                results[(lat, lon)] = score
    except Exception as e:
        print("Weather matching error:", e)
    return results
