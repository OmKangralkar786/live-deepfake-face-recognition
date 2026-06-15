import { useRef, useState } from "react";
import Webcam from "react-webcam";
import api from "../services/api";

function Camera() {
    const webcamRef = useRef(null);

    const [image, setImage] = useState(null);
    const [result, setResult] = useState("");
    const [loading, setLoading] = useState(false);

    const capture = async () => {

        try {

            setLoading(true);

            const video = webcamRef.current.video;

            const canvas = document.createElement("canvas");

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            const ctx = canvas.getContext("2d");

            ctx.drawImage(
                video,
                0,
                0,
                canvas.width,
                canvas.height
            );

            const imageSrc = canvas.toDataURL("image/jpeg");

            setImage(imageSrc);

            const response = await api.post(
                "detect/",
                {
                    image: imageSrc
                }
            );

            const people = response.data.persons ?? [];

            setResult(
                people.length > 0
                    ? people.join(", ")
                    : response.data.person
            );

        } catch (error) {

            console.log(error);

            setResult("Recognition Failed");

        } finally {

            setLoading(false);

        }
    };

    return (
        <div
            style={{
                minHeight: "100vh",
                background:
                    "linear-gradient(135deg,#0f172a,#1e293b,#111827)",
                color: "white",
                padding: "30px"
            }}
        >
            <div className="container">

                <div className="text-center mb-5">

                    <h1
                        className="fw-bold"
                        style={{
                            fontSize: "3rem"
                        }}
                    >
                        AI Face Recognition
                    </h1>

                    <p
                        className="text-light"
                    >
                        Live Deepfake Detection &
                        Face Recognition System
                    </p>

                </div>

                <div className="row">

                    <div className="col-lg-7">

                        <div
                            className="p-4"
                            style={{
                                background:
                                    "rgba(255,255,255,0.08)",
                                backdropFilter:
                                    "blur(15px)",
                                borderRadius: "20px",
                                border:
                                    "1px solid rgba(255,255,255,0.1)"
                            }}
                        >

                            <h4 className="mb-3">
                                Live Camera
                            </h4>

                            <Webcam
                                ref={webcamRef}
                                audio={false}
                                screenshotFormat="image/jpeg"
                                className="img-fluid rounded"
                            />

                            <button
                                className="btn btn-primary btn-lg mt-4 w-100"
                                onClick={capture}
                                disabled={loading}
                            >
                                {
                                    loading
                                        ? "Recognizing..."
                                        : "Capture & Recognize"
                                }
                            </button>

                        </div>

                    </div>

                    <div className="col-lg-5">

                        <div
                            className="p-4"
                            style={{
                                background:
                                    "rgba(255,255,255,0.08)",
                                backdropFilter:
                                    "blur(15px)",
                                borderRadius: "20px",
                                border:
                                    "1px solid rgba(255,255,255,0.1)"
                            }}
                        >

                            <h4>
                                Recognition Result
                            </h4>

                            <hr />

                            {
                                result ? (
                                    <div
                                        className="alert alert-success"
                                    >
                                        <h5>
                                            Detected:
                                        </h5>

                                        <h2>
                                            {result}
                                        </h2>
                                    </div>
                                ) : (
                                    <div
                                        className="alert alert-secondary"
                                    >
                                        Waiting for recognition...
                                    </div>
                                )
                            }

                            {
                                image && (
                                    <>
                                        <h5 className="mt-4">
                                            Captured Image
                                        </h5>

                                        <img
                                            src={image}
                                            alt="Captured"
                                            className="img-fluid rounded shadow"
                                        />
                                    </>
                                )
                            }

                        </div>

                    </div>

                </div>

            </div>
        </div>
    );
}

export default Camera;