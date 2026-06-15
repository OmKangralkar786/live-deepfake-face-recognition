from django.conf import settings
import os
import numpy as np
import cv2
from pathlib import Path

KNOWN_FACE_DIR = settings.MEDIA_ROOT / "known_faces"

MODEL_NAME = "Facenet512"
DETECTION_BACKEND = "opencv"
MATCH_THRESHOLD = 0.23


def recognize_face(captured_image):

    try:

        from deepface import DeepFace

        print("\nStarting Recognition...")
        print("Captured Image:", captured_image)

        if not os.path.exists(KNOWN_FACE_DIR):
            print("known_faces folder not found")
            return []

        known_embeddings = []

        def resolve_image_path(image_path):
            path = Path(image_path)

            if path.exists():
                return path

            if not path.is_absolute():
                candidate = settings.BASE_DIR / path
                if candidate.exists():
                    return candidate

            return path

        def load_image_array(image_path):
            resolved_path = resolve_image_path(image_path)

            if not resolved_path.exists():
                return None

            image = cv2.imread(str(resolved_path))

            if image is not None:
                return image

            image_bytes = np.fromfile(str(resolved_path), dtype=np.uint8)

            if image_bytes.size == 0:
                return None

            return cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        for file in os.listdir(KNOWN_FACE_DIR):

            known_image = KNOWN_FACE_DIR / file

            if not os.path.isfile(known_image):
                continue

            print("\nEncoding Known Face:", known_image)

            known_image_array = load_image_array(known_image)

            if known_image_array is None:
                print("Unable to load known image:", known_image)
                continue

            known_faces = DeepFace.represent(
                img_path=known_image_array,
                model_name=MODEL_NAME,
                detector_backend=DETECTION_BACKEND,
                enforce_detection=False,
            )

            if not known_faces:
                continue

            known_embeddings.append({
                "name": os.path.splitext(file)[0],
                "embedding": np.array(known_faces[0]["embedding"], dtype=float),
            })

        if not known_embeddings:
            print("No known face embeddings found")
            return []

        captured_image_array = load_image_array(captured_image)

        if captured_image_array is None:
            print("Unable to load captured image:", captured_image)
            return []

        detected_faces = DeepFace.represent(
            img_path=captured_image_array,
            model_name=MODEL_NAME,
            detector_backend=DETECTION_BACKEND,
            enforce_detection=False,
            max_faces=None,
        )

        if not detected_faces:
            print("No Face Detected")
            return []

        recognized_people = []

        for detected_face in detected_faces:

            unknown_embedding = np.array(detected_face["embedding"], dtype=float)

            best_match = None
            best_distance = float("inf")

            for known_face in known_embeddings:

                known_embedding = known_face["embedding"]

                denominator = np.linalg.norm(known_embedding) * np.linalg.norm(unknown_embedding)

                if denominator == 0:
                    continue

                distance = 1 - float(np.dot(known_embedding, unknown_embedding) / denominator)

                if distance < best_distance:
                    best_distance = distance
                    best_match = known_face["name"]

            print("Best distance:", best_distance, "Best match:", best_match)

            if best_match is not None and best_distance <= MATCH_THRESHOLD:
                recognized_people.append(best_match)

        return list(dict.fromkeys(recognized_people))
    except Exception as e:

        print("DeepFace Error:", str(e))

        return []