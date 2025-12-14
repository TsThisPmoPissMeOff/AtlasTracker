from geoclip_model import predict_locations
from ocr import extract_text
from exif import extract_exif
from sun_analysis import score_candidates_by_sun
from weather import score_candidates_by_weather
from priors import population_prior
from landmarks import detect_landmarks
from language_detection import detect_language

def analyze_image(image_bytes, bbox=None):
    exif = extract_exif(image_bytes)
    text = extract_text(image_bytes)

    candidates = predict_locations(image_bytes)

    sun = score_candidates_by_sun(candidates, exif)
    weather = score_candidates_by_weather(candidates, exif)
    pop = population_prior(candidates)
    landmark_score = detect_landmarks(image_bytes)
    lang = detect_language(text)

    final = []
    for c in candidates:
        lat, lon = c["coords"]["lat"], c["coords"]["lon"]

        score = (
            0.65 * c["score"] +
            0.08 * sun.get((lat, lon), 0) +
            0.07 * weather.get((lat, lon), 0) +
            0.10 * pop.get((lat, lon), 0) +
            0.10 * landmark_score
        )

        final.append({**c, "final_score": score})

    final.sort(key=lambda x: x["final_score"], reverse=True)

    return {
        "candidates": final[:5],
        "explanation": {
            "language": lang,
            "landmark_score": landmark_score,
            "exif": exif,
            "ocr": text
        }
    }
