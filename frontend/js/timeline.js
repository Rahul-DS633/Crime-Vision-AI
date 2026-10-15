/**
 * CrimeVision AI - Timeline Renderer
 * Handles interactive second-by-second video event snapping and audio transcript timelines
 */
class Timeline {
  constructor() {
    this.audioBody = document.getElementById('audioTimelineBody');
    this.videoBody = document.getElementById('videoTimelineBody');
    this.videoPlayer = document.getElementById('surveillanceVideoPlayer');
    this.setupListeners();
  }

  setupListeners() {
    // When clicking any timeline item, seek video to that timestamp
    if (this.videoBody) {
      this.videoBody.addEventListener('click', (e) => {
        const row = e.target.closest('tr');
        if (row && row.dataset.sec !== undefined && this.videoPlayer) {
          const sec = parseFloat(row.dataset.sec);
          this.videoPlayer.currentTime = sec;
          this.videoPlayer.play().catch(() => {});
          
          // Highlight active row
          document.querySelectorAll('#videoTimelineBody tr').forEach(r => r.classList.remove('active-row'));
          row.classList.add('active-row');
        }
      });
    }

    // Auto-highlight timeline row as video plays
    if (this.videoPlayer) {
      this.videoPlayer.addEventListener('timeupdate', () => {
        const currentSec = Math.floor(this.videoPlayer.currentTime);
        const rows = document.querySelectorAll('#videoTimelineBody tr');
        rows.forEach(r => {
          if (parseInt(r.dataset.sec) === currentSec) {
            r.classList.add('active-row');
          } else {
            r.classList.remove('active-row');
          }
        });

        // Update duration tag
        const durTag = document.getElementById('videoDurationTag');
        if (durTag) {
          const curM = Math.floor(this.videoPlayer.currentTime / 60);
          const curS = Math.floor(this.videoPlayer.currentTime % 60);
          const totM = Math.floor((this.videoPlayer.duration || 15) / 60);
          const totS = Math.floor((this.videoPlayer.duration || 15) % 60);
          durTag.textContent = `${curM}:${curS.toString().padStart(2, '0')} / ${totM}:${totS.toString().padStart(2, '0')}`;
        }
      });
    }
  }

  render(timelineItems, mode = 'video') {
    if (!timelineItems || !Array.isArray(timelineItems)) return;

    if (mode === 'video' && this.videoBody) {
      this.videoBody.innerHTML = '';
      timelineItems.forEach(item => {
        const tr = document.createElement('tr');
        const sec = item.seconds !== undefined ? item.seconds : (item.second || 0);
        tr.dataset.sec = sec;
        tr.innerHTML = `
          <td class="time-col">${item.time || '00:00'}</td>
          <td>${item.event || 'Activity detected'}</td>
        `;
        this.videoBody.appendChild(tr);
      });
    } else if (mode === 'audio' && this.audioBody) {
      this.audioBody.innerHTML = '';
      timelineItems.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="time-col">${item.time || '00:00'}</td>
          <td>${item.event || 'Statement recorded'}</td>
        `;
        this.audioBody.appendChild(tr);
      });
    }
  }
}

window.Timeline = Timeline;
