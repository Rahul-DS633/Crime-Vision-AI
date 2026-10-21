/**
 * CrimeVision AI - Upload Panel Controller
 * Handles drag and drop, file picking, auto-mode switching, and instant evidence processing
 */
class UploadPanel {
  constructor(onFileReady = null, onModeSwitch = null) {
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

    this.onFileReady = onFileReady;
    this.onModeSwitch = onModeSwitch;

    this.selectedFile = null;
    this.isPreset = false;
    this.presetPath = null;
    this.currentMode = 'image';

    this.init();
  }

  detectFileType(file) {
    if (!file) return 'image';
    const name = (file.name || '').toLowerCase();
    const type = (file.type || '').toLowerCase();

    if (type.startsWith('video/') || /\.(mp4|avi|mov|webm|mkv|flv|wmv)$/i.test(name)) {
      return 'video';
    }
    if (type.startsWith('audio/') || /\.(wav|mp3|ogg|flac|aac|m4a|wma)$/i.test(name)) {
      return 'audio';
    }
    return 'image';
  }

  init() {
    // Dropzone drag-over visual feedback
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

    // Handle Drop with Auto-Detection & Immediate Processing
    this.dropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      if (dt.files && dt.files.length > 0) {
        const file = dt.files[0];
        const detectedMode = this.detectFileType(file);
        
        // Auto-switch mode if mismatched
        if (detectedMode !== this.currentMode && this.onModeSwitch) {
          this.onModeSwitch(detectedMode);
        }

        this.setFile(file);

        // Auto-trigger analysis immediately on drop
        if (this.onFileReady) {
          this.onFileReady(file, false);
        }
      }
    });

    // Handle File Input Change
    this.fileInput.addEventListener('change', () => {
      if (this.fileInput.files && this.fileInput.files.length > 0) {
        const file = this.fileInput.files[0];
        const detectedMode = this.detectFileType(file);

        if (detectedMode !== this.currentMode && this.onModeSwitch) {
          this.onModeSwitch(detectedMode);
        }

        this.setFile(file);

        // Auto-trigger analysis
        if (this.onFileReady) {
          this.onFileReady(file, false);
        }
      }
    });

    // Remove File
    this.removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.clearFile();
    });

    // Use Benchmark Preset
    if (this.presetBtn) {
      this.presetBtn.addEventListener('click', () => {
        this.usePresetEvidence();
      });
    }

    // Real-Life Dataset Presets
    const storeCctvBtn = document.getElementById('presetStoreCctvBtn');
    if (storeCctvBtn) {
      storeCctvBtn.addEventListener('click', () => {
        if (this.onModeSwitch) this.onModeSwitch('video');
        this.loadPresetDirect(
          'real_cctv_surveillance_store.mp4 (Real Mall CCTV 65s)',
          'samples/video/real_cctv_surveillance_store.mp4',
          'video'
        );
      });
    }

    const trafficCctvBtn = document.getElementById('presetTrafficCctvBtn');
    if (trafficCctvBtn) {
      trafficCctvBtn.addEventListener('click', () => {
        if (this.onModeSwitch) this.onModeSwitch('video');
        this.loadPresetDirect(
          'real_intersection_surveillance.mp4 (Traffic CCTV 54s)',
          'samples/video/real_intersection_surveillance.mp4',
          'video'
        );
      });
    }

    const realImgBtn = document.getElementById('presetRealImageBtn');
    if (realImgBtn) {
      realImgBtn.addEventListener('click', () => {
        if (this.onModeSwitch) this.onModeSwitch('image');
        this.loadPresetDirect(
          'real_street_traffic_surveillance.jpg (Street Traffic Crime Scene)',
          'samples/image/real_street_traffic_surveillance.jpg',
          'image'
        );
      });
    }

    const realAudioBtn = document.getElementById('presetRealAudioBtn');
    if (realAudioBtn) {
      realAudioBtn.addEventListener('click', () => {
        if (this.onModeSwitch) this.onModeSwitch('audio');
        this.loadPresetDirect(
          'case01_distress_call_911.wav (Real 911 Emergency Audio)',
          'samples/audio/case01_distress_call_911.wav',
          'audio'
        );
      });
    }
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
      this.dropSub.textContent = 'Witness & 911 audio (.mp3, .wav)';
      this.fileInput.accept = 'audio/*';
    } else if (mode === 'video') {
      this.uploadTitle.textContent = 'Upload Video';
      this.uploadIcon.className = 'fa-solid fa-video';
      this.dropPrompt.textContent = 'Upload Video';
      this.dropSub.textContent = 'CCTV (.mp4, .avi, 3D tracking)';
      this.fileInput.accept = 'video/*';
    }
  }

  setFile(file) {
    this.selectedFile = file;
    this.isPreset = false;
    this.presetPath = null;
    this.fileNameDisplay.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;
    this.fileStatusPill.classList.remove('hidden');
  }

  loadPresetDirect(displayName, path, mode) {
    this.isPreset = true;
    this.selectedFile = null;
    this.presetPath = path;
    this.fileNameDisplay.textContent = displayName;
    this.fileStatusPill.classList.remove('hidden');

    if (this.onFileReady) {
      this.onFileReady(null, true, path);
    }
  }

  usePresetEvidence() {
    this.isPreset = true;
    this.selectedFile = null;

    let presetName = 'real_street_traffic_surveillance.jpg (Street Traffic Crime Scene)';
    let path = 'samples/image/real_street_traffic_surveillance.jpg';
    if (this.currentMode === 'audio') {
      presetName = 'case01_distress_call_911.wav (Real 911 Emergency Audio)';
      path = 'samples/audio/case01_distress_call_911.wav';
    } else if (this.currentMode === 'video') {
      presetName = 'real_cctv_surveillance_store.mp4 (Real Mall CCTV 65s)';
      path = 'samples/video/real_cctv_surveillance_store.mp4';
    }

    this.loadPresetDirect(presetName, path, this.currentMode);
  }

  clearFile() {
    this.selectedFile = null;
    this.isPreset = false;
    this.presetPath = null;
    this.fileInput.value = '';
    this.fileStatusPill.classList.add('hidden');
  }

  getFiles() {
    return this.selectedFile;
  }
}

window.UploadPanel = UploadPanel;

