/**
 * CrimeVision AI - Upload Panel Controller
 * Handles drag and drop, file picking, and benchmark evidence preloading
 */
class UploadPanel {
  constructor() {
    this.dropZone = document.getElementById('dropZone');
    this.fileInput = document.getElementById('fileInput');
    this.uploadTitle = document.getElementById('uploadTitle');
    this.uploadIcon = document.getElementById('uploadIcon');
    this.dropPrompt = document.getElementById('dropPrompt');
    this.dropSub = document.getElementById('dropSub');
    this.fileStatusPill = document.getElementById('fileStatusPill');
    this.fileNameDisplay = document.getElementById('fileNameDisplay');
    this.removeFileBtn = document.getElementById('removeFileBtn');
    this.presetBtn = document.getElementById('presetEvidenceBtn');

    this.selectedFile = null;
    this.isPreset = false;
    this.currentMode = 'image';

    this.init();
  }

  init() {
    // Dropzone drag-over events
    ['dragenter', 'dragover'].forEach(eventName => {
      this.dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.dropZone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      this.dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.dropZone.classList.remove('dragover');
      });
    });

    // Handle Drop
    this.dropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      if (dt.files && dt.files.length > 0) {
        this.setFile(dt.files[0]);
      }
    });

    // Handle File Input Change
    this.fileInput.addEventListener('change', () => {
      if (this.fileInput.files && this.fileInput.files.length > 0) {
        this.setFile(this.fileInput.files[0]);
      }
    });

    // Remove File
    this.removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.clearFile();
    });

    // Use Preset Evidence
    this.presetBtn.addEventListener('click', () => {
      this.usePresetEvidence();
    });
  }

  setMode(mode) {
    this.currentMode = mode;
    this.clearFile();

    if (mode === 'image') {
      this.uploadTitle.textContent = 'Upload Image';
      this.uploadIcon.className = 'fa-solid fa-cloud-arrow-up';
      this.dropPrompt.textContent = 'Upload Image';
      this.dropSub.textContent = 'Photos for 3D recovery (JPG, PNG)';
      this.fileInput.accept = 'image/*';
    } else if (mode === 'audio') {
      this.uploadTitle.textContent = 'Upload Audio';
      this.uploadIcon.className = 'fa-solid fa-microphone-lines';
      this.dropPrompt.textContent = 'Upload Audio';
      this.dropSub.textContent = 'Witness statements (.mp3, .wav)';
      this.fileInput.accept = 'audio/*';
    } else if (mode === 'video') {
      this.uploadTitle.textContent = 'Upload Video';
      this.uploadIcon.className = 'fa-solid fa-video';
      this.dropPrompt.textContent = 'Upload Video';
      this.dropSub.textContent = 'CCTV (.mp4, .avi, max 50s)';
      this.fileInput.accept = 'video/*';
    }
  }

  setFile(file) {
    this.selectedFile = file;
    this.isPreset = false;
    this.fileNameDisplay.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;
    this.fileStatusPill.classList.remove('hidden');
  }

  usePresetEvidence() {
    this.isPreset = true;
    this.selectedFile = null;

    let presetName = 'sample_crime_scene.jpg (Preloaded Office)';
    if (this.currentMode === 'audio') {
      presetName = 'sample_robbery_witness.wav (Maple Ave Testimony)';
    } else if (this.currentMode === 'video') {
      presetName = 'sample_surveillance_store.mp4 (CCTV Mall 15s)';
    }

    this.fileNameDisplay.textContent = presetName;
    this.fileStatusPill.classList.remove('hidden');
  }

  clearFile() {
    this.selectedFile = null;
    this.isPreset = false;
    this.fileInput.value = '';
    this.fileStatusPill.classList.add('hidden');
  }

  getFiles() {
    return this.selectedFile;
  }
}

window.UploadPanel = UploadPanel;
