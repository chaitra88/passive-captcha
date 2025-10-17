// bot_generator/generate_simple_bot.js

const puppeteer = require('puppeteer');

async function runSimpleBot() {
    console.log("🚀 Launching simple bot...");
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    await page.goto('http://localhost:8000');

    console.log("📝 Filling out the form robotically...");

    await page.type('#username', 'simple_bot_user', { delay: 0 });
    await page.type('#password', 'RobotPass123!', { delay: 0 });

    await page.click('button[type="submit"]');

    console.log("✅ Form submitted. Waiting for data to be sent...");

    // This is the corrected line
    await new Promise(r => setTimeout(r, 2000));

    await browser.close();

    console.log("🏁 Simple bot finished.");
}

runSimpleBot();