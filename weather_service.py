"""
Weather service using Open-Meteo free API (no API key needed).
"""
import requests
from datetime import datetime, timedelta
from config import WEATHER_API, PALGHAR_LOCATIONS


def get_weather(lat: float, lon: float) -> dict | None:
    """Fetch current weather and 7-day forecast from Open-Meteo."""
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,weather_code",
            "timezone": "Asia/Kolkata",
            "forecast_days": 7,
        }
        resp = requests.get(WEATHER_API, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        # Format current weather
        result = {
            "current": {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "precipitation": current.get("precipitation"),
                "wind_speed": current.get("wind_speed_10m"),
                "weather_code": current.get("weather_code"),
                "description": _weather_code_to_text(current.get("weather_code", 0)),
            },
            "forecast": [],
        }
        
        # Format daily forecast
        dates = daily.get("time", [])
        for i, date_str in enumerate(dates):
            result["forecast"].append({
                "date": date_str,
                "temp_max": daily["temperature_2m_max"][i] if "temperature_2m_max" in daily else None,
                "temp_min": daily["temperature_2m_min"][i] if "temperature_2m_min" in daily else None,
                "precipitation": daily["precipitation_sum"][i] if "precipitation_sum" in daily else None,
                "wind_speed": daily["wind_speed_10m_max"][i] if "wind_speed_10m_max" in daily else None,
                "weather_code": daily["weather_code"][i] if "weather_code" in daily else None,
                "description": _weather_code_to_text(daily["weather_code"][i] if "weather_code" in daily else 0),
            })
        
        return result
    except Exception as e:
        return None


def _weather_code_to_text(code: int) -> str:
    """Convert WMO weather code to text description."""
    codes = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤️",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫️",
        48: "Fog with frost 🌫️",
        51: "Light drizzle 🌦️",
        53: "Moderate drizzle 🌦️",
        55: "Dense drizzle 🌧️",
        61: "Slight rain 🌧️",
        63: "Moderate rain 🌧️",
        65: "Heavy rain 🌧️",
        71: "Slight snow ❄️",
        73: "Moderate snow ❄️",
        75: "Heavy snow ❄️",
        80: "Slight showers 🌦️",
        81: "Moderate showers 🌧️",
        82: "Heavy showers ⛈️",
        95: "Thunderstorm ⛈️",
        96: "Thunderstorm with hail ⛈️",
        99: "Thunderstorm with heavy hail ⛈️",
    }
    return codes.get(code, f"Weather code {code}")


def get_weather_emoji(code: int) -> str:
    """Get weather emoji for code."""
    if code == 0:
        return "☀️"
    elif code <= 3:
        return "⛅"
    elif code <= 48:
        return "🌫️"
    elif code <= 55:
        return "🌦️"
    elif code <= 65:
        return "🌧️"
    elif code <= 75:
        return "❄️"
    elif code <= 82:
        return "🌧️"
    else:
        return "⛈️"


def get_farming_advice_from_weather(weather_data: dict, lang: str = "en") -> list[str]:
    """Generate farming advice based on current weather conditions."""
    if not weather_data or "current" not in weather_data:
        return []
    
    current = weather_data["current"]
    temp = current.get("temperature")
    humidity = current.get("humidity")
    precipitation = current.get("precipitation")
    wind = current.get("wind_speed")
    
    # Check upcoming rainfall
    forecast = weather_data.get("forecast", [])
    rain_coming = any(
        (f.get("precipitation") or 0) > 5 for f in forecast[:3]
    )
    
    advice = {
        "en": [],
        "hi": [],
        "mr": [],
    }
    
    # Temperature-based advice
    if temp is not None:
        if temp > 40:
            advice["en"].append("🌡️ Very hot today! Irrigate crops in early morning or evening. Avoid noon spraying.")
            advice["hi"].append("🌡️ आज बहुत गर्मी है! सुबह जल्दी या शाम को सिंचाई करें। दोपहर में छिड़काव से बचें।")
            advice["mr"].append("🌡️ आज खूप उकाडा आहे! सकाळी लवकर किंवा संध्याकाळी पाणी द्या. दुपारी फवारणी टाळा.")
        elif temp > 35:
            advice["en"].append("🌡️ Hot weather - ensure adequate irrigation for your crops. Apply mulch to retain soil moisture.")
            advice["hi"].append("🌡️ गर्म मौसम - फसलों को पर्याप्त पानी दें। मिट्टी की नमी बनाए रखने के लिए मल्च लगाएं।")
            advice["mr"].append("🌡️ उष्ण हवामान - पिकांना पुरेसे पाणी द्या. मातीत ओलावा टिकवण्यासाठी आच्छादन करा.")
        elif temp < 10:
            advice["en"].append("🥶 Cold weather! Protect young seedlings from frost. Cover with plastic sheets if needed.")
            advice["hi"].append("🥶 ठंडा मौसम! छोटे पौधों को पाले से बचाएं। ज़रूरत हो तो प्लास्टिक शीट से ढकें।")
            advice["mr"].append("🥶 थंड हवामान! लहान रोपांना दंवापासून वाचवा. गरज असल्यास प्लॅस्टिक शीटने झाका.")
    
    # Humidity-based advice
    if humidity is not None:
        if humidity > 85:
            advice["en"].append("💧 Very high humidity - watch for fungal diseases. Consider preventive fungicide spray.")
            advice["hi"].append("💧 बहुत अधिक नमी - फफूंद रोगों पर नज़र रखें। निवारक फफूंदनाशक छिड़काव पर विचार करें।")
            advice["mr"].append("💧 खूप जास्त आर्द्रता - बुरशीजन्य रोगांवर लक्ष ठेवा. प्रतिबंधात्मक बुरशीनाशक फवारणीचा विचार करा.")
    
    # Rain-based advice
    if precipitation is not None and precipitation > 0:
        advice["en"].append("🌧️ Rain today - avoid pesticide or fertilizer application. Water will wash it away.")
        advice["hi"].append("🌧️ आज बारिश है - कीटनाशक या खाद का छिड़काव न करें। पानी बहा ले जाएगा।")
        advice["mr"].append("🌧️ आज पाऊस आहे - कीटकनाशक किंवा खताची फवारणी करू नका. पाणी वाहून नेईल.")
    
    if rain_coming:
        advice["en"].append("🌧️ Rain expected in next 3 days. Plan harvesting of ready crops before rain. Ensure drainage channels are clear.")
        advice["hi"].append("🌧️ अगले 3 दिनों में बारिश की संभावना। बारिश से पहले तैयार फसलों की कटाई करें। नालियाँ साफ़ रखें।")
        advice["mr"].append("🌧️ पुढील 3 दिवसांत पावसाची शक्यता. पावसापूर्वी तयार पिकांची काढणी करा. पाण्याचे नाले स्वच्छ ठेवा.")
    
    # Wind-based advice
    if wind is not None and wind > 40:
        advice["en"].append("💨 Strong winds today! Stake tall crops like banana, sugarcane. Avoid spraying chemicals.")
        advice["hi"].append("💨 आज तेज़ हवा! केले, गन्ने जैसी ऊंची फसलों को सहारा दें। रसायनों का छिड़काव न करें।")
        advice["mr"].append("💨 आज जोरदार वारे! केळी, ऊसासारख्या उंच पिकांना आधार द्या. रासायनिक फवारणी टाळा.")
    
    return advice.get(lang, advice["en"])
