const puppeteer = require('puppeteer');

// Helper function to simulate jagged, linear mouse movement
async function moveMouseLikeIntermediateBot(page, targetElement) {
    const targetBox = await targetElement.boundingBox();
    const startX = Math.random() * 50;
    const startY = Math.random() * 50;
    const endX = targetBox.x + targetBox.width / 2;
    const endY = targetBox.y + targetBox.height / 2;

    const steps = 20;
    for (let i = 1; i <= steps; i++) {
        const progress = i / steps;
        let x = startX + (endX - startX) * progress;
        let y = startY + (endY - startY) * progress;

        if (i < steps) { // Add jitter
            x += (Math.random() - 0.5) * 10;
            y += (Math.random() - 0.5) * 10;
        }

        await page.mouse.move(x, y);
        await new Promise(r => setTimeout(r, 15)); // Use the new timeout method
    }
}

async function runIntermediateBot() {
    const browser = await puppeteer.launch({ headless: true }); // Run headless for speed
    const page = await browser.newPage();
    await page.goto('http://localhost:8000');

    const usernameInput = await page.$('#username');
    const passwordInput = await page.$('#password');
    const submitButton = await page.$('button[type="submit"]');

    await moveMouseLikeIntermediateBot(page, usernameInput);
    await usernameInput.click();
    await usernameInput.type('intermediate_bot_456', { delay: 50 }); // Fixed 50ms delay

    await moveMouseLikeIntermediateBot(page, passwordInput);
    await passwordInput.click();
    await passwordInput.type('SlightlyBetterPass789', { delay: Math.random() * 60 + 20 });

    await moveMouseLikeIntermediateBot(page, submitButton);
    await submitButton.click();

    await new Promise(r => setTimeout(r, 2000));
    await browser.close();
}

// --- Loop to generate many sessions ---
(async () => {
    const SESSIONS_TO_GENERATE = 60;
    console.log(`🚀 Starting to generate ${SESSIONS_TO_GENERATE} intermediate bot sessions...`);
    for (let i = 0; i < SESSIONS_TO_GENERATE; i++) {
        try {
            await runIntermediateBot();
            console.log(`✅ Completed session ${i + 1}/${SESSIONS_TO_GENERATE}`);
        } catch (error) {
            console.error(`❌ Failed session ${i + 1}:`, error);
        }
    }
    console.log("🏁 All intermediate bot sessions generated.");
})();