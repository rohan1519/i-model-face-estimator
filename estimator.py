import cv2
import numpy as np
import base64
import os
import logging
# deepface will be lazy-loaded to optimize server startup speed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MediaPipe Face Mesh safely
try:
    import mediapipe as mp
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    )
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    HAS_MEDIAPIPE = True
    logger.info("MediaPipe Face Mesh initialized successfully.")
except Exception as e:
    HAS_MEDIAPIPE = False
    logger.error(f"Failed to initialize MediaPipe Face Mesh: {e}. Falling back to OpenCV detection.")

# Fallback OpenCV Haar Cascade for Face Detection
local_cascade = 'haarcascade_frontalface_default.xml'
if os.path.exists(local_cascade):
    CASCADE_PATH = local_cascade
else:
    CASCADE_PATH = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def decode_image(image_bytes: bytes) -> np.ndarray:
    """Decodes image bytes to an OpenCV BGR image."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def encode_image_to_base64(img: np.ndarray) -> str:
    """Encodes an OpenCV image to a base64 JPEG string."""
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"

def calculate_patch_metrics(patch: np.ndarray) -> tuple:
    """
    Calculates brightness, smoothness, and uniformity for a skin patch.
    Returns (brightness_score, smoothness_score, uniformity_score)
    """
    if patch is None or patch.size == 0:
        return 50, 50, 50

    # 1. Brightness Score
    # Convert to YCrCb and extract the Y channel (Luminance)
    ycrcb = cv2.cvtColor(patch, cv2.COLOR_BGR2YCrCb)
    y_channel = ycrcb[:, :, 0]
    mean_y = np.mean(y_channel)
    # Normalize brightness to 0-100 (assuming typical skin Y values range from 50 to 220)
    brightness_score = np.clip((mean_y - 50) / 1.7, 0, 100)

    # 2. Smoothness Score
    # Convert to grayscale
    gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
    # Calculate Laplacian variance (high variance = sharp/rough/noisy skin, low = smooth)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_var = np.var(laplacian)
    # Map variance to smoothness (typical range: 10 is very smooth, 300 is rough/textured)
    # Let's use a non-linear mapping (log scale or clipping)
    smoothness_score = 100.0 - np.clip(laplacian_var * 0.5, 0, 100)

    # 3. Uniformity Score
    # Skin uniformity: standard deviation of channels (low deviation = even color/fewer spots)
    std_bgr = np.std(patch, axis=(0, 1))
    mean_std = np.mean(std_bgr)
    # Standard deviation of 0-5 is very uniform, 30+ is patchy/spotted
    uniformity_score = 100.0 - np.clip(mean_std * 3.0, 0, 100)

    return float(brightness_score), float(smoothness_score), float(uniformity_score)

def get_face_metrics_mediapipe(img: np.ndarray):
    """
    Detects face landmarks using MediaPipe and extracts cheek and forehead patches.
    Draws the mesh and patches, and computes metrics.
    """
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)
    
    if not results.multi_face_landmarks:
        return None
    
    landmarks = results.multi_face_landmarks[0].landmark
    
    # Define landmark coordinates in pixels
    pts = np.array([[int(l.x * w), int(l.y * h)] for l in landmarks])
    
    # Calculate Face Width (distance between leftmost and rightmost edge)
    # Landmark 234: Left side of face, Landmark 454: Right side of face
    x1, y1 = pts[234]
    x2, y2 = pts[454]
    face_width = int(np.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    
    # Size of the patches (around 10% of face width)
    patch_size = max(10, int(face_width * 0.10))
    half_p = patch_size // 2
    
    # Get centers for Left Cheek, Right Cheek, Forehead
    # Landmark 50: Left cheek center
    # Landmark 280: Right cheek center
    # Landmark 9: Forehead center (between brows)
    patch_centers = {
        "left_cheek": pts[50],
        "right_cheek": pts[280],
        "forehead": pts[9]
    }
    
    metrics = []
    annotated_img = img.copy()
    
    # Crop patches and calculate scores
    for name, (cx, cy) in patch_centers.items():
        x_start = max(0, cx - half_p)
        x_end = min(w, cx + half_p)
        y_start = max(0, cy - half_p)
        y_end = min(h, cy + half_p)
        
        patch = img[y_start:y_end, x_start:x_end]
        b_score, s_score, u_score = calculate_patch_metrics(patch)
        metrics.append((b_score, s_score, u_score))
        
        # Draw bounding boxes for patches on the annotated image
        # Green box for Left Cheek, Blue for Right Cheek, Cyan for Forehead
        color = (0, 255, 0) if "left" in name else ((255, 0, 0) if "right" in name else (0, 255, 255))
        cv2.rectangle(annotated_img, (x_start, y_start), (x_end, y_end), color, 2)
        cv2.putText(annotated_img, name.replace("_", " ").title(), (x_start, y_start - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv2.LINE_AA)
        
    # Draw face mesh landmarks on annotated image
    mp_drawing.draw_landmarks(
        image=annotated_img,
        landmark_list=results.multi_face_landmarks[0],
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
    )
    
    # Calculate average scores
    avg_brightness = sum(m[0] for m in metrics) / 3.0
    avg_smoothness = sum(m[1] for m in metrics) / 3.0
    avg_uniformity = sum(m[2] for m in metrics) / 3.0
    
    return {
        "brightness": avg_brightness,
        "smoothness": avg_smoothness,
        "uniformity": avg_uniformity,
        "annotated_img": annotated_img
    }

def get_face_metrics_fallback(img: np.ndarray):
    """
    Fallback method using OpenCV Haar Cascades to detect the face box.
    Crops areas representing forehead and cheeks relative to the face box.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None
    
    # Take the largest face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    
    # Calculate patch size (15% of face width)
    patch_size = max(10, int(w * 0.15))
    half_p = patch_size // 2
    
    # Estimate centers relative to face box (x, y, w, h)
    # Forehead: middle top (x + w/2, y + h/5)
    # Left cheek: left middle-bottom (x + w/4, y + 5*h/8)
    # Right cheek: right middle-bottom (x + 3*w/4, y + 5*h/8)
    patch_centers = {
        "forehead": (x + w // 2, y + h // 5),
        "left_cheek": (x + w // 4, y + 5 * h // 8),
        "right_cheek": (x + 3 * w // 4, y + 5 * h // 8)
    }
    
    metrics = []
    annotated_img = img.copy()
    
    # Draw face box
    cv2.rectangle(annotated_img, (x, y), (x + w, y + h), (255, 0, 255), 2)
    cv2.putText(annotated_img, "Face Detected", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
    
    for name, (cx, cy) in patch_centers.items():
        x_start = max(0, cx - half_p)
        x_end = min(img.shape[1], cx + half_p)
        y_start = max(0, cy - half_p)
        y_end = min(img.shape[0], cy + half_p)
        
        patch = img[y_start:y_end, x_start:x_end]
        b_score, s_score, u_score = calculate_patch_metrics(patch)
        metrics.append((b_score, s_score, u_score))
        
        color = (0, 255, 0) if "left" in name else ((255, 0, 0) if "right" in name else (0, 255, 255))
        cv2.rectangle(annotated_img, (x_start, y_start), (x_end, y_end), color, 2)
        
    avg_brightness = sum(m[0] for m in metrics) / 3.0
    avg_smoothness = sum(m[1] for m in metrics) / 3.0
    avg_uniformity = sum(m[2] for m in metrics) / 3.0
    
    return {
        "brightness": avg_brightness,
        "smoothness": avg_smoothness,
        "uniformity": avg_uniformity,
        "annotated_img": annotated_img
    }

def analyze_face(image_bytes: bytes) -> dict:
    """
    Main entry point to decode image, detect face landmarks, calculate age (DeepFace),
    and estimate skin glow/quality metrics.
    """
    img = decode_image(image_bytes)
    if img is None:
        raise ValueError("Invalid image file or format.")
    
    # 1. Estimate Age with DeepFace
    # We save image temporarily to a temp file since DeepFace prefers file paths or numpy arrays
    temp_path = "temp_face_analysis.jpg"
    cv2.imwrite(temp_path, img)
    
    try:
        from deepface import DeepFace
        logger.info("Running DeepFace analysis for age prediction...")
        # We enforce_detection=False so that if the face detection fails, it still tries to predict on the full image
        analysis = DeepFace.analyze(img_path=temp_path, actions=['age'], enforce_detection=False)
        if isinstance(analysis, list):
            age = int(analysis[0]['age'])
        else:
            age = int(analysis['age'])
        logger.info(f"DeepFace estimated age: {age}")
    except Exception as e:
        logger.error(f"DeepFace analysis failed: {e}. Falling back to default age.")
        age = 25
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
                
    # 2. Estimate Glow Metrics (MediaPipe first, fallback to OpenCV Cascades)
    face_details = None
    if HAS_MEDIAPIPE:
        try:
            face_details = get_face_metrics_mediapipe(img)
        except Exception as e:
            logger.error(f"MediaPipe processing failed: {e}. Falling back to OpenCV Cascades.")
            
    if face_details is None:
        face_details = get_face_metrics_fallback(img)
        
    if face_details is None:
        # No face detected at all
        return {
            "face_detected": False,
            "age": age,
            "glow_score": 0.0,
            "brightness": 0.0,
            "smoothness": 0.0,
            "uniformity": 0.0,
            "annotated_image": encode_image_to_base64(img)
        }
        
    # Combine scores into a final Glow Index
    b_score = face_details["brightness"]
    s_score = face_details["smoothness"]
    u_score = face_details["uniformity"]
    
    # Glow Index Formula
    glow_score = (b_score * 0.4) + (s_score * 0.4) + (u_score * 0.2)
    
    return {
        "face_detected": True,
        "age": age,
        "glow_score": round(glow_score, 1),
        "brightness": round(b_score, 1),
        "smoothness": round(s_score, 1),
        "uniformity": round(u_score, 1),
        "annotated_image": encode_image_to_base64(face_details["annotated_img"])
    }
