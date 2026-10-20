/**
 * CrimeVision AI - 3D Scene Reconstruction with Three.js
 * Visualizes crime scenes in full 3D with interactive object bounding meshes,
 * forensic markers, and orbit camera controls.
 */
class Scene3D {
  constructor(containerId = 'threejsViewport') {
    this.container = document.getElementById(containerId);
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.evidenceGroup = null;
    this.animationId = null;

    if (this.container && typeof THREE !== 'undefined') {
      this.init();
    }
  }

  init() {
    const width = this.container.clientWidth || 600;
    const height = this.container.clientHeight || 480;

    // 1. Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x070b14);
    this.scene.fog = new THREE.FogExp2(0x070b14, 0.04);

    // 2. Camera
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    this.camera.position.set(0, 5, 8);

    // 3. Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.container.innerHTML = '';
    this.container.appendChild(this.renderer.domElement);

    // 4. Controls
    if (typeof THREE.OrbitControls !== 'undefined') {
      this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.maxPolarAngle = Math.PI / 2 + 0.1;
      this.controls.minDistance = 2;
      this.controls.maxDistance = 25;
    }

    // 5. Lighting
    this.setupLighting();

    // 6. Forensic Room & Grid
    this.setupRoom();

    // 7. Group for detected evidence items
    this.evidenceGroup = new THREE.Group();
    this.scene.add(this.evidenceGroup);

    // Load default scene objects
    this.buildDefaultCrimeScene();

    // Resize handler
    window.addEventListener('resize', () => this.onResize());

    // Animation Loop
    this.animate();
  }

  setupLighting() {
    const ambientLight = new THREE.AmbientLight(0x94a3b8, 0.6);
    this.scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(5, 12, 7);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    this.scene.add(dirLight);

    const forensicSpot = new THREE.PointLight(0x38bdf8, 1.2, 15);
    forensicSpot.position.set(0, 4, 0);
    this.scene.add(forensicSpot);
  }

  setupRoom() {
    // Floor Grid
    const gridHelper = new THREE.GridHelper(14, 14, 0x3b82f6, 0x1e293b);
    gridHelper.position.y = 0.01;
    this.scene.add(gridHelper);

    // Room Floor Plane
    const floorGeo = new THREE.PlaneGeometry(14, 14);
    const floorMat = new THREE.MeshStandardMaterial({
      color: 0x0f172a,
      roughness: 0.8,
      metalness: 0.2
    });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    this.scene.add(floor);

    // Back Wall
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.9 });
    const backWallGeo = new THREE.PlaneGeometry(14, 6);
    const backWall = new THREE.Mesh(backWallGeo, wallMat);
    backWall.position.set(0, 3, -7);
    this.scene.add(backWall);

    // Left Wall
    const leftWall = new THREE.Mesh(backWallGeo, wallMat);
    leftWall.rotation.y = Math.PI / 2;
    leftWall.position.set(-7, 3, 0);
    this.scene.add(leftWall);
  }

  buildDefaultCrimeScene() {
    this.clearEvidence();

    // 1. Human (Victim on the floor)
    const victimGroup = new THREE.Group();
    // Torso (blue shirt)
    const torsoGeo = new THREE.BoxGeometry(0.8, 0.3, 1.4);
    const torsoMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.5 });
    const torso = new THREE.Mesh(torsoGeo, torsoMat);
    torso.position.set(0, 0.15, 0);
    torso.castShadow = true;
    victimGroup.add(torso);

    // Head
    const headGeo = new THREE.SphereGeometry(0.22, 16, 16);
    const headMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, roughness: 0.4 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.set(0, 0.18, -0.9);
    victimGroup.add(head);

    // Legs (jeans)
    const legGeo = new THREE.BoxGeometry(0.35, 0.25, 1.2);
    const legMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a });
    const leftLeg = new THREE.Mesh(legGeo, legMat);
    leftLeg.position.set(-0.25, 0.12, 1.2);
    const rightLeg = new THREE.Mesh(legGeo, legMat);
    rightLeg.position.set(0.25, 0.12, 1.2);
    victimGroup.add(leftLeg);
    victimGroup.add(rightLeg);

    // 3D Bounding Wireframe around Human
    const bboxHuman = new THREE.BoxHelper(victimGroup, 0x10b981);
    victimGroup.add(bboxHuman);
    this.evidenceGroup.add(victimGroup);

    // 2. Weapon (Knife)
    const knifeGroup = new THREE.Group();
    // Blade
    const bladeGeo = new THREE.BoxGeometry(0.06, 0.02, 0.35);
    const bladeMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.1 });
    const blade = new THREE.Mesh(bladeGeo, bladeMat);
    blade.position.set(1.2, 0.02, -0.2);
    knifeGroup.add(blade);
    // Handle
    const handleGeo = new THREE.BoxGeometry(0.08, 0.04, 0.15);
    const handleMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
    const handle = new THREE.Mesh(handleGeo, handleMat);
    handle.position.set(1.2, 0.02, 0.05);
    knifeGroup.add(handle);

    // Knife Bounding Marker (Red)
    const bboxKnife = new THREE.BoxHelper(knifeGroup, 0xef4444);
    knifeGroup.add(bboxKnife);
    this.evidenceGroup.add(knifeGroup);

    // 3. Desk / Diningtable
    const deskGeo = new THREE.BoxGeometry(2.4, 1.2, 1.2);
    const deskMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.7 });
    const desk = new THREE.Mesh(deskGeo, deskMat);
    desk.position.set(2.8, 0.6, -2.5);
    desk.castShadow = true;
    const bboxDesk = new THREE.BoxHelper(desk, 0x3b82f6);
    this.evidenceGroup.add(desk);
    this.evidenceGroup.add(bboxDesk);

    // 4. Laptop on Desk
    const laptopGeo = new THREE.BoxGeometry(0.5, 0.04, 0.35);
    const laptopMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.8 });
    const laptop = new THREE.Mesh(laptopGeo, laptopMat);
    laptop.position.set(2.6, 1.22, -2.4);
    this.evidenceGroup.add(laptop);

    // 5. Office Chair
    const chairGeo = new THREE.BoxGeometry(0.8, 1.4, 0.8);
    const chairMat = new THREE.MeshStandardMaterial({ color: 0x334155 });
    const chair = new THREE.Mesh(chairGeo, chairMat);
    chair.position.set(-2.5, 0.7, -2.5);
    chair.castShadow = true;
    const bboxChair = new THREE.BoxHelper(chair, 0x3b82f6);
    this.evidenceGroup.add(chair);
    this.evidenceGroup.add(bboxChair);

    // 6. Sofa
    const sofaGeo = new THREE.BoxGeometry(1.2, 1.0, 2.6);
    const sofaMat = new THREE.MeshStandardMaterial({ color: 0x1e293b });
    const sofa = new THREE.Mesh(sofaGeo, sofaMat);
    sofa.position.set(-4.5, 0.5, 0.5);
    sofa.castShadow = true;
    const bboxSofa = new THREE.BoxHelper(sofa, 0x3b82f6);
    this.evidenceGroup.add(sofa);
    this.evidenceGroup.add(bboxSofa);

    // 7. Evidence Tape markers (Yellow ribbons on floor)
    const tapeMat = new THREE.MeshBasicMaterial({ color: 0xfacc15, side: THREE.DoubleSide });
    const tape1Geo = new THREE.PlaneGeometry(3.5, 0.1);
    const tape1 = new THREE.Mesh(tape1Geo, tapeMat);
    tape1.rotation.x = -Math.PI / 2;
    tape1.position.set(0.5, 0.03, -1.0);
    this.evidenceGroup.add(tape1);
  }

  loadSceneData(sceneData) {
    if (!sceneData || !this.evidenceGroup) return;
    this.clearEvidence();

    const objects = sceneData.objects || [];
    if (!objects.length) {
      this.buildDefaultCrimeScene();
      return;
    }

    objects.forEach((obj, idx) => {
      const pos = obj.position_3d || { x: (idx % 3 - 1) * 2, y: 0.5, z: -idx };
      const label = obj.label || "Object";
      
      let color = 0x3b82f6;
      let w = 1.0, h = 1.0, d = 1.0;

      if (label === 'Human') {
        color = 0x10b981;
        w = 0.8; h = 1.6; d = 0.6;
      } else if (label === 'Weapon') {
        color = 0xef4444;
        w = 0.3; h = 0.2; d = 0.5;
      } else if (label === 'laptop') {
        color = 0x06b6d4;
        w = 0.6; h = 0.1; d = 0.4;
      }

      const geo = new THREE.BoxGeometry(w, h, d);
      const mat = new THREE.MeshStandardMaterial({
        color: color,
        roughness: 0.4,
        metalness: 0.2,
        transparent: true,
        opacity: 0.85
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(pos.x, Math.max(h/2, pos.y), pos.z);
      mesh.castShadow = true;

      const helper = new THREE.BoxHelper(mesh, color);
      this.evidenceGroup.add(mesh);
      this.evidenceGroup.add(helper);
    });
  }

  clearEvidence() {
    if (!this.evidenceGroup) return;
    while (this.evidenceGroup.children.length > 0) {
      const child = this.evidenceGroup.children[0];
      this.evidenceGroup.remove(child);
      if (child.geometry) child.geometry.dispose();
      if (child.material) {
        if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
        else child.material.dispose();
      }
    }
  }

  resetCamera() {
    if (this.camera && this.controls) {
      this.camera.position.set(0, 5, 8);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    }
  }

  onResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    if (!width || !height) return;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    this.animationId = requestAnimationFrame(() => this.animate());
    if (this.controls) this.controls.update();
    if (this.renderer && this.scene && this.camera) {
      this.renderer.render(this.scene, this.camera);
    }
  }
}

/**
 * VideoTrajectory3D - Surveillance Camera & 3D Suspect Movement Trajectory
 * Reconstructs 3D motion path, camera frustum, and synchronized video tracking.
 */
class VideoTrajectory3D {
  constructor(containerId = 'videoTrajectoryViewport') {
    this.container = document.getElementById(containerId);
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.animationId = null;

    this.tracksGroup = null;
    this.suspectAvatar = null;
    this.cctvFrustum = null;
    this.cctvCameraMesh = null;
    this.hotspotMesh = null;

    this.trajectoryData = null;
    this.suspectWaypoints = [];
    this.isTrackingSuspect = false;
    this.currentSecond = 0;

    if (this.container && typeof THREE !== 'undefined') {
      this.init();
    }
  }

  init() {
    const width = this.container.clientWidth || 640;
    const height = this.container.clientHeight || 480;

    // 1. Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x060913);
    this.scene.fog = new THREE.FogExp2(0x060913, 0.035);

    // 2. Camera
    this.camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    this.camera.position.set(0, 7.5, 9.5);

    // 3. Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.container.innerHTML = '';
    this.container.appendChild(this.renderer.domElement);

    // 4. Controls
    if (typeof THREE.OrbitControls !== 'undefined') {
      this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.maxPolarAngle = Math.PI / 2 + 0.05;
      this.controls.minDistance = 2;
      this.controls.maxDistance = 35;
      this.controls.target.set(0, 0.5, 0);
    }

    // 5. Lighting
    this.setupLighting();

    // 6. Surveillance Environment & Floor
    this.setupSurveillanceRoom();

    // 7. Virtual CCTV Camera & FOV Frustum
    this.setupVirtualCCTVCamera();

    // 8. Tracks Group
    this.tracksGroup = new THREE.Group();
    this.scene.add(this.tracksGroup);

    // Load default benchmark trajectory
    this.buildDefaultTrajectory();

    // Resize listener
    window.addEventListener('resize', () => this.onResize());

    // Animation Loop
    this.animate();
  }

  setupLighting() {
    const ambient = new THREE.AmbientLight(0x94a3b8, 0.7);
    this.scene.add(ambient);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
    dirLight.position.set(4, 12, 6);
    dirLight.castShadow = true;
    this.scene.add(dirLight);

    // Cyan surveillance spot
    const cctvSpot = new THREE.SpotLight(0x38bdf8, 2.0, 20, Math.PI / 4, 0.4);
    cctvSpot.position.set(0, 5.2, 7.5);
    cctvSpot.target.position.set(0, 0, 0);
    this.scene.add(cctvSpot);
    this.scene.add(cctvSpot.target);
  }

  setupSurveillanceRoom() {
    // Floor Grid
    const grid = new THREE.GridHelper(18, 18, 0x2563eb, 0x1e293b);
    grid.position.y = 0.01;
    this.scene.add(grid);

    // Ground Floor
    const floorGeo = new THREE.PlaneGeometry(18, 18);
    const floorMat = new THREE.MeshStandardMaterial({
      color: 0x090d16,
      roughness: 0.85,
      metalness: 0.15
    });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    this.scene.add(floor);

    // Subtle Boundary Walls
    const wallMat = new THREE.MeshBasicMaterial({
      color: 0x1e293b,
      wireframe: true,
      transparent: true,
      opacity: 0.25
    });
    const backWall = new THREE.Mesh(new THREE.PlaneGeometry(18, 6), wallMat);
    backWall.position.set(0, 3, -9);
    this.scene.add(backWall);

    // Landmark Zones
    this.createLandmark([-3.5, 0, -4.8], 'STORE ENTRANCE', 0x10b981);
    this.createLandmark([-1.8, 0, 0.5], 'AISLE 2 SHELVES', 0x64748b);
    this.createLandmark([3.0, 0, 1.8], 'CHECKOUT REGISTER', 0xf59e0b);

    // Anomaly Danger Hotspot Zone
    const hotspotGeo = new THREE.RingGeometry(0.8, 1.8, 32);
    const hotspotMat = new THREE.MeshBasicMaterial({
      color: 0xef4444,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.35
    });
    this.hotspotMesh = new THREE.Mesh(hotspotGeo, hotspotMat);
    this.hotspotMesh.rotation.x = -Math.PI / 2;
    this.hotspotMesh.position.set(0.2, 0.02, -0.5);
    this.scene.add(this.hotspotMesh);
  }

  createLandmark(pos, text, colorHex) {
    const group = new THREE.Group();
    group.position.set(pos[0], pos[1], pos[2]);

    // Marker base
    const baseGeo = new THREE.CylinderGeometry(0.3, 0.3, 0.05, 16);
    const baseMat = new THREE.MeshStandardMaterial({ color: colorHex });
    const base = new THREE.Mesh(baseGeo, baseMat);
    group.add(base);

    // Marker pin
    const pinGeo = new THREE.CylinderGeometry(0.04, 0.04, 1.2, 8);
    const pinMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8 });
    const pin = new THREE.Mesh(pinGeo, pinMat);
    pin.position.y = 0.6;
    group.add(pin);

    // Pin top sphere
    const topGeo = new THREE.SphereGeometry(0.14, 16, 16);
    const topMat = new THREE.MeshStandardMaterial({ color: colorHex, emissive: colorHex, emissiveIntensity: 0.6 });
    const topSphere = new THREE.Mesh(topGeo, topMat);
    topSphere.position.y = 1.2;
    group.add(topSphere);

    this.scene.add(group);
  }

  setupVirtualCCTVCamera() {
    const camGroup = new THREE.Group();
    camGroup.position.set(0, 5.2, 7.5);

    // Camera body
    const bodyGeo = new THREE.BoxGeometry(0.5, 0.4, 0.9);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.4 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.rotation.x = -0.45;
    camGroup.add(body);

    // Lens
    const lensGeo = new THREE.CylinderGeometry(0.18, 0.18, 0.3, 16);
    const lensMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.1, metalness: 0.9 });
    const lens = new THREE.Mesh(lensGeo, lensMat);
    lens.rotation.x = Math.PI / 2 - 0.45;
    lens.position.set(0, -0.15, -0.5);
    camGroup.add(lens);

    // Blinking REC LED
    const ledGeo = new THREE.SphereGeometry(0.06, 8, 8);
    const ledMat = new THREE.MeshBasicMaterial({ color: 0xef4444 });
    this.recLed = new THREE.Mesh(ledGeo, ledMat);
    this.recLed.position.set(0.18, 0.15, -0.4);
    camGroup.add(this.recLed);

    // CCTV Mount bracket
    const mountGeo = new THREE.CylinderGeometry(0.06, 0.06, 1.2, 8);
    const mountMat = new THREE.MeshStandardMaterial({ color: 0x1e293b });
    const mount = new THREE.Mesh(mountGeo, mountMat);
    mount.position.set(0, 0.6, 0.2);
    camGroup.add(mount);

    // Holographic FOV Frustum Pyramid projecting to ground
    const frustumGeo = new THREE.ConeGeometry(7.5, 9.5, 4, 1, true);
    const frustumMat = new THREE.MeshBasicMaterial({
      color: 0x38bdf8,
      wireframe: true,
      transparent: true,
      opacity: 0.2
    });
    this.cctvFrustum = new THREE.Mesh(frustumGeo, frustumMat);
    this.cctvFrustum.position.set(0, 2.2, 3.8);
    this.cctvFrustum.rotation.x = -Math.PI / 2 - 0.45;
    this.scene.add(this.cctvFrustum);

    this.cctvCameraMesh = camGroup;
    this.scene.add(camGroup);
  }

  buildDefaultTrajectory() {
    const waypoints = [];
    for (let s = 0; s <= 20; s++) {
      const p = s / 20.0;
      waypoints.append ? null : waypoints.push({
        second: s,
        x: -3.2 + 6.2 * p + 0.3 * Math.sin(p * 3.0),
        y: 0.0,
        z: -4.2 + 6.8 * p,
        speed: 0.9 + 0.4 * Math.sin(p * Math.PI),
        action: s < 3 ? 'Entering Scene' : (s < 8 ? 'Scanning Shelves' : (s < 14 ? 'Concealing Object' : 'Exiting')),
        danger_level: s >= 8 && s <= 14 ? 'high' : 'low'
      });
    }
    this.loadTrajectoryData({
      suspect_tracks: [
        { track_id: 1, name: 'Suspect #1', color: '#ef4444', path: waypoints }
      ]
    });
  }

  loadTrajectoryData(data) {
    if (!data) return;
    this.trajectoryData = data;
    this.suspectWaypoints = data.suspect_tracks?.[0]?.path || [];

    // Clear old tracks
    while (this.tracksGroup.children.length > 0) {
      const child = this.tracksGroup.children[0];
      this.tracksGroup.remove(child);
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
    }

    if (this.suspectWaypoints.length < 2) return;

    // 1. Generate 3D Spline Path
    const points = this.suspectWaypoints.map(wp => new THREE.Vector3(wp.x, 0.08, wp.z));
    const curve = new THREE.CatmullRomCurve3(points);
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.06, 8, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xef4444,
      emissive: 0xb91c1c,
      emissiveIntensity: 0.7,
      roughness: 0.3
    });
    const trajectoryTube = new THREE.Mesh(tubeGeo, tubeMat);
    this.tracksGroup.add(trajectoryTube);

    // 2. Add Waypoint nodes at key seconds
    this.suspectWaypoints.forEach((wp, idx) => {
      if (idx % 3 === 0 || idx === this.suspectWaypoints.length - 1) {
        const nodeGeo = new THREE.SphereGeometry(0.12, 12, 12);
        const nodeMat = new THREE.MeshBasicMaterial({
          color: wp.danger_level === 'high' ? 0xef4444 : 0x38bdf8
        });
        const node = new THREE.Mesh(nodeGeo, nodeMat);
        node.position.set(wp.x, 0.08, wp.z);
        this.tracksGroup.add(node);
      }
    });

    // 3. Suspect 3D Avatar (Stylized Forensic Mannequin)
    this.createSuspectAvatar();

    // Reset position to t=0
    this.updatePlaybackTime(0);
  }

  createSuspectAvatar() {
    if (this.suspectAvatar) {
      this.scene.remove(this.suspectAvatar);
    }

    const avatarGroup = new THREE.Group();

    // Pulsing target ring at base
    const ringGeo = new THREE.RingGeometry(0.35, 0.45, 24);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0xef4444,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.8
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.04;
    avatarGroup.add(ring);

    // Body cylinder
    const bodyGeo = new THREE.CylinderGeometry(0.24, 0.28, 1.1, 16);
    const bodyMat = new THREE.MeshStandardMaterial({
      color: 0xdc2626,
      metalness: 0.3,
      roughness: 0.4
    });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.65;
    avatarGroup.add(body);

    // Head sphere
    const headGeo = new THREE.SphereGeometry(0.2, 16, 16);
    const headMat = new THREE.MeshStandardMaterial({
      color: 0xfca5a5,
      metalness: 0.2,
      roughness: 0.5
    });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 1.4;
    avatarGroup.add(head);

    // Forward direction indicator cone
    const dirGeo = new THREE.ConeGeometry(0.14, 0.4, 8);
    const dirMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
    const dirCone = new THREE.Mesh(dirGeo, dirMat);
    dirCone.rotation.x = Math.PI / 2;
    dirCone.position.set(0, 0.65, 0.35);
    avatarGroup.add(dirCone);

    this.suspectAvatar = avatarGroup;
    this.scene.add(this.suspectAvatar);
  }

  updatePlaybackTime(seconds) {
    this.currentSecond = seconds;
    if (!this.suspectWaypoints || this.suspectWaypoints.length === 0 || !this.suspectAvatar) return;

    // Find nearest waypoint or interpolate
    const secFloor = Math.floor(seconds);
    const secCeil = Math.min(secFloor + 1, this.suspectWaypoints.length - 1);
    const t = seconds - secFloor;

    const wp1 = this.suspectWaypoints[Math.min(secFloor, this.suspectWaypoints.length - 1)];
    const wp2 = this.suspectWaypoints[secCeil];

    if (!wp1) return;

    const curX = wp1.x + ((wp2 ? wp2.x : wp1.x) - wp1.x) * t;
    const curZ = wp1.z + ((wp2 ? wp2.z : wp1.z) - wp1.z) * t;

    // Update avatar position
    this.suspectAvatar.position.set(curX, 0, curZ);

    // Face movement direction
    if (wp2 && (wp2.x !== wp1.x || wp2.z !== wp1.z)) {
      const angle = Math.atan2(wp2.x - wp1.x, wp2.z - wp1.z);
      this.suspectAvatar.rotation.y = angle;
    }

    // Telemetry HUD elements update
    const posElem = document.getElementById('telemetryPos');
    const statusElem = document.getElementById('telemetryStatus');
    const speedElem = document.getElementById('telemetrySpeed');
    const distElem = document.getElementById('telemetryDist');

    if (posElem) posElem.textContent = `X: ${curX.toFixed(2)}m, Z: ${curZ.toFixed(2)}m`;
    if (statusElem) statusElem.textContent = wp1.action || 'Tracking active';
    if (speedElem) speedElem.textContent = `${(wp1.speed || 1.1).toFixed(2)} m/s`;
    if (distElem) distElem.textContent = `${(Math.sqrt(curX * curX + curZ * curZ) + 1.2).toFixed(1)} m`;

    // Follow suspect camera mode
    if (this.isTrackingSuspect && this.controls) {
      this.controls.target.set(curX, 0.8, curZ);
      this.camera.position.set(curX, 4.5, curZ + 5.5);
    }
  }

  setCCTVAngle() {
    this.isTrackingSuspect = false;
    if (this.camera && this.controls) {
      this.camera.position.set(0, 5.2, 7.5);
      this.controls.target.set(0, 0.4, 0);
      this.controls.update();
    }
  }

  setTopDownView() {
    this.isTrackingSuspect = false;
    if (this.camera && this.controls) {
      this.camera.position.set(0, 15, 0.01);
      this.controls.target.set(0, 0, 0);
      this.controls.update();
    }
  }

  setOrbitView() {
    this.isTrackingSuspect = false;
    if (this.camera && this.controls) {
      this.camera.position.set(7.5, 7.0, 8.5);
      this.controls.target.set(0, 0.5, 0);
      this.controls.update();
    }
  }

  toggleTrackSuspect() {
    this.isTrackingSuspect = !this.isTrackingSuspect;
    return this.isTrackingSuspect;
  }

  resetCamera() {
    this.isTrackingSuspect = false;
    if (this.camera && this.controls) {
      this.camera.position.set(0, 7.5, 9.5);
      this.controls.target.set(0, 0.5, 0);
      this.controls.update();
    }
  }

  onResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    if (!width || !height) return;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    this.animationId = requestAnimationFrame(() => this.animate());
    
    // Pulse REC LED
    if (this.recLed) {
      this.recLed.material.color.setHex(Date.now() % 1000 > 500 ? 0xef4444 : 0x450a0a);
    }

    // Pulse Hotspot Ring
    if (this.hotspotMesh) {
      this.hotspotMesh.material.opacity = 0.25 + 0.15 * Math.sin(Date.now() * 0.004);
    }

    if (this.controls) this.controls.update();
    if (this.renderer && this.scene && this.camera) {
      this.renderer.render(this.scene, this.camera);
    }
  }
}

window.Scene3D = Scene3D;
window.VideoTrajectory3D = VideoTrajectory3D;

