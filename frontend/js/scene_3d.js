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

window.Scene3D = Scene3D;
