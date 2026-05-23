import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Analyze.css';

function Analyze() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showCamera, setShowCamera] = useState(false);
  const [stream, setStream] = useState(null);
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
      }
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      handleFileSelect({ target: { files: [file] } });
    }
  };

  const openCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(mediaStream);
      setShowCamera(true);
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      }, 100);
    } catch (error) {
      alert('Unable to access camera. Please check permissions.');
    }
  };

  const closeCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }
    setShowCamera(false);
    setStream(null);
  };

  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    canvas.toBlob((blob) => {
      const file = new File([blob], 'captured-photo.jpg', { type: 'image/jpeg' });
      setSelectedFile(file);
      setPreview(canvas.toDataURL('image/jpeg'));
      closeCamera();
    }, 'image/jpeg');
  };

  const analyzeImage = async () => {
    if (!selectedFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        withCredentials: true
      });

      if (response.data.success) {
        sessionStorage.setItem('analysisResults', JSON.stringify(response.data.predictions));
        sessionStorage.setItem('analysisImage', preview);
        navigate('/report');
      }
    } catch (error) {
      alert(error.response?.data?.error || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analyze-page">
      <div className="analyze-container">
        <div className="page-header">
          <h1>📸 Upload or Capture Image</h1>
          <p>Upload a clear image of the skin condition for analysis</p>
        </div>

        <div
          className={`upload-section ${preview ? 'has-image' : ''}`}
          onClick={() => fileInputRef.current.click()}
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
        >
          {!preview ? (
            <div className="upload-prompt">
              <div className="upload-icon">📤</div>
              <div className="upload-text">Click to upload or drag & drop</div>
              <div className="upload-subtext">Supports JPG, PNG, JPEG (Max 10MB)</div>
            </div>
          ) : (
            <img src={preview} alt="Preview" className="image-preview" />
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </div>

        <div className="button-group">
          <button className="btn btn-success" onClick={openCamera}>
            📷 Capture Photo
          </button>
          <button
            className="btn btn-primary"
            onClick={analyzeImage}
            disabled={!selectedFile || loading}
          >
            {loading ? '⏳ Analyzing...' : '🔍 Analyze Image'}
          </button>
        </div>

        {loading && <div className="loader"></div>}

        <div className="instructions">
          <h3>📋 Tips for Best Results</h3>
          <ul>
            <li>Ensure good lighting when taking photos</li>
            <li>Keep the camera steady and focused</li>
            <li>Capture the affected area clearly</li>
            <li>Avoid blurry or dark images</li>
            <li>Include some surrounding healthy skin for context</li>
          </ul>
        </div>
      </div>

      {showCamera && (
        <div className="camera-modal" onClick={closeCamera}>
          <div className="camera-container" onClick={(e) => e.stopPropagation()}>
            <h2>📷 Capture Photo</h2>
            <video ref={videoRef} autoPlay className="camera-video"></video>
            <div className="camera-buttons">
              <button className="btn btn-success" onClick={capturePhoto}>Capture</button>
              <button className="btn btn-secondary" onClick={closeCamera}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Analyze;
