// frontend/tracker.js

(function () {
    // --- 1. Point to the new /predict endpoint ---
    const API_ENDPOINT = 'http://127.0.0.1:5000/predict';
    const form = document.getElementById('myForm');

    if (!form) return;

    let behavioralData = {
        mouse_moves: [],
        clicks: [],
        keystrokes: [],
        timestamps: {
            start: Date.now(),
            end: null
        }
    };

    // --- All the event listeners are the same ---
    let lastMove = 0;
    document.addEventListener('mousemove', (e) => {
        let now = Date.now();
        if (now - lastMove > 20) {
            behavioralData.mouse_moves.push({
                x: e.clientX,
                y: e.clientY,
                t: now - behavioralData.timestamps.start
            });
            lastMove = now;
        }
    });

    document.addEventListener('click', (e) => {
        behavioralData.clicks.push({
            x: e.clientX,
            y: e.clientY,
            target: e.target.tagName,
            t: Date.now() - behavioralData.timestamps.start
        });
    });

    form.addEventListener('keydown', (e) => {
        behavioralData.keystrokes.push({
            key: e.key,
            t: Date.now() - behavioralData.timestamps.start
        });
    });

    // --- 2. Update the submit handler logic ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Always prevent default
        behavioralData.timestamps.end = Date.now();

        console.log("Submitting data to /predict...");

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(behavioralData),
            });

            const result = await response.json();
            console.log('Server response:', result);

            // --- 3. Act on the server's decision ---
            if (result.decision === 'allow') {
                // If human, allow the form to submit
                alert('Verification successful. Submitting form.');
                form.submit(); // This submits the form for real
            } else {
                // If bot, block the submission
                alert('Verification failed. Please try again.');
                // We just do nothing, blocking the submission.
            }

        } catch (error) {
            console.error('Error sending data:', error);
            // In case of error, you might want to block or allow
            alert("Error during verification. Please try again.");
        }
    });
})();