document.addEventListener('DOMContentLoaded', () => {
    // API base URL - assuming page is served from same host
    const apiBase = '';

    // Elements
    const captureBtn = document.getElementById('captureBtn');
    const countdownEl = document.getElementById('countdown');
    const modeBtns = document.querySelectorAll('.mode-options .opt-btn');
    const filterBtns = document.querySelectorAll('.filter-options .opt-btn');
    const galleryTimeline = document.getElementById('galleryTimeline');
    const photoModal = document.getElementById('photoModal');
    const modalImage = document.getElementById('modalImage');
    const closeBtn = document.querySelector('.close-btn');
    const printBtn = document.getElementById('printBtn');
    const printIndicator = document.getElementById('printIndicator');

    let currentMode = 'SINGLE';
    let currentFilter = 'NONE';
    let currentModalFile = '';

    // Set up listeners for mode and filter options
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.dataset.mode;
            updateMode(currentMode);
        });
    });

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            updateFilter(currentFilter);
        });
    });

    captureBtn.addEventListener('click', startCapture);
    closeBtn.addEventListener('click', closeModal);
    printBtn.addEventListener('click', triggerPrint);

    // API calls
    async function updateMode(mode) {
        try {
            await fetch(`${apiBase}/api/set_mode`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mode })
            });
        } catch (e) {
            console.error("Failed to set mode", e);
        }
    }

    async function updateFilter(filter) {
        try {
            await fetch(`${apiBase}/api/set_filter`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filter })
            });
        } catch (e) {
            console.error("Failed to set filter", e);
        }
    }

    function startCapture() {
        captureBtn.disabled = true;
        let count = 3;
        countdownEl.innerText = count;
        countdownEl.classList.remove('hidden');

        // Countdown animation
        const timer = setInterval(() => {
            count--;
            if (count > 0) {
                countdownEl.innerText = count;
            } else if (count === 0) {
                countdownEl.innerText = '📸';
                // Screen flash effect
                const flash = document.createElement('div');
                flash.style.position = 'fixed';
                flash.style.top = '0'; flash.style.left = '0';
                flash.style.width = '100vw'; flash.style.height = '100vh';
                flash.style.backgroundColor = 'white';
                flash.style.zIndex = '9999';
                document.body.appendChild(flash);
                setTimeout(() => flash.remove(), 100);
            } else {
                clearInterval(timer);
                countdownEl.classList.add('hidden');
                executeCapture();
            }
        }, 1000);
    }

    async function executeCapture() {
        try {
            captureBtn.innerHTML = 'PROCESSING...';
            const res = await fetch(`${apiBase}/api/capture`, { method: 'POST' });
            const data = await res.json();

            if (data.status === 'success' && data.images.length > 0) {
                // Add new photos to gallery
                data.images.forEach(filename => {
                    addGalleryItem(filename);
                });
                // Auto-open the latest photo
                openModal(data.images[data.images.length - 1]);
            }
        } catch (e) {
            console.error("Capture failed", e);
            alert("Capture failed! Backend might be down.");
        } finally {
            captureBtn.disabled = false;
            captureBtn.innerHTML = '📸 CAPTURE';
        }
    }

    function addGalleryItem(filename) {
        const item = document.createElement('div');
        item.className = 'timeline-item';

        const img = document.createElement('img');
        img.src = `${apiBase}/photos/${filename}`;

        item.appendChild(img);

        // Add to top of timeline
        galleryTimeline.insertBefore(item, galleryTimeline.firstChild);

        // Setup observer for scroll animation
        observer.observe(item);

        item.addEventListener('click', () => {
            openModal(filename);
        });

        // Trigger reflow & show
        setTimeout(() => item.classList.add('show'), 50);
    }

    function openModal(filename) {
        currentModalFile = filename;
        modalImage.src = `${apiBase}/photos/${filename}`;
        photoModal.classList.remove('hidden');
        printIndicator.classList.add('hidden');
        printBtn.style.display = 'block';
    }

    function closeModal() {
        photoModal.classList.add('hidden');
        modalImage.src = '';
    }

    async function triggerPrint() {
        if (!currentModalFile) return;

        printBtn.style.display = 'none';
        printIndicator.classList.remove('hidden');

        try {
            await fetch(`${apiBase}/api/print`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: currentModalFile })
            });
            printIndicator.innerText = "PRINT JOB SUBMITTED!";
            setTimeout(() => {
                closeModal();
                printIndicator.innerText = "SENDING TO PRINTER...";
            }, 2000);

        } catch (e) {
            console.error("Print failed", e);
            printIndicator.innerText = "PRINT FAILED!";
            setTimeout(() => printBtn.style.display = 'block', 2000);
        }
    }

    // Scroll Observer for Timeline animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            } else {
                // reverse animation on scroll back up
                entry.target.classList.remove('show');
            }
        });
    }, { threshold: 0.2 });

    // Initialize observer on existing items (if any are loaded via backend)
    document.querySelectorAll('.timeline-item').forEach(item => {
        observer.observe(item);
    });
});
