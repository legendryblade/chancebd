import asyncio
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8836"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            args=["--no-sandbox"],
        )
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))

        await page.goto(BASE, wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.screenshot(path="E:/chancebd/verify-01-profile.png", full_page=True)
        print("1. Profile page screenshot taken")
        print("   Header:", await page.text_content(".logo-text"))
        print("   Badge:", await page.text_content(".header-badge"))

        # Change name and GPAs only (defaults are valid)
        await page.fill('input[value="Rahim Ahmed"]', "Tanvir Islam")
        await page.fill('input[type="number"] >> nth=0', "4.75")
        await page.fill('input[type="number"] >> nth=2', "4.9")

        await page.click('button:has-text("Run Investigation Agent")')
        await page.wait_for_timeout(1800)
        await page.screenshot(path="E:/chancebd/verify-02-matches.png", full_page=True)
        print("2. Matches page screenshot taken")
        cards = await page.query_selector_all(".match-card")
        print("   Match cards:", len(cards))
        stats = await page.query_selector_all(".stat-value")
        print("   Stats:", [await s.text_content() for s in stats])
        first_title = await page.text_content(".match-title >> nth=0")
        print("   Top match:", first_title)

        # Timeline
        await page.click('button:has-text("View Timeline")')
        await page.wait_for_timeout(700)
        await page.screenshot(path="E:/chancebd/verify-03-timeline.png", full_page=True)
        print("3. Timeline page screenshot taken")
        items = await page.query_selector_all(".timeline-item")
        print("   Timeline items:", len(items))
        badges = await page.query_selector_all(".timeline-item .badge")
        print("   Statuses:", [await b.text_content() for b in badges])

        # Drafts via step tab
        await page.click('.step:has-text("Draft")')
        await page.wait_for_timeout(700)
        await page.screenshot(path="E:/chancebd/verify-04-drafts.png", full_page=True)
        print("4. Drafts page screenshot taken")
        draft = await page.query_selector(".draft-box")
        text = await draft.text_content() if draft else ""
        print("   Draft length:", len(text))
        print("   Draft has header:", "APPLICATION DRAFT" in text)
        print("   Draft has name:", "Tanvir Islam" in text)

        print("\nConsole errors:", len(errors))
        for e in errors[:5]:
            print("  -", e[:150])

        await browser.close()
        print("\nVERIFICATION COMPLETE")


asyncio.run(main())
