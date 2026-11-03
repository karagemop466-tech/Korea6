from pathlib import Path
pages={
 'exec':'Executive summary',
 'index':'Overview',
 'schedule':'Daily schedule',
 'vacations':'Vacation finder',
 'core-scope':'Scope & AM/FM proof',
 'radio':'Radio guide',
 'sources':'Sources & method',
 'review':'Flagged for review',
}
current='aria-current="page"'
icons=['','◉','▦','↗','⊕','◌','≡','⚑']
for key,title in pages.items():
 if key=='core-scope':
  continue
 nav=''.join(
  f'<a href="{p}.html" class="{"active" if p==key else ""}" {current if p==key else ""}>'
  + (f'<span class="symbol">{icon}</span>' if icon else '')
  + f'{name}</a>'
  for (p,name),icon in zip(pages.items(),icons)
 )
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="A source-backed San Francisco sports and vacation planner. Verified fixtures, radio evidence, and honest schedule uncertainty through 2029."><title>{title} · Free Time Vacation</title><link rel="stylesheet" href="style.css"><link rel="icon" href="favicon.svg" type="image/svg+xml"></head><body data-page="{key}"><a class="sr-only" href="#content">Skip to content</a><aside class="sidebar"><a class="brand" href="index.html"><span class="brandmark">↗</span>free time<small>VACATION PLANNER</small></a><div class="navlabel">YOUR PLANNING DESK</div><nav aria-label="Main navigation">{nav}</nav><div class="sidebarfoot"><strong>San Francisco, CA</strong>Outer Sunset · 94122<br>Standard AM/FM radio<br><br>Less guessing.<br>More time away.</div></aside><div class="main"><header class="topbar"><span>Planning desk <span class="muted">/</span> <b>{title}</b></span><span><span class="dot"></span>Pacific Time · PST / PDT</span></header><main id="content" tabindex="-1"><div class="loading" role="status">Loading official schedule snapshots…</div></main></div><noscript>This dashboard requires JavaScript. Official source records are available as JSON in the data folder. No day can be certified free from this page without loading the records.</noscript><script type="module" src="app.js"></script></body></html>'''
 Path(f'site/{key}.html').write_text(html)
