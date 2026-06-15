from django.http import HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.deepface_utils import recognize_face
def home(request):
    return HttpResponse("Live Deepfake Detection Backend Running")


@api_view(['GET'])
def test(request):
    return Response({
        "message": "Backend Working"
    })


@api_view(['POST'])
def detect(request):

    import os
    import uuid
    import base64

    image = request.data.get("image")

    if not image:
        return Response({
            "status": "failed"
        })

    header, encoded = image.split(",")

    image_data = base64.b64decode(encoded)

    captured_dir = settings.MEDIA_ROOT / "captured"

    os.makedirs(
        captured_dir,
        exist_ok=True
    )

    filename = f"{uuid.uuid4()}.jpg"

    filepath = captured_dir / filename

    with open(filepath, "wb") as f:
        f.write(image_data)

    print("Image Saved:", filepath)

    recognized_people = recognize_face(str(filepath))

    return Response({
        "status": "received",
        "person": recognized_people[0] if recognized_people else "Unknown Person",
        "persons": recognized_people,
        "image": filename
    })