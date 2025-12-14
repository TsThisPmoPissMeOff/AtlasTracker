import random

BBOX = None  # optional bounding box

def predict_locations(image_bytes, top_k=5):
    """
    Dummy GeoCLIP stub.
    Replace with actual model if desired.
    Returns list of candidates with fake coordinates and scores.
    """
    candidates = []
    for i in range(top_k):
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        if BBOX:
            lat_min, lon_min, lat_max, lon_max = BBOX
            lat = random.uniform(lat_min, lat_max)
            lon = random.uniform(lon_min, lon_max)
        score = random.uniform(0.5, 1.0)
        candidates.append({'coords': {'lat': lat, 'lon': lon}, 'score': score})
    return candidates
