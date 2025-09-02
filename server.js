// server.js
const express = require("express");
const { remote } = require("webdriverio");

let browser = null;

const app = express();
app.use(express.json());

app.post("/open", async (req, res) => {
  if (browser) {
    return res.send("Browser already open");
  }
  browser = await remote({
    capabilities: { browserName: "chrome" },
    logLevel: "error",
  });
  res.send("Browser opened");
});

app.post("/navigate", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const { url } = req.body;
  if (!url) return res.status(400).send("No URL provided");
  await browser.url(url);
  res.send(`Navigated to ${url}`);
});

app.post("/click", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const { selector } = req.body;
  if (!selector) return res.status(400).send("No selector provided");
  const elem = await browser.$(selector);
  await elem.click();
  res.send(`Clicked ${selector}`);
});

app.post("/set-value", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const { selector, value } = req.body;
  if (!selector || value === undefined)
    return res.status(400).send("Selector and value required");
  const elem = await browser.$(selector);
  await elem.setValue(value);
  res.send(`Set value for ${selector}`);
});

app.post("/source", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const source = await browser.getPageSource();
  res.send(source);
});

// Wait for element to be displayed
app.post("/wait-for-displayed", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const { selector, timeout } = req.body;
  if (!selector) return res.status(400).send("No selector provided");
  try {
    const elem = await browser.$(selector);
    await elem.waitForDisplayed({ timeout: timeout || 5000 });
    res.send(`Element ${selector} is displayed`);
  } catch (e) {
    res.status(500).send(`Error waiting for displayed: ${e}`);
  }
});

// Wait for element to be enabled
app.post("/wait-for-enabled", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const { selector, timeout } = req.body;
  if (!selector) return res.status(400).send("No selector provided");
  try {
    const elem = await browser.$(selector);
    await elem.waitForEnabled({ timeout: timeout || 5000 });
    res.send(`Element ${selector} is enabled`);
  } catch (e) {
    res.status(500).send(`Error waiting for enabled: ${e}`);
  }
});

// Scroll to element
app.post("/scroll-to", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const { selector } = req.body;
  if (!selector) return res.status(400).send("No selector provided");
  try {
    const elem = await browser.$(selector);
    await elem.scrollIntoView();
    res.send(`Scrolled to ${selector}`);
  } catch (e) {
    res.status(500).send(`Error scrolling to element: ${e}`);
  }
});

// Get text of element
app.post("/get-text", async (req, res) => {
  if (!browser) return res.status(400).send("Browser not open");
  const { selector } = req.body;
  if (!selector) return res.status(400).send("No selector provided");
  try {
    const elem = await browser.$(selector);
    const text = await elem.getText();
    res.send(text);
  } catch (e) {
    res.status(500).send(`Error getting text: ${e}`);
  }
});

app.post("/close", async (req, res) => {
  if (browser) {
    await browser.deleteSession();
    browser = null;
    res.send("Browser closed");
  } else {
    res.send("No browser to close");
  }
});

// Reset browser session for a fresh start (no cookies, no session data)
app.post("/reset", async (req, res) => {
  if (browser) {
    try {
      await browser.deleteSession();
    } catch (e) {
      // ignore errors on deleteSession
    }
    browser = null;
  }
  // Start a new browser session
  browser = await remote({
    capabilities: { browserName: "chrome" },
    logLevel: "error",
    // Add more WebdriverIO config as needed
  });
  res.send("Browser reset and started fresh");
});

app.listen(3000, () => console.log("WebdriverIO server running on port 3000"));
