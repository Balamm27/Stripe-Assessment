"""Build the public review page from prepared V2 assets.

The original PowerPoint, high-resolution recordings, and unredacted PDFs remain
outside this repository.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TITLES = [
    "AI Powered Agent", "What you’ll see in this walkthrough",
    "From analyst queue to guided payment investigations", "How It Works",
    "AI Powered Agent architecture", "Working demo", "Key Features",
    "Impact & Value Proposition", "How the agent investigates the metric gap",
    "Adaptive Auth: the explanation Claude never received",
    "How I fixed the Adaptive Auth retrieval failure",
    "A wrong-year answer changed the prompt and SQL rule",
    "A 1,000-character limit hid the schema the agent needed",
    "Test Coverage Matrix", "Usage and reliability",
    "What I’d bring to Stripe Finance", "Making the architecture reusable",
]
CHAPTERS = [
    "Introduction", "Introduction", "The workflow", "The experience",
    "The build", "Working demo", "The experience", "The value", "The build",
    "What failed", "What changed", "What changed", "What changed",
    "Validation", "Observed usage", "Closing", "Supplementary walkthrough",
]
APPENDIX = [
    "Two skills make setup reusable", "Reuse across Expedia",
    "Analytical scope and example investigations", "Two execution paths",
    "Inside the investigative tool loop", "Controls around the agent",
    "How feedback becomes reusable knowledge", "Reference: a defined calculation",
]
MAIN_DURATIONS = [
    35.284, 26.003, 68.817, 25.517, 128.483, 395.346, 58.409, 67.575,
    78.064, 69.241, 65.375, 50.559, 75.063, 70.641, 37.122, 64.492,
]

def esc(s):
    return html.escape(s, quote=True)

def runtime(seconds):
    return f"{int(seconds // 60)}:{int(round(seconds % 60)):02d}"

def page():
    panels = []
    for i, (title, chapter) in enumerate(zip(TITLES, CHAPTERS), 1):
        theme = "dark" if i in (1, 2, 4, 6, 7, 14, 16, 17) else "light"
        if i in (6, 17):
            src = f"assets/video/slides/{i:02d}.mp4" if i == 6 else "assets/video/supplementary-walkthrough.mp4"
            media = f'<div class="solo-video"><video controls playsinline preload="none" poster="assets/video/slide-{i:02d}-poster.jpg" aria-label="Watch slide {i}: {esc(title)}"><source src="{src}" type="video/mp4">Your browser does not support video. <a href="{src}">Open the recording</a>.</video></div>'
            actions = ""
        else:
            media = f'<figure class="slide-frame"><img src="assets/slides/{i:02d}.png" alt="Slide {i}: {esc(title)}" width="1920" height="1080" {"fetchpriority=high" if i == 1 else "loading=lazy"}></figure>'
            src = f"assets/video/slides/{i:02d}.mp4"
            actions = f'<div class="panel-actions"><button class="expand" type="button" data-slide="{i}" aria-label="View slide {i} full size">View full size <span aria-hidden="true">↗</span></button><details class="slide-recording"><summary>▶ Watch Bala present this slide <span class="runtime">{runtime(MAIN_DURATIONS[i-1])}</span></summary><video controls playsinline preload="none" poster="assets/slides/{i:02d}.png" aria-label="Narrated recording for slide {i}"><source src="{src}" type="video/mp4">Your browser does not support video. <a href="{src}">Open the recording</a>.</video></details></div>'
        panels.append(f'<section id="slide-{i}" class="story-panel {theme}" aria-labelledby="title-{i}"><div class="panel-top"><span class="chapter">{esc(chapter)}</span><span class="count">{i:02d} / 17</span></div><h2 id="title-{i}" class="panel-title">{esc(title)}</h2>{media}{actions}</section>')
    appendix = "".join(
        f'<details class="appendix-item"><summary><span>{i-17:02d}</span>{esc(title)}<span class="plus" aria-hidden="true">+</span></summary><img src="assets/slides/{i:02d}.png" alt="Appendix slide: {esc(title)}" width="1920" height="1080" loading="lazy"></details>'
        for i, title in enumerate(APPENDIX, 18)
    )
    docs = "".join(
        f'<article class="document"><div class="document-heading"><h3>{esc(title)}</h3><a href="assets/documents/{esc(filename)}" target="_blank" rel="noopener">Open PDF ↗</a></div><object data="assets/documents/{esc(filename)}" type="application/pdf" aria-label="{esc(title)} PDF"><p>Your browser cannot display this PDF here. <a href="assets/documents/{esc(filename)}">Open the PDF</a>.</p></object></article>'
        for title, filename in [
            ("Agent UI", "Agent UI - Redacted.pdf"),
            ("Agent UI · PLS sample prompts", "Agent UI - PLS Sample Prompts - Redacted.pdf"),
        ]
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#062657"><meta name="description" content="Bala Manoghar Mathavy’s AI Solutions assessment: narrated walkthroughs, slide-by-slide case study, technical appendix, and sample agent outputs."><meta property="og:title" content="AI Powered Agent · Bala Manoghar Mathavy"><meta property="og:description" content="A narrated walkthrough of an AI agent for payment investigations, its design, demo, failures, fixes, and evidence."><meta property="og:image" content="https://balamm27.github.io/Stripe-Assessment/assets/slides/01.png"><meta property="og:type" content="website"><title>AI Powered Agent | Bala Manoghar Mathavy</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head>
<body><a class="skip" href="#contents">Skip to contents</a><div class="scroll-progress" aria-hidden="true"><span></span></div><header class="site-header"><a class="wordmark" href="#contents">BALA <span>/ AI SOLUTIONS</span></a><nav aria-label="Primary"><a href="#recordings">Full videos</a><a href="#slide-1">Slides</a><a href="#appendix">Appendix</a><a href="#sample-pdfs">Sample PDFs</a></nav><button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false">Menu</button></header>
<main><section id="contents" class="contents-section" aria-labelledby="contents-title"><div class="contents-inner"><span class="eyebrow">Assessment walkthrough · October 2026</span><h1 id="contents-title">An AI agent for guided payment investigations</h1><p class="contents-intro">Watch the narrated assessment, or move through the deck one slide at a time. Each presented slide has its own recording.</p><div class="contents-heading">Contents</div><div class="contents-grid"><a href="#recordings"><span>01</span><strong>Full recordings</strong><small>Main assessment and supplementary walkthrough</small></a><a href="#slide-1"><span>02</span><strong>Slide-by-slide story</strong><small>Workflow, build, demo, lessons, and evidence</small></a><a href="#appendix"><span>03</span><strong>Technical appendix</strong><small>Eight reference slides from the deck</small></a><a href="#sample-pdfs"><span>04</span><strong>Sample agent outputs</strong><small>Two redacted PDF exports</small></a></div><a class="contents-next" href="#recordings">Start with the recordings <span aria-hidden="true">↓</span></a></div></section>
<section id="recordings" class="recordings-section" aria-labelledby="recordings-title"><div class="section-inner wide"><span class="eyebrow">Watch the assessment</span><h2 id="recordings-title">The complete walkthroughs</h2><p class="section-intro">Bala narrates both recordings in his own voice. The individual slide recordings appear below.</p><div class="recordings-grid"><article class="recording-card"><div class="recording-meta"><span>01 · Main assessment</span><span>21:56</span></div><video controls playsinline preload="metadata" poster="assets/slides/01.png" aria-label="Main assessment recording"><source src="assets/video/main-walkthrough.mp4" type="video/mp4">Your browser does not support video. <a href="assets/video/main-walkthrough.mp4">Open the main recording</a>.</video><h3>From workflow to working agent</h3><p>The recurring payment analytics workflow, application demo, design choices, fixes, and observed results.</p></article><article class="recording-card"><div class="recording-meta"><span>02 · Supplementary walkthrough</span><span>3:50</span></div><video controls playsinline preload="metadata" poster="assets/video/slide-17-poster.jpg" aria-label="Supplementary recording"><source src="assets/video/supplementary-walkthrough.mp4" type="video/mp4">Your browser does not support video. <a href="assets/video/supplementary-walkthrough.mp4">Open the supplementary recording</a>.</video><h3>Making the architecture reusable</h3><p>A closer look at the reusable setup and what it enables for other teams.</p></article></div><a class="section-jump" href="#slide-1">Explore the slides <span aria-hidden="true">↓</span></a></div></section>
<div class="slides-intro" id="slides"><span class="eyebrow">The deck, with a recording for each slide</span><h2>Explore the story</h2><p>Scroll through the slides or play Bala’s narration alongside any one of them.</p></div>{''.join(panels)}
<section id="appendix" class="appendix-section" aria-labelledby="appendix-title"><div class="section-inner"><span class="eyebrow">Reference material</span><h2 id="appendix-title">Technical appendix</h2><p class="section-intro">Eight additional slides from the final PowerPoint. Open a topic to view the original slide.</p><div class="appendix-list">{appendix}</div></div></section>
<section id="sample-pdfs" class="documents-section" aria-labelledby="documents-title"><div class="section-inner wide"><span class="eyebrow">Agent output examples</span><h2 id="documents-title">Sample prompts and responses</h2><p class="section-intro">These are the two PDF exports from the agent. Dollar values are masked in these external review copies.</p><div class="document-list">{docs}</div></div></section></main><footer><span>Bala Manoghar Mathavy</span><span>AI Powered Agent · October 2026</span><a href="#contents">Back to top ↑</a></footer><dialog id="slide-dialog" aria-label="Full-size slide"><button class="dialog-close" type="button" aria-label="Close full-size slide">×</button><img alt="Expanded slide"></dialog></body></html>'''

def main():
    assert all((ROOT / f"assets/slides/{i:02d}.png").exists() for i in range(1, 26))
    assert all((ROOT / f"assets/video/slides/{i:02d}.mp4").exists() for i in range(1, 17))
    (ROOT / "index.html").write_text(page(), encoding="utf-8")
    (ROOT / "site-data.json").write_text(json.dumps({
        "titles": TITLES, "chapters": CHAPTERS, "appendix": APPENDIX,
        "main_slide_durations_seconds": MAIN_DURATIONS,
    }, indent=2), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

if __name__ == "__main__":
    main()
