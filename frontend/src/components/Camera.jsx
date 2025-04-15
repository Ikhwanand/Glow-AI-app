import React, { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";

const Camera = ({ onCapture, onClose }) => {
  const webcamRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      onCapture(imageSrc);
    }
  }, [webcamRef, onCapture]);

  return (
    <div className="card p-4">
      <h2 className="text-xl font-semibold mb-4">Take a Photo</h2>

      {!isCameraActive ? (
        <div className="space-y-4">
          <button 
            className="btn-primary w-full" 
            onClick={() => setIsCameraActive(true)}
          >
            Activate Camera
          </button>
          <button className="btn-secondary w-full" onClick={onClose}>
            Cancel
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="w-full rounded-lg"
          />
          <div className="flex gap-2">
            <button className="btn-primary flex-1" onClick={capture}>
              Capture Photo
            </button>
            <button 
              className="btn-secondary flex-1" 
              onClick={() => setIsCameraActive(false)}
            >
              Retake
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Camera;