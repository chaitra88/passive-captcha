// frontend/tracker.js

(function () {
    // Configuration
    const API_ENDPOINT = 'http://127.0.0.1:5000/collect';
    const form = document.getElementById('myForm');

    if (!form) {
        return; // Exit if the form isn't on the page
    }

    // Data storage object
    let behavioralData = {
        mouse_moves: [],
        clicks: [],
        keystrokes: [],
        timestamps: {
            start: Date.now(),
            end: null
        }
    };

    // --- Event Listeners to Capture Data ---

    // 1. Capture Mouse Movements (throttled for performance)
    let lastMove = 0;
    document.addEventListener('mousemove', (e) => {
        let now = Date.now();
        if (now - lastMove > 20) { // Capture every 20ms
            behavioralData.mouse_moves.push({
                x: e.clientX,
                y: e.clientY,
                t: now - behavioralData.timestamps.start // time since start
            });
            lastMove = now;
        }
    });

    // 2. Capture Clicks
    document.addEventListener('click', (e) => {
        behavioralData.clicks.push({
            x: e.clientX,
            y: e.clientY,
            target: e.target.tagName,
            t: Date.now() - behavioralData.timestamps.start
        });
    });

    // 3. Capture Keystrokes on the form
    form.addEventListener('keydown', (e) => {
        behavioralData.keystrokes.push({
            key: e.key,
            t: Date.now() - behavioralData.timestamps.start
        });
    });


    // --- Intercept Form Submission to Send Data ---

    form.addEventListener('submit', async (e) => {
        // Prevent the form from submitting the traditional way
        e.preventDefault();

        // Record the end timestamp
        behavioralData.timestamps.end = Date.now();

        console.log("Submitting behavioral data...", behavioralData);

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(behavioralData),
            });

            const result = await response.json();
            console.log('Server response:', result);

            // For now, show an alert. Later we'll use the response to decide what to do.
            alert("Data collected! Check your Flask terminal.");

        } catch (error) {
            console.error('Error sending data:', error);
            alert("Failed to send data. See console for errors.");
        }
    });
})();