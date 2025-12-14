from geopy.geocoders import Nominatim

def population_prior(candidates):
    """
    Assign prior probability based on city/population density.
    Uses Nominatim to approximate populated areas.
    """
    geolocator = Nominatim(user_agent="atlasfinder")
    results = {}
    try:
        for c in candidates:
            lat = c['coords']['lat']
            lon = c['coords']['lon']
            location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
            if location and 'city' in location.raw['address']:
                results[(lat, lon)] = 1.0  # highly populated area
            else:
                results[(lat, lon)] = 0.5  # rural or unknown
    except Exception as e:
        print("Population prior error:", e)
    return results
