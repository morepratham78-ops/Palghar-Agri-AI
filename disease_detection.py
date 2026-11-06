"""
Crop disease detection service using real fine-tuned ResNet model trained on PlantVillage dataset.
Provides real image-based disease detection, confidence scores, symptoms, treatments, and prevention.
"""
import os
import io
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
from config import BASE_DIR, DISEASE_INFO, GENERIC_DISEASE_ADVICE

LOCAL_MODEL_DIR = os.path.join(BASE_DIR, "models", "plantvillage-resnet18")

_model = None
_processor = None
_model_loaded = False
_model_error = None


def is_model_available() -> bool:
    """Check if model files exist locally."""
    return os.path.exists(LOCAL_MODEL_DIR) and os.path.exists(
        os.path.join(LOCAL_MODEL_DIR, "model.safetensors")
    )


def load_model():
    """Load the locally saved fine-tuned PlantVillage ResNet model."""
    global _model, _processor, _model_loaded, _model_error
    if _model_loaded and _model is not None:
        return True
    
    try:
        if not os.path.exists(LOCAL_MODEL_DIR):
            _model_error = f"Model directory not found at {LOCAL_MODEL_DIR}"
            return False
            
        _processor = AutoImageProcessor.from_pretrained(LOCAL_MODEL_DIR)
        _model = AutoModelForImageClassification.from_pretrained(LOCAL_MODEL_DIR)
        _model.eval()
        _model_loaded = True
        _model_error = None
        return True
    except Exception as e:
        _model_error = str(e)
        _model_loaded = False
        return False


def predict_disease(image_bytes: bytes) -> dict:
    """
    Predict crop disease from image bytes using genuine trained model.
    Returns:
        dict with success status, predicted_class, crop name, disease name,
        confidence, reliability flag, top-3 candidates, and human-friendly labels.
    """
    global _model, _processor
    if not _model_loaded:
        if not load_model():
            return {
                "success": False,
                "error": _model_error or "Unable to load vision model",
                "reliable": False
            }
            
    try:
        # Load image safely
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Preprocess using official processor
        inputs = _processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = _model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            
            # Top-3 predictions
            top3_probs, top3_indices = torch.topk(probabilities, 3, dim=1)
            
            top3 = []
            for i in range(3):
                class_idx = top3_indices[0][i].item()
                class_label = _model.config.id2label[class_idx]
                top3.append({
                    "class": class_label,
                    "confidence": float(top3_probs[0][i].item())
                })
        
        best_prediction = top3[0]
        predicted_class = best_prediction["class"]
        confidence_val = best_prediction["confidence"]
        
        # Parse crop and disease names
        parts = predicted_class.split("___")
        crop_name = parts[0].replace("_", " ").replace("(", " (") if len(parts) > 0 else "Unknown"
        disease_raw = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
        is_healthy = "healthy" in disease_raw.lower()
        
        # Real reliability evaluation
        reliable = confidence_val >= 0.55
        
        return {
            "success": True,
            "predicted_class": predicted_class,
            "crop": crop_name,
            "disease_raw": disease_raw,
            "is_healthy": is_healthy,
            "confidence": confidence_val,
            "reliable": reliable,
            "top3": top3,
            "is_pretrained_only": False,  # Truly fine-tuned on PlantVillage!
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "reliable": False
        }


def get_disease_info(predicted_class: str, lang: str = "en") -> dict:
    """Get structured symptoms, treatment, and prevention for the predicted disease."""
    if predicted_class in DISEASE_INFO:
        info = DISEASE_INFO[predicted_class]
        if lang in info:
            return info[lang]
        return info.get("en", {})
        
    # Check if any key is a substring or match
    for k, v in DISEASE_INFO.items():
        if k.lower() == predicted_class.lower():
            if lang in v:
                return v[lang]
            return v.get("en", {})
            
    # Generic agricultural fallback advice with formatted name
    parts = predicted_class.split("___")
    crop_display = parts[0].replace("_", " ") if len(parts) > 0 else "Crop"
    disease_display = parts[1].replace("_", " ") if len(parts) > 1 else "Infection"
    
    localized_fallback = GENERIC_DISEASE_ADVICE.get(lang, GENERIC_DISEASE_ADVICE["en"])
    return {
        "name": f"{crop_display} - {disease_display}",
        "symptoms": localized_fallback.get("symptoms", ""),
        "treatment": localized_fallback.get("treatment", ""),
        "prevention": localized_fallback.get("prevention", ""),
    }
