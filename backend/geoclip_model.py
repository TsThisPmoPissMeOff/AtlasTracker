import io
from PIL import Image
import torch
from geoclip import GeoCLIP

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = GeoCLIP()
    return _model

def predict_locations(image_bytes, top_k=5):
    """
    Use real GeoCLIP to generate geolocation predictions.
    Returns a list of candidates with 'coords' and 'score'.
    """
    model = _load_model()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    temp_path = "/tmp/temp_image.png"
    image.save(temp_path)

    try:
        top_coords, top_probs = model.predict(temp_path, top_k=top_k)
        results = [
            {"coords": {"lat": float(lat), "lon": float(lon)}, "score": float(prob)}
            for (lat, lon), prob in zip(top_coords, top_probs)
        ]
    except Exception as e:
        results = []
        print("GeoCLIP prediction error:", e)

    return results
