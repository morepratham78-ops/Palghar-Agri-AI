"""
Market prices service for agricultural commodities in Maharashtra.
Features:
1. Live Mandi price query from Agmarknet / data.gov.in.
2. Official Government of India Minimum Support Prices (MSP 2024-25) benchmark data.
3. Transparent error handling - never fabricates live price figures.
"""
import requests

# Official Minimum Support Prices (MSP) declared by Govt of India (Cabinet Committee on Economic Affairs)
# for Kharif & Rabi Crops (2024-2025 season) - Rates in Rs. per Quintal
OFFICIAL_MSP_2024_25 = [
    {"commodity": "Paddy (Common) / भात (साधारण)", "msp": 2300, "category": "Cereals / धान्य"},
    {"commodity": "Paddy (Grade A) / भात (ग्रेड ए)", "msp": 2320, "category": "Cereals / धान्य"},
    {"commodity": "Jowar (Hybrid) / ज्वारी (हायब्रिड)", "msp": 3371, "category": "Cereals / धान्य"},
    {"commodity": "Jowar (Maldandi) / ज्वारी (मालदांडी)", "msp": 3421, "category": "Cereals / धान्य"},
    {"commodity": "Bajra / बाजरी", "msp": 2625, "category": "Millets / भरडधान्य"},
    {"commodity": "Ragi (Nagli) / नाचणी / रागी", "msp": 4290, "category": "Millets / भरडधान्य"},
    {"commodity": "Maize / मका", "msp": 2225, "category": "Cereals / धान्य"},
    {"commodity": "Tur (Arhar) / तूर", "msp": 7550, "category": "Pulses / कडधान्ये"},
    {"commodity": "Moong / मूग", "msp": 8682, "category": "Pulses / कडधान्ये"},
    {"commodity": "Urad / उडीद", "msp": 7400, "category": "Pulses / कडधान्ये"},
    {"commodity": "Groundnut / भुईमूग", "msp": 6783, "category": "Oilseeds / गळीत धान्य"},
    {"commodity": "Soybean (Yellow) / सोयाबीन", "msp": 4892, "category": "Oilseeds / गळीत धान्य"},
    {"commodity": "Sunflower Seed / सूर्यफूल", "msp": 7280, "category": "Oilseeds / गळीत धान्य"},
    {"commodity": "Sesamum (Til) / तीळ", "msp": 9267, "category": "Oilseeds / गळीत धान्य"},
    {"commodity": "Nigerseed (Karale) / कारळे", "msp": 8717, "category": "Oilseeds / गळीत धान्य"},
    {"commodity": "Cotton (Medium Staple) / कापूस (मध्यम धागा)", "msp": 7121, "category": "Commercial / नगदी"},
    {"commodity": "Cotton (Long Staple) / कापूस (लांब धागा)", "msp": 7521, "category": "Commercial / नगदी"},
    {"commodity": "Wheat / गहू", "msp": 2275, "category": "Rabi / रब्बी"},
    {"commodity": "Gram (Chana) / हरभरा", "msp": 5440, "category": "Rabi / रब्बी"},
    {"commodity": "Mustard / मोहरी", "msp": 5650, "category": "Rabi / रब्बी"},
    {"commodity": "Safflower (Kardi) / करडई", "msp": 5800, "category": "Rabi / रब्बी"},
]

COMMON_COMMODITIES = [
    "Paddy(Dhan)(Common)", "Rice", "Wheat", "Jowar(Sorghum)", "Bajra(Pearl Millet)", 
    "Maize", "Ragi (Finger Millet)", "Onion", "Tomato", "Potato", "Brinjal", 
    "Chilli Red", "Cotton", "Soyabean", "Groundnut", "Tur (Arhar)", "Moong(Green Gram)",
    "Urad(Black Gram)", "Sugarcane", "Banana", "Grapes", "Mango", "Chickoo",
    "Coconut", "Garlic", "Ginger", "Turmeric", "Cauliflower", "Cabbage", "Capsicum"
]

MAHARASHTRA_MARKETS = [
    "Palghar", "Dahanu", "Vasai", "Mumbai", "Kalyan", "Vashi (Navi Mumbai)",
    "Pune", "Nashik", "Lasalgaon", "Nagpur", "Kolhapur", "Solapur", "Ahmednagar",
    "Sangli", "Satara", "Jalgaon", "Dhule", "Amravati", "Latur", "Nanded"
]


def get_market_prices(commodity: str = "", state: str = "Maharashtra", market: str = "") -> dict:
    """
    Fetch actual market prices from the open government data portal (Agmarknet).
    Never fabricates prices.
    """
    api_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
        "format": "json",
        "limit": 30,
        "filters[state.keyword]": state,
    }
    
    if commodity:
        params["filters[commodity]"] = commodity
    if market:
        params["filters[market]"] = market
        
    try:
        resp = requests.get(api_url, params=params, timeout=7)
        if resp.status_code == 200:
            data = resp.json()
            records = data.get("records", [])
            return {
                "success": True,
                "records": records,
                "total": data.get("total", len(records)),
                "source": "Agmarknet (data.gov.in)",
                "updated": data.get("updated_date", ""),
            }
        else:
            return {
                "success": False,
                "error": f"Mandi API server response code {resp.status_code}",
                "records": []
            }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Mandi server timed out. The national Agmarknet server is temporarily busy.",
            "records": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "records": []
        }


def get_msp_data(search_query: str = "") -> list:
    """Return verified official Government Minimum Support Prices (MSP)."""
    if not search_query or not search_query.strip():
        return OFFICIAL_MSP_2024_25
        
    q = search_query.lower().strip()
    return [
        item for item in OFFICIAL_MSP_2024_25
        if q in item["commodity"].lower() or q in item["category"].lower()
    ]
