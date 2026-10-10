"""Package the final assessment deck as a static, accessible GitHub Pages site.

The source PowerPoint and PDF exports are read only.
"""
from __future__ import annotations

import html
import json
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent
DECK = Path('/Users/bala/Documents/Codex/Interview Prep/Stripe/Stripe_Assessment.pptx')
RENDER = ROOT / '.render'
ASSETS = ROOT / 'assets'
PDFTOPPM = '/Users/bala/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftoppm'

TITLES = [
    'AI Powered Agent',
    'What you’ll see in this walkthrough',
    'From analyst queue to guided payment investigations',
    'How It Works',
    'AI Powered Agent architecture',
    'Working demo',
    'Key Features',
    'Impact & Value Proposition',
    'How the agent investigates the metric gap',
    'Adaptive Auth: the explanation Claude never received',
    'How I fixed the Adaptive Auth retrieval failure',
    'A wrong-year answer changed the prompt and SQL rule',
    'A 1,000-character limit hid the schema the agent needed',
    'Test Coverage Matrix',
    'Usage and reliability',
    'Making the architecture reusable',
    'What I’d bring to Stripe Finance',
]

CHAPTERS = [
    'Introduction', 'Introduction', 'The workflow', 'The experience', 'The build',
    'Working demo', 'The experience', 'The value', 'The build',
    'What failed', 'What changed', 'What changed', 'What changed',
    'Validation', 'Observed usage', 'Reusable design', 'Closing',
]

APPENDIX = [
    'Two skills make setup reusable',
    'Reuse across Expedia',
    'Analytical scope and example investigations',
    'Two execution paths',
    'Inside the investigative tool loop',
    'Controls around the agent',
    'How feedback becomes reusable knowledge',
    'Reference: a defined calculation',
]

def esc(value: str) -> str:
    return html.escape(value, quote=True)


def main() -> None:
    (ASSETS / 'slides').mkdir(parents=True, exist_ok=True)
    (ASSETS / 'video').mkdir(parents=True, exist_ok=True)
    (ASSETS / 'documents').mkdir(parents=True, exist_ok=True)
    for number in range(1, 26):
        shutil.copy2(RENDER / f'slide-{number}.png', ASSETS / 'slides' / f'{number:02}.png')

    with ZipFile(DECK) as z:
        (ASSETS / 'video' / 'agent-demo.mp4').write_bytes(z.read('ppt/media/media1.mp4'))
        (ASSETS / 'video' / 'reusable-architecture.mp4').write_bytes(z.read('ppt/media/media2.mp4'))
        (ASSETS / 'video' / 'agent-demo-poster.png').write_bytes(z.read('ppt/media/image33.png'))
        (ASSETS / 'video' / 'reusable-architecture-poster.jpg').write_bytes(z.read('ppt/media/image63.jpg'))
    # Only the redacted review copies are packaged. Source exports stay outside this repository.
    for name, stem in [('Agent UI - Redacted.pdf', 'agent-ui'), ('Agent UI - PLS Sample Prompts - Redacted.pdf', 'pls-prompts')]:
        subprocess.run([PDFTOPPM, '-jpeg', '-r', '180', '-jpegopt', 'quality=84,optimize=y',
                        str(ASSETS / 'documents' / name), str(ASSETS / 'documents' / stem)], check=True)

    panels = []
    for index, (title, chapter) in enumerate(zip(TITLES, CHAPTERS), 1):
        theme = 'dark' if index in (1, 2, 4, 6, 7, 14, 16, 17) else 'light'
        eager = 'fetchpriority="high"' if index == 1 else 'loading="lazy"'
        if index in (6, 16):
            src = 'agent-demo.mp4' if index == 6 else 'reusable-architecture.mp4'
            poster = 'agent-demo-poster.png' if index == 6 else 'reusable-architecture-poster.jpg'
            label = 'Watch the working agent' if index == 6 else 'Watch the reusable setup'
            media = f'''<div class="video-area single-video">
              <video controls playsinline preload="metadata" poster="assets/video/{poster}" aria-label="{esc(label)}">
                <source src="assets/video/{src}" type="video/mp4">
                Your browser does not support this video. <a href="assets/video/{src}">Download the recording</a>.
              </video>
              <a class="media-link" href="assets/video/{src}" download>Download recording <span aria-hidden="true">↗</span></a>
            </div>'''
            actions = ''
        else:
            media = f'<figure class="slide-frame"><img src="assets/slides/{index:02}.png" alt="Slide {index}: {esc(title)}" width="1920" height="1080" {eager}></figure>'
            actions = f'<div class="panel-bottom"><button class="expand" type="button" data-slide="{index}" aria-label="Expand slide {index}">View full size <span aria-hidden="true">↗</span></button></div>'
        panels.append(f'''<section id="slide-{index}" class="story-panel {theme}" aria-labelledby="title-{index}">
          <div class="panel-top"><span class="chapter">{esc(chapter)}</span><span class="count">{index:02} / 17</span></div>
          <h2 id="title-{index}" class="panel-title">{esc(title)}</h2>
          {media}
          {actions}
        </section>''')

    appendix_items = []
    for index, title in enumerate(APPENDIX, 18):
        appendix_items.append(f'''<details class="appendix-item"><summary><span>{index - 17:02}</span>{esc(title)}<span class="plus" aria-hidden="true">+</span></summary>
          <img src="assets/slides/{index:02}.png" alt="Appendix slide: {esc(title)}" width="1920" height="1080" loading="lazy">
        </details>''')

    def page_previews(stem: str, count: int) -> str:
        return ''.join(f'<img src="assets/documents/{stem}-{i}.jpg" alt="Page {i} of {count}" loading="lazy">' for i in range(1, count + 1))

    html_text = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#062657">
  <meta name="description" content="Bala Manoghar Mathavy’s AI Solutions assessment: a payment analytics agent, its workflow, working demo, design decisions, failures, fixes, and evidence.">
  <meta property="og:title" content="AI Powered Agent · Bala Manoghar Mathavy">
  <meta property="og:description" content="From analyst queue to guided payment investigations. An interactive, slide-by-slide case study with embedded demos.">
  <meta property="og:image" content="https://balamm27.github.io/Stripe-Assessment/assets/slides/01.png">
  <meta property="og:type" content="website">
  <title>AI Powered Agent | Bala Manoghar Mathavy</title>
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script src="app.js" defer></script>
</head>
<body>
  <a class="skip" href="#slide-1">Skip to the case study</a>
  <div class="scroll-progress" aria-hidden="true"><span></span></div>
  <header class="site-header"><a class="wordmark" href="#slide-1">BALA <span>/ AI SOLUTIONS</span></a>
    <nav aria-label="Primary"><a href="#slide-3">Workflow</a><a href="#slide-6">Demo</a><a href="#slide-10">Build lessons</a><a href="#slide-14">Evidence</a><a href="#appendix">Appendix</a></nav>
    <button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false">Menu</button>
  </header>
  <main>
    {''.join(panels)}
    <section id="appendix" class="appendix-section" aria-labelledby="appendix-title"><div class="section-inner">
      <span class="eyebrow">Optional technical detail</span><h2 id="appendix-title">Appendix</h2>
      <p class="section-intro">The final PowerPoint has eight hidden reference slides. Open any topic below to see the original slide.</p>
      <div class="appendix-list">{''.join(appendix_items)}</div>
    </div></section>
    <section id="ui-exports" class="documents-section" aria-labelledby="documents-title"><div class="section-inner">
      <span class="eyebrow">External review copies</span><h2 id="documents-title">Agent UI examples</h2>
      <p class="section-intro">These examples preserve the questions and response structure. Numerical values and identifiers are redacted for external sharing.</p>
      <div class="document-list">
        <article class="document"><div class="document-heading"><h3>Agent UI</h3><a href="assets/documents/Agent%20UI%20-%20Redacted.pdf" target="_blank" rel="noopener">Open redacted PDF ↗</a></div><div class="document-pages">{page_previews('agent-ui', 3)}</div></article>
        <article class="document"><div class="document-heading"><h3>Agent UI · PLS sample prompts</h3><a href="assets/documents/Agent%20UI%20-%20PLS%20Sample%20Prompts%20-%20Redacted.pdf" target="_blank" rel="noopener">Open redacted PDF ↗</a></div><div class="document-pages">{page_previews('pls-prompts', 5)}</div></article>
      </div>
    </div></section>
  </main>
  <footer><span>Bala Manoghar Mathavy</span><span>AI Powered Agent · October 2026</span><a href="#slide-1">Back to top ↑</a></footer>
  <dialog id="slide-dialog" aria-label="Full-size slide"><button class="dialog-close" type="button" aria-label="Close full-size slide">×</button><img alt="Expanded slide"></dialog>
</body>
</html>'''
    (ROOT / 'index.html').write_text(html_text, encoding='utf-8')
    (ROOT / '.nojekyll').write_text('', encoding='utf-8')
    (ROOT / 'site-data.json').write_text(json.dumps({'titles': TITLES, 'chapters': CHAPTERS, 'appendix': APPENDIX}, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
