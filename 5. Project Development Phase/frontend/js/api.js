/**
 * CrimeVision AI - API Client
 * Matches specification from Activity 6.1 (Page 25)
 */
const API_BASE_URL = window.location.origin.includes('5000') 
  ? `${window.location.origin}/api` 
  : 'http://localhost:5000/api';

class API {
  /**
   * 1. Universal File Uploader
   */
  static async uploadBatch(files) {
    const formData = new FormData();
    if (files instanceof FileList || Array.isArray(files)) {
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }
    } else if (files instanceof File) {
      formData.append('files', files);
    }

    const response = await fetch(`${API_BASE_URL}/upload/batch`, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  }

  /**
   * 2. Specialized Pipeline Triggers (Full Multimodal)
   */
  static async processCompletePipeline(caseId = "default") {
    const response = await fetch(`${API_BASE_URL}/process/complete/${caseId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    return await response.json();
  }

  /**
   * 3. Direct Module Access (Fast Path)
   */
  static async analyzeImage(fileOrPath) {
    if (typeof fileOrPath === 'string') {
      const response = await fetch(`${API_BASE_URL}/process/image`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_path: fileOrPath })
      });
      return await response.json();
    }
    const formData = new FormData();
    if (fileOrPath instanceof File) {
      formData.append('file', fileOrPath);
    }
    const response = await fetch(`${API_BASE_URL}/process/image`, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  }

  static async analyzeAudio(fileOrPath) {
    if (typeof fileOrPath === 'string') {
      const response = await fetch(`${API_BASE_URL}/analyze-audio`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ audio_path: fileOrPath })
      });
      return await response.json();
    }
    const formData = new FormData();
    if (fileOrPath instanceof File) {
      formData.append('file', fileOrPath);
    }
    const response = await fetch(`${API_BASE_URL}/analyze-audio`, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  }

  static async analyzeVideo(fileOrPath) {
    if (typeof fileOrPath === 'string') {
      const response = await fetch(`${API_BASE_URL}/analyze-video`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_path: fileOrPath })
      });
      return await response.json();
    }
    const formData = new FormData();
    if (fileOrPath instanceof File) {
      formData.append('file', fileOrPath);
    }
    const response = await fetch(`${API_BASE_URL}/analyze-video`, {
      method: 'POST',
      body: formData
    });
  }

  /**
   * OpenCV Video Detection & Evidence Prediction API
   * Predicts objects, people, vehicles, 2D boxes, 3D trajectories, and timeline
   */
  static async opencvPredictVideo(fileOrPath) {
    if (typeof fileOrPath === 'string') {
      const response = await fetch(`${API_BASE_URL}/video/opencv-predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_path: fileOrPath })
      });
      return await response.json();
    }
    const formData = new FormData();
    if (fileOrPath instanceof File) {
      formData.append('file', fileOrPath);
    }
    const response = await fetch(`${API_BASE_URL}/video/opencv-predict`, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  }

  /**
   * 4. Forensic Chatbot
   */
  static async chat(mode, session_id, question) {
    const response = await fetch(`${API_BASE_URL}/chat/${mode}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id, question })
    });
    return await response.json();
  }

  /**
   * 5. Download Report URL
   */
  static getReportUrl(session_id) {
    return `${API_BASE_URL}/report/download/${session_id}`;
  }

  /**
   * 6. Health Check
   */
  static async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await response.json();
    } catch (e) {
      return { status: 'offline' };
    }
  }
}

window.API = API;
