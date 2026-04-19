document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const toggleMonitorBtn = document.getElementById('toggle-monitor');
    const monitorText = document.getElementById('monitor-text');
    const videoFeed = document.getElementById('video-feed');
    const cameraPlaceholder = document.getElementById('camera-placeholder');
    const statRegistered = document.getElementById('stat-registered');
    const statToday = document.getElementById('stat-today');
    const attendanceBody = document.getElementById('attendance-body');
    
    // Modal Elements
    const modal = document.getElementById('register-modal');
    const openRegisterBtn = document.getElementById('open-register');
    const closeBtn = document.querySelector('.close-btn');
    const registerForm = document.getElementById('register-form');
    const regStatus = document.getElementById('reg-status');
    const regSubmitBtn = document.getElementById('reg-submit-btn');

    let isMonitoring = false;
    let pollInterval = null;

    // Toggle Monitoring
    toggleMonitorBtn.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/toggle_monitoring', { method: 'POST' });
            const data = await res.json();
            isMonitoring = data.active;
            
            if (isMonitoring) {
                monitorText.textContent = 'Stop Attendance';
                toggleMonitorBtn.classList.add('btn-danger', 'active');
                toggleMonitorBtn.classList.remove('primary-btn');
                
                // Show video stream
                videoFeed.src = '/video_feed?' + new Date().getTime(); // cache bust
                videoFeed.style.display = 'block';
                cameraPlaceholder.style.display = 'none';
            } else {
                monitorText.textContent = 'Start Attendance';
                toggleMonitorBtn.classList.remove('btn-danger', 'active');
                toggleMonitorBtn.classList.add('primary-btn');
                
                // Hide video stream
                videoFeed.src = '';
                videoFeed.style.display = 'none';
                cameraPlaceholder.style.display = 'block';
            }
        } catch (error) {
            console.error('Error toggling monitor:', error);
        }
    });

    // Update Dashboard Data
    async function updateDashboard() {
        try {
            // Stats
            const statsRes = await fetch('/api/stats');
            const stats = await statsRes.json();
            statRegistered.textContent = stats.registered;
            statToday.textContent = stats.today;

            // Attendance Table
            const attRes = await fetch('/api/attendance');
            const records = await attRes.json();
            
            // Only update if count changed to prevent flicker, 
            // or we could do a smart DOM diff. For simplicity:
            if (attendanceBody.children.length !== records.length) {
                attendanceBody.innerHTML = '';
                records.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${r.check_in_time}</td>
                        <td>${r.user_id}</td>
                        <td><strong>${r.name}</strong></td>
                    `;
                    attendanceBody.appendChild(tr);
                });
            }
        } catch (error) {
            console.error('Error updating dashboard:', error);
        }
    }

    // Polling every 2 seconds
    updateDashboard();
    pollInterval = setInterval(updateDashboard, 2000);

    // Modal Logic
    openRegisterBtn.addEventListener('click', () => {
        modal.classList.add('show');
        regStatus.textContent = '';
        regStatus.className = 'status-msg';
        registerForm.reset();
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.remove('show');
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });

    // Handle Registration
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const userId = document.getElementById('reg-id').value;
        const name = document.getElementById('reg-name').value;
        
        regStatus.textContent = 'Registering... Please look at the camera.';
        regStatus.className = 'status-msg';
        regSubmitBtn.disabled = true;

        try {
            const res = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, name: name })
            });
            const data = await res.json();
            
            if (data.success) {
                regStatus.textContent = 'User registered successfully!';
                regStatus.className = 'status-msg status-success';
                setTimeout(() => modal.classList.remove('show'), 2000);
                updateDashboard();
            } else {
                regStatus.textContent = 'Error: ' + data.message;
                regStatus.className = 'status-msg status-error';
            }
        } catch (error) {
            regStatus.textContent = 'Server error during registration.';
            regStatus.className = 'status-msg status-error';
        } finally {
            regSubmitBtn.disabled = false;
        }
    });
});
