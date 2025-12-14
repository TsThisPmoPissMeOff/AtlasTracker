from geoclip_model import predict_locations
from ocr import extract_text
from exif import extract_exif
from sun_analysis import estimate_latitude
from weather import match_weather
from priors import population_prior
from refine import BBOX, apply_bounding_box

def analyze_image(image_bytes, bbox=None):
    if bbox:
        apply_bounding_box(bbox)

    exif_data = extract_exif(image_bytes)
    text_data = extract_text(image_bytes)

    visual_candidates = predict_locations(image_bytes)

    sun_scores = estimate_latitude(image_bytes, exif_data)
    weather_scores = match_weather(image_bytes, exif_data)
    prior_scores = population_prior(visual_candidates)

    final_candidates = []
    for c in visual_candidates:
        lat, lon = c['coords']['lat'], c['coords']['lon']
        score = (
            0.5 * c['score'] +
            0.2 * sun_scores.get(round(lat), 0) +
            0.2 * weather_scores.get((round(lat), round(lon)), 0) +
            0.1 * prior_scores.get((lat, lon), 0)
        )
        final_candidates.append({**c, 'final_score': score})

    final_candidates.sort(key=lambda x: x['final_score'], reverse=True)

    explanation = {
        'EXIF': exif_data,
        'OCR': text_data,
        'Visual': [c['score'] for c in visual_candidates],
        'Sun/Shadow': sun_scores,
        'Weather': weather_scores,
        'Population': prior_scores
    }

    return {
        'candidates': final_candidates[:5],
        'explanation': explanation
    }
