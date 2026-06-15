import face_recognition
import os


KNOWN_FACE_DIR = "media/known_faces"


def recognize_face(image_path):

    known_encodings = []
    known_names = []

    for file in os.listdir(KNOWN_FACE_DIR):

        image = face_recognition.load_image_file(
            os.path.join(KNOWN_FACE_DIR, file)
        )

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:

            known_encodings.append(
                encodings[0]
            )

            known_names.append(
                os.path.splitext(file)[0]
            )

    if not known_encodings:
        return []

    unknown_image = face_recognition.load_image_file(
        image_path
    )

    unknown_encodings = face_recognition.face_encodings(
        unknown_image
    )

    if len(unknown_encodings) == 0:
        return []

    recognized_names = []

    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(
            known_encodings,
            unknown_encoding
        )

        if len(distances) == 0:
            continue

        best_index = distances.argmin()

        if distances[best_index] <= 0.6:
            recognized_names.append(known_names[best_index])

    return list(dict.fromkeys(recognized_names))