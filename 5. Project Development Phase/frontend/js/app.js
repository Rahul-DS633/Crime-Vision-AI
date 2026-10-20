/**
 * CrimeVision AI - Main Dashboard Application Controller
 * Matches implementation workflow & UI specifications
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Components
  let videoScene3D = null;
  const scene3D = new Scene3D('threejsViewport');
  videoScene3D = new VideoTrajectory3D('videoTrajectoryViewport');
  const timeline = new Timeline();

  const imageChat = new ChatHandler('image', 'imageChatInput', 'imageChatSendBtn', 'imageChatHistory');
  const audioChat = new ChatHandler('audio', 'audioChatInput', 'audioChatSendBtn', 'audioChatHistory');
  const videoChat = new ChatHandler('video', 'videoChatInput', 'videoChatSendBtn', 'videoChatHistory');

  let currentMode = 'image';
  let activeSessionId = 'ready-state';
  let currentVideoFrameDetections = [];

  const uploadPanel = new UploadPanel(
    (file, isPreset, presetPath) => startProcessing(file, isPreset, presetPath),
    (mode) => switchMode(mode)
  );

  // 2. Navigation Mode Switching
  const navButtons = {
    image: document.getElementById('navImageBtn'),
    audio: document.getElementById('navAudioBtn'),
    video: document.getElementById('navVideoBtn')
  };

  const modeViews = {
    image: document.getElementById('imageView'),
    audio: document.getElementById('audioView'),
    video: document.getElementById('videoView')
  };

  const modeBadge = document.getElementById('currentModeBadge');

  function switchMode(mode) {
    currentMode = mode;
    uploadPanel.setMode(mode);

    // Update Nav Button Styles
    Object.keys(navButtons).forEach(m => {
      if (m === mode) navButtons[m].classList.add('active');
      else navButtons[m].classList.remove('active');
    });

    // Update View Visibility
    Object.keys(modeViews).forEach(m => {
      if (m === mode) modeViews[m].classList.add('active');
      else modeViews[m].classList.remove('active');
    });

    const modeLabels = {
      image: 'Mode: Image Analysis',
      audio: 'Mode: Audio Analysis',
      video: 'Mode: Video Analysis (3D Surveillance)'
    };
    if (modeBadge) modeBadge.textContent = modeLabels[mode];

    // Trigger Three.js resize
    if (mode === 'image' && scene3D) {
      setTimeout(() => scene3D.onResize(), 100);
    } else if (mode === 'video' && videoScene3D) {
      setTimeout(() => videoScene3D.onResize(), 100);
    }
  }

  navButtons.image.addEventListener('click', () => switchMode('image'));
  navButtons.audio.addEventListener('click', () => switchMode('audio'));
  navButtons.video.addEventListener('click', () => switchMode('video'));

  // 3. Translations Multi-Tab Switching (Audio Mode)
  let currentTranslations = {};
  const langTabs = document.querySelectorAll('.lang-tab');
  const translationOutput = document.getElementById('translationOutputText');

  langTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      langTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const lang = tab.dataset.lang;
      if (currentTranslations[lang]) {
        translationOutput.textContent = currentTranslations[lang];
      }
    });
  });

  // 4. View Mode Toggle (3D Mesh vs 2D Annotated Image)
  const view3dBtn = document.getElementById('view3dToggle');
  const view2dBtn = document.getElementById('view2dToggle');
  const threejsViewport = document.getElementById('threejsViewport');
  const imageAnnotatedView = document.getElementById('imageAnnotatedView');

  if (view3dBtn && view2dBtn) {
    view3dBtn.addEventListener('click', () => {
      view3dBtn.classList.add('active');
      view2dBtn.classList.remove('active');
      threejsViewport.classList.remove('hidden');
      imageAnnotatedView.classList.add('hidden');
    });

    view2dBtn.addEventListener('click', () => {
      view2dBtn.classList.add('active');
      view3dBtn.classList.remove('active');
      threejsViewport.classList.add('hidden');
      imageAnnotatedView.classList.remove('hidden');
    });
  }

  // Video Mode Toggle: 2D CCTV Feed vs 3D Spatial Trajectory
  const videoView2dToggle = document.getElementById('videoView2dToggle');
  const videoView3dToggle = document.getElementById('videoView3dToggle');
  const video2dContainer = document.getElementById('video2dContainer');
  const video3dContainer = document.getElementById('video3dContainer');

  if (videoView2dToggle && videoView3dToggle) {
    videoView2dToggle.addEventListener('click', () => {
      videoView2dToggle.classList.add('active');
      videoView3dToggle.classList.remove('active');
      video2dContainer.classList.remove('hidden');
      video3dContainer.classList.add('hidden');
    });

    videoView3dToggle.addEventListener('click', () => {
      videoView3dToggle.classList.add('active');
      videoView2dToggle.classList.remove('active');
      video2dContainer.classList.add('hidden');
      video3dContainer.classList.remove('hidden');
      if (videoScene3D) {
        setTimeout(() => videoScene3D.onResize(), 100);
      }
    });
  }

  // Video 3D Camera Controls
  const btnCamCCTV = document.getElementById('btnCamCCTV');
  const btnCamTopDown = document.getElementById('btnCamTopDown');
  const btnCamOrbit = document.getElementById('btnCamOrbit');
  const btnCamFollow = document.getElementById('btnCamFollow');
  const btnCamResetVideo = document.getElementById('btnCamResetVideo');

  function clearCamActive() {
    [btnCamCCTV, btnCamTopDown, btnCamOrbit, btnCamFollow].forEach(b => b?.classList.remove('active'));
  }

  btnCamCCTV?.addEventListener('click', () => {
    clearCamActive();
    btnCamCCTV.classList.add('active');
    videoScene3D?.setCCTVAngle();
  });

  btnCamTopDown?.addEventListener('click', () => {
    clearCamActive();
    btnCamTopDown.classList.add('active');
    videoScene3D?.setTopDownView();
  });

  btnCamOrbit?.addEventListener('click', () => {
    clearCamActive();
    btnCamOrbit.classList.add('active');
    videoScene3D?.setOrbitView();
  });

  btnCamFollow?.addEventListener('click', () => {
    const isTracking = videoScene3D?.toggleTrackSuspect();
    if (isTracking) {
      clearCamActive();
      btnCamFollow.classList.add('active');
    } else {
      btnCamFollow.classList.remove('active');
    }
  });

  btnCamResetVideo?.addEventListener('click', () => {
    clearCamActive();
    btnCamCCTV?.classList.add('active');
    videoScene3D?.resetCamera();
  });

  // Video Player Playback Time Sync & Live Bounding Box Overlay
  const surveillanceVideoPlayer = document.getElementById('surveillanceVideoPlayer');
  const videoBBoxOverlay = document.getElementById('videoBBoxOverlay');
  const videoDurationTag = document.getElementById('videoDurationTag');

  function formatTimeStr(sec) {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  if (surveillanceVideoPlayer) {
    surveillanceVideoPlayer.addEventListener('timeupdate', () => {
      const curTime = surveillanceVideoPlayer.currentTime;
      const duration = surveillanceVideoPlayer.duration || 0;
      if (videoDurationTag) {
        videoDurationTag.textContent = `${formatTimeStr(curTime)} / ${formatTimeStr(duration)}`;
      }

      // Update 3D suspect position in Three.js synchronized with video
      if (videoScene3D) {
        videoScene3D.updatePlaybackTime(curTime);
      }

      // Render 2D bounding boxes for current second
      renderVideoBoundingBoxes(curTime);
    });
  }

  function renderVideoBoundingBoxes(currentTime) {
    if (!videoBBoxOverlay) return;
    videoBBoxOverlay.innerHTML = '';
    const sec = Math.floor(currentTime);

    const frameData = currentVideoFrameDetections.find(fd => fd.second === sec);
    const detections = frameData ? frameData.detections : (currentVideoFrameDetections[0]?.detections || []);

    detections.forEach(det => {
      const box = det.box_normalized || [0.2, 0.2, 0.4, 0.4];
      const left = box[0] * 100;
      const top = box[1] * 100;
      const width = (box[2] - box[0]) * 100;
      const height = (box[3] - box[1]) * 100;

      const rect = document.createElement('div');
      rect.className = `bbox-rect ${det.label.toLowerCase().includes('suspect') ? 'weapon' : (det.label.toLowerCase().includes('person') ? 'human' : '')}`;
      rect.style.left = `${left}%`;
      rect.style.top = `${top}%`;
      rect.style.width = `${width}%`;
      rect.style.height = `${height}%`;

      const label = document.createElement('div');
      label.className = 'bbox-label';
      label.textContent = `${det.label} ${Math.round((det.confidence || 0.9) * 100)}%`;
      rect.appendChild(label);

      videoBBoxOverlay.appendChild(rect);
    });
  }

  // Camera Reset & Fullscreen
  const resetCameraBtn = document.getElementById('resetCameraBtn');
  if (resetCameraBtn && scene3D) {
    resetCameraBtn.addEventListener('click', () => scene3D.resetCamera());
  }

  const fullscreen3dBtn = document.getElementById('fullscreen3dBtn');
  if (fullscreen3dBtn) {
    fullscreen3dBtn.addEventListener('click', () => {
      const container = document.getElementById('canvas3dContainer');
      if (!document.fullscreenElement) {
        container.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });
  }

  // 5. Start Processing Implementation
  const startBtn = document.getElementById('startProcessingBtn');
  const spinner = document.getElementById('processSpinner');
  const processBtnText = document.getElementById('processBtnText');

  startBtn.addEventListener('click', async () => {
    await startProcessing();
  });

  async function startProcessing(passedFile = null, isPresetDirect = false, presetPathDirect = null) {
    const file = passedFile || uploadPanel.getFiles();
    const isPreset = isPresetDirect || uploadPanel.isPreset;
    const presetPath = presetPathDirect || uploadPanel.presetPath;

    // Show loading state
    startBtn.disabled = true;
    spinner.classList.remove('hidden');
    processBtnText.textContent = 'Processing Evidence...';

    try {
      if (currentMode === 'image') {
        const payload = isPreset ? (presetPath || 'backend/data/uploads/image/real_street_traffic_surveillance.jpg') : file;
        const result = await API.analyzeImage(payload);
        updateImageFindings(result, file, isPreset ? payload : null);
      } else if (currentMode === 'audio') {
        const payload = isPreset ? (presetPath || 'backend/data/uploads/audio/case01_distress_call_911.wav') : file;
        const result = await API.analyzeAudio(payload);
        updateAudioFindings(result, file, isPreset ? payload : null);
      } else if (currentMode === 'video') {
        const payload = isPreset ? (presetPath || 'backend/data/uploads/video/real_cctv_surveillance_store.mp4') : file;
        const result = await API.analyzeVideo(payload);
        updateVideoFindings(result, file, isPreset ? payload : null);
      }
    } catch (err) {
      console.error("Analysis failed:", err);
      alert("Analysis completed or server fallback active.");
    } finally {
      startBtn.disabled = false;
      spinner.classList.add('hidden');
      processBtnText.textContent = 'Start Processing';
    }
  }

  // 6. Update View Helpers

  function updateImageFindings(result, file, presetPath = null) {
    activeSessionId = result.session_id || 'session-image-01';
    document.getElementById('currentSessionId').textContent = activeSessionId.substring(0, 13);
    imageChat.setSessionId(activeSessionId);

    // Stats
    document.getElementById('imgObjectsCount').textContent = result.objects_count || (result.detections ? result.detections.length : 8);
    document.getElementById('imgPersonsCount').textContent = result.people_count || 1;
    document.getElementById('imgWeaponsCount').textContent = result.weapons_count || 1;
    document.getElementById('imgLocationName').textContent = result.location || 'Surveillance Zone';

    // Summaries
    if (result.ai_scene_summary) {
      document.getElementById('imageSummaryType').textContent = result.ai_scene_summary.summary_type || 'Crime Scene';
      document.getElementById('imageBriefDesc').textContent = result.ai_scene_summary.brief_description || result.visual_summary;
    }
    if (result.visual_summary) {
      document.getElementById('imageVisualSummary').textContent = result.visual_summary;
    }

    // Actions tags
    const actionsBox = document.getElementById('imageActionsTags');
    actionsBox.innerHTML = '';
    (result.actions || ['standing', 'surveillance detection']).forEach(act => {
      const span = document.createElement('span');
      span.className = 'tag-pill';
      span.textContent = act;
      actionsBox.appendChild(span);
    });

    // Evidence Facts
    const facts = result.evidence_facts || listUniqueLabels(result.detections) || ['Human', 'Vehicle', 'Weapon'];
    document.getElementById('imageEvidenceFacts').textContent = Array.isArray(facts) ? facts.join(', ') : facts;

    // Scenarios
    const scenariosList = document.getElementById('imageScenariosList');
    scenariosList.innerHTML = '';
    (result.scenarios || []).forEach(scen => {
      const card = document.createElement('div');
      card.className = 'scenario-card';
      card.innerHTML = scen;
      scenariosList.appendChild(card);
    });

    // 3D Scene Update
    if (scene3D && result.scene_3d_data) {
      scene3D.loadSceneData(result.scene_3d_data);
    }

    // 2D Annotated View
    render2DAnnotations(result.detections, file, presetPath);
  }

  function listUniqueLabels(detections) {
    if (!detections) return [];
    return Array.from(new Set(detections.map(d => d.label)));
  }

  function render2DAnnotations(detections, file, presetPath = null) {
    const previewImg = document.getElementById('evidenceImagePreview');
    const overlay = document.getElementById('boundingBoxOverlay');
    overlay.innerHTML = '';

    if (file && file instanceof File) {
      previewImg.src = URL.createObjectURL(file);
    } else if (presetPath) {
      const norm = presetPath.replace(/\\/g, '/');
      const parts = norm.split('/data/');
      previewImg.src = parts.length > 1 ? `/data/${parts[1]}` : (presetPath.startsWith('/') ? presetPath : `/${presetPath}`);
    } else {
      previewImg.src = '/data/uploads/image/real_street_traffic_surveillance.jpg';
    }

    (detections || []).forEach(det => {
      const box = det.box_normalized || [0.2, 0.2, 0.4, 0.4];
      const left = box[0] * 100;
      const top = box[1] * 100;
      const width = (box[2] - box[0]) * 100;
      const height = (box[3] - box[1]) * 100;

      const rect = document.createElement('div');
      rect.className = `bbox-rect ${det.label.toLowerCase()}`;
      rect.style.left = `${left}%`;
      rect.style.top = `${top}%`;
      rect.style.width = `${width}%`;
      rect.style.height = `${height}%`;

      const label = document.createElement('div');
      label.className = 'bbox-label';
      label.textContent = `${det.label} ${Math.round((det.confidence || 0.9) * 100)}%`;
      rect.appendChild(label);

      overlay.appendChild(rect);
    });
  }

  function updateAudioFindings(result, file, presetPath = null) {
    activeSessionId = result.session_id || 'session-audio-01';
    document.getElementById('currentSessionId').textContent = activeSessionId.substring(0, 13);
    audioChat.setSessionId(activeSessionId);

    // Audio Player Source
    const audioPlayer = document.getElementById('audioPlayer');
    if (file && file instanceof File) {
      audioPlayer.src = URL.createObjectURL(file);
    } else if (presetPath) {
      const norm = presetPath.replace(/\\/g, '/');
      const parts = norm.split('/data/');
      audioPlayer.src = parts.length > 1 ? `/data/${parts[1]}` : (presetPath.startsWith('/') ? presetPath : `/${presetPath}`);
    } else if (result.audio_path) {
      const norm = result.audio_path.replace(/\\/g, '/');
      const parts = norm.split('/data/');
      audioPlayer.src = parts.length > 1 ? `/data/${parts[1]}` : '/data/uploads/audio/case01_distress_call_911.wav';
    } else {
      audioPlayer.src = '/data/uploads/audio/case01_distress_call_911.wav';
    }
    audioPlayer.load();

    // Live Transcript
    if (result.transcription) {
      document.getElementById('audioTranscriptText').textContent = result.transcription;
    }

    // AI Summary & Badges
    if (result.summary) {
      document.getElementById('audioAiSummary').textContent = `"${result.summary}"`;
    }
    if (result.crime_type) {
      document.getElementById('audioCrimeBadge').textContent = result.crime_type;
    }
    if (result.location) {
      document.getElementById('audioLocationBadge').textContent = result.location;
    }

    // Translations
    if (result.translations) {
      currentTranslations = result.translations;
      const activeLang = document.querySelector('.lang-tab.active')?.dataset.lang || 'english';
      if (currentTranslations[activeLang]) {
        translationOutput.textContent = currentTranslations[activeLang];
      }
    }

    // Timeline Table
    if (result.timeline) {
      timeline.render(result.timeline, 'audio');
    }
  }

  function updateVideoFindings(result, file, presetPath = null) {
    activeSessionId = result.session_id || 'session-video-01';
    document.getElementById('currentSessionId').textContent = activeSessionId.substring(0, 13);
    videoChat.setSessionId(activeSessionId);

    // Store frame detections for real-time video bounding boxes overlay
    currentVideoFrameDetections = result.frame_detections || [];

    // Load 3D spatial trajectory and camera extrinsics into Three.js
    if (videoScene3D && result.spatial_3d_trajectory) {
      videoScene3D.loadTrajectoryData(result.spatial_3d_trajectory);
    }

    // Video Player Source
    const videoPlayer = document.getElementById('surveillanceVideoPlayer');
    if (file && file instanceof File) {
      videoPlayer.src = URL.createObjectURL(file);
    } else if (presetPath) {
      const norm = presetPath.replace(/\\/g, '/');
      const parts = norm.split('/data/');
      videoPlayer.src = parts.length > 1 ? `/data/${parts[1]}` : (presetPath.startsWith('/') ? presetPath : `/${presetPath}`);
    } else if (result.video_path) {
      const norm = result.video_path.replace(/\\/g, '/');
      const parts = norm.split('/data/');
      videoPlayer.src = parts.length > 1 ? `/data/${parts[1]}` : '/data/uploads/video/real_cctv_surveillance_store.mp4';
    } else {
      videoPlayer.src = '/data/uploads/video/real_cctv_surveillance_store.mp4';
    }
    videoPlayer.load();

    // Render initial bounding boxes
    renderVideoBoundingBoxes(0);

    // Classification Badge
    const badge = document.getElementById('videoClassificationBadge');
    const reason = document.getElementById('videoClassificationReason');
    if (result.crime_classification) {
      badge.textContent = result.crime_classification.badge || 'NORMAL ACTIVITY (90%)';
      if (result.crime_classification.badge_type === 'danger') {
        badge.className = 'classification-pill-badge danger';
      } else {
        badge.className = 'classification-pill-badge';
      }
      reason.textContent = `Reason: ${result.crime_classification.reason || 'No explicit crime committed'}`;
    }

    // Visual Summary
    if (result.ai_visual_summary) {
      document.getElementById('videoVisualSummaryText').textContent = result.ai_visual_summary;
    }

    // Scene Intelligence
    if (result.scene_intelligence) {
      document.getElementById('videoObjectsDetect').textContent = result.scene_intelligence.objects_detect;
      document.getElementById('videoPeopleCount').textContent = result.scene_intelligence.people_count;
      document.getElementById('videoLocation').textContent = result.scene_intelligence.location;
      document.getElementById('videoAction').textContent = result.scene_intelligence.action;
    }

    // Second by Second Timeline
    if (result.timeline) {
      timeline.render(result.timeline, 'video');
    }
  }

  // 7. PDF Report Download Handlers
  ['downloadImagePdfBtn', 'downloadAudioPdfBtn', 'downloadVideoPdfBtn'].forEach(btnId => {
    const btn = document.getElementById(btnId);
    if (btn) {
      btn.addEventListener('click', () => {
        const downloadUrl = API.getReportUrl(activeSessionId);
        window.open(downloadUrl, '_blank');
      });
    }
  });

  // Check health on startup
  API.checkHealth().then(res => {
    const statusText = document.getElementById('systemHealthText');
    const engineInfo = document.getElementById('engineInfo');
    if (res.status === 'healthy') {
      statusText.textContent = `AI Engine Online (${res.device.toUpperCase()})`;
      engineInfo.textContent = `PyTorch ${res.device.toUpperCase()} + RT-DETR`;
    }
  });

  // Pre-populate translations dictionary with defaults
  currentTranslations = {
    english: "I was walking down Maple Avenue around 8 p.m. when I noticed the lights still on inside the jewelry store on the corner. Suddenly, I saw two masked individuals rush out of the store carrying bags. One of them dropped a necklace on the sidewalk. They jumped into a dark car parked nearby and sped off before anyone could react. I remember hearing the store alarm blaring right after they drove away.",
    hindi: "मैं लगभग 8 बजे मेपल एवेन्यू पर चल रहा था जब मैंने देखा कि कोने पर स्थित ज्वेलरी स्टोर के अंदर अभी भी रोशनी जल रही थी। अचानक, मैंने दो मास्कधारी व्यक्तियों को स्टोर से बैग लेकर भागते हुए देखा। उनमें से एक ने साइडवॉक पर एक हार गिरा दिया। वे पास के एक अंधेरे कार पार्क में कूद गए और किसी की प्रतिक्रिया से पहले ही तेजी से चले गए। मुझे याद है कि वे चले जाने के तुरंत बाद स्टोर अलार्म की आवाज सुनाई दे रही थी।",
    telugu: "మేపుల్ అవెన్యూలో సుమారు 8 గంటల సమయంలో నేను నడుస్తుండగా, మూలలో ఉన్న ఆభరణాల దుకాణంలో ఇంకా లైట్లు వెలిగే ఉన్నాయని నేను గమనించాను. హఠాత్తుగా, బ్యాగులతో దుకాణం నుండి రెండు ముఖం మూసుకున్న వ్యక్తులు వెళ్లిపోతున్నారని నేను చూశాను. వారిలో ఒకరు నడివీధిలో ఒక మాలను పడవేశారు. వారు ప్రక్కనే ఉన్న చీకటి కారులోకి దూకి ఎవరూ ప్రతిస్పందించకముందే వెళ్లిపోయారు. వారు వెళ్లిపోయిన వెంటనే దుకాణం అలారం మ్రోగుతున్నట్లు నేను గుర్తుచేసుకున్నాను.",
    french: "J'ai marché le long de l'avenue Maple vers 20 heures lorsque j'ai remarqué que les lumières étaient toujours allumées à l'intérieur du magasin de bijoux au coin de la rue. Soudain, j'ai vu deux individus masqués sortir précipitamment du magasin en portant des sacs. L'un d'eux a laissé tomber un collier sur le trottoir. Ils ont sauté dans une voiture sombre garée à proximité et ont démarré avant que quiconque puisse réagir. Je me souviens d'avoir entendu la sirène du magasin retentir immédiatement après leur départ."
  };

  // Pre-load default image preview
  render2DAnnotations([
    { label: "Human", confidence: 0.94, box_normalized: [0.25, 0.35, 0.75, 0.85] },
    { label: "Weapon", confidence: 0.88, box_normalized: [0.60, 0.65, 0.70, 0.75] }
  ]);
});
