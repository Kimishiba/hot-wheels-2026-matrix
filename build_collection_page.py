import json

with open('owned_cars.json') as f:
    cars = json.load(f)

total_count = len(cars)
pkg_count = len([c for c in cars if c['condition'] == 'In Packaging'])
loose_count = len([c for c in cars if c['condition'] == 'Loose'])
hw_count = len([c for c in cars if c['brand'] == 'Hot Wheels'])
mbx_count = len([c for c in cars if c['brand'] == 'Matchbox'])

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#ff5f1f">
  <title>Owned Vehicles Garage — Hot Wheels & Matchbox Collection</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anybody:wght@700;800;900&family=Hanken+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #f4f4f0;
      --surface: #ffffff;
      --black: #000000;
      --orange: #ff5f1f;
      --orange-hover: #e04f14;
      --pkg-badge: #10b981;
      --loose-badge: #f59e0b;
      --hw-blue: #0284c7;
      --mbx-red: #e11d48;
      --border-thick: 4px solid #000000;
      --border-mid: 3px solid #000000;
      --border-thin: 2px solid #000000;
      --shadow-base: 4px 4px 0px #000000;
      --shadow-hover: 6px 6px 0px #000000;
      --shadow-active: 1px 1px 0px #000000;
      --shadow-modal: 10px 10px 0px #000000;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg);
      background-image: radial-gradient(#d1d5db 1.2px, transparent 1.2px);
      background-size: 16px 16px;
      font-family: 'Hanken Grotesk', -apple-system, sans-serif;
      color: var(--black);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* HEADER */
    header.top-bar {{
      background: #ffffff;
      border-bottom: var(--border-thick);
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0px 4px 0px rgba(0,0,0,0.1);
    }}

    .header-inner {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .brand-title {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.4rem;
      text-transform: uppercase;
      letter-spacing: -0.03em;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-title span.accent {{
      background: var(--orange);
      color: #ffffff;
      padding: 2px 8px;
      border: var(--border-mid);
      box-shadow: 2px 2px 0px #000000;
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .btn {{
      font-family: 'Anybody', sans-serif;
      font-weight: 800;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: -0.01em;
      padding: 8px 14px;
      background: #ffffff;
      color: var(--black);
      border: var(--border-mid);
      box-shadow: var(--shadow-base);
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.08s ease;
      border-radius: 0px;
    }}

    .btn:hover {{
      transform: translate(-2px, -2px);
      box-shadow: var(--shadow-hover);
    }}

    .btn:active {{
      transform: translate(2px, 2px);
      box-shadow: var(--shadow-active);
    }}

    .btn.primary {{
      background: var(--orange);
      color: #ffffff;
    }}

    .btn.primary:hover {{
      background: var(--orange-hover);
    }}

    /* HERO BANNER & STATS */
    .hero-section {{
      max-width: 1600px;
      margin: 24px auto 0;
      padding: 0 20px;
      width: 100%;
    }}

    .hero-card {{
      background: #ffffff;
      border: var(--border-thick);
      box-shadow: var(--shadow-hover);
      padding: 20px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }}

    .hero-text h1 {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: clamp(1.4rem, 2.5vw, 2.2rem);
      letter-spacing: -0.03em;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}

    .hero-text p {{
      font-size: 0.95rem;
      font-weight: 600;
      color: #4b5563;
    }}

    .stats-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .stat-box {{
      background: #f9f9f9;
      border: var(--border-mid);
      box-shadow: 3px 3px 0px #000000;
      padding: 10px 16px;
      min-width: 105px;
      text-align: center;
    }}

    .stat-val {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.5rem;
      line-height: 1.1;
    }}

    .stat-label {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 0.65rem;
      text-transform: uppercase;
      margin-top: 4px;
      color: #374151;
    }}

    .stat-box.pkg {{ background: #ecfdf5; border-color: #000000; }}
    .stat-box.pkg .stat-val {{ color: #047857; }}
    .stat-box.loose {{ background: #fffbeb; border-color: #000000; }}
    .stat-box.loose .stat-val {{ color: #b45309; }}
    .stat-box.hw {{ background: #f0f9ff; }}
    .stat-box.hw .stat-val {{ color: #0284c7; }}
    .stat-box.mbx {{ background: #fff1f2; }}
    .stat-box.mbx .stat-val {{ color: #e11d48; }}

    /* CONTROLS & FILTER BAR */
    .controls-section {{
      max-width: 1600px;
      margin: 20px auto 0;
      padding: 0 20px;
      width: 100%;
    }}

    .controls-card {{
      background: #ffffff;
      border: var(--border-thick);
      box-shadow: var(--shadow-base);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .filter-row-primary {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .search-box-wrap {{
      flex: 1;
      min-width: 280px;
      position: relative;
    }}

    .search-input {{
      width: 100%;
      height: 44px;
      padding: 0 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      font-weight: 700;
      border: var(--border-mid);
      box-shadow: 3px 3px 0px #000000;
      outline: none;
      border-radius: 0px;
      background: #ffffff;
    }}

    .search-input:focus {{
      border-color: var(--orange);
      box-shadow: 4px 4px 0px #000000;
    }}

    .condition-filters {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .filter-pill {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 0.75rem;
      text-transform: uppercase;
      padding: 8px 12px;
      background: #f3f4f6;
      border: var(--border-mid);
      box-shadow: 2px 2px 0px #000000;
      cursor: pointer;
      user-select: none;
      transition: all 0.08s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .filter-pill:hover {{
      background: #e5e7eb;
      transform: translateY(-1px);
    }}

    .filter-pill.active {{
      background: var(--black);
      color: #ffffff;
      box-shadow: 3px 3px 0px var(--orange);
      transform: translate(-1px, -1px);
    }}

    .filter-pill.pkg.active {{
      background: #047857;
      color: #ffffff;
      box-shadow: 3px 3px 0px #000000;
    }}

    .filter-pill.loose.active {{
      background: #b45309;
      color: #ffffff;
      box-shadow: 3px 3px 0px #000000;
    }}

    .category-filters {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      border-top: 2px dashed #d1d5db;
      padding-top: 12px;
    }}

    .cat-btn {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 0.7rem;
      text-transform: uppercase;
      padding: 4px 10px;
      background: #ffffff;
      border: var(--border-thin);
      box-shadow: 2px 2px 0px #000000;
      cursor: pointer;
      border-radius: 0px;
      transition: all 0.08s ease;
    }}

    .cat-btn:hover {{
      background: #f1f5f9;
    }}

    .cat-btn.active {{
      background: var(--orange);
      color: #ffffff;
      box-shadow: 2px 2px 0px #000000;
    }}

    /* MAIN CARS GRID */
    main.cars-container {{
      max-width: 1600px;
      margin: 24px auto 40px;
      padding: 0 20px;
      width: 100%;
      flex: 1;
    }}

    .cars-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 18px;
    }}

    /* INDIVIDUAL CAR CARD (NEO-RAW) */
    .vehicle-card {{
      background: #ffffff;
      border: var(--border-thick);
      box-shadow: var(--shadow-base);
      display: flex;
      flex-direction: column;
      cursor: pointer;
      position: relative;
      transition: transform 0.12s ease, box-shadow 0.12s ease;
      overflow: hidden;
    }}

    .vehicle-card:hover {{
      transform: translate(-3px, -3px);
      box-shadow: var(--shadow-hover);
    }}

    /* CARD CONDITION BANNER */
    .card-topbar {{
      height: 28px;
      background: #ececec;
      border-bottom: var(--border-mid);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      font-weight: 800;
    }}

    .brand-tag {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      text-transform: uppercase;
    }}

    .brand-tag.hw {{ color: var(--hw-blue); }}
    .brand-tag.mbx {{ color: var(--mbx-red); }}

    .condition-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 6px;
      border: 1.5px solid #000000;
      box-shadow: 1.5px 1.5px 0px #000000;
    }}

    .condition-badge.pkg {{
      background: var(--pkg-badge);
      color: #ffffff;
    }}

    .condition-badge.loose {{
      background: var(--loose-badge);
      color: #000000;
    }}

    /* IMAGE CONTAINER */
    .car-image-box {{
      width: 100%;
      height: 180px;
      background: #ffffff;
      border-bottom: var(--border-mid);
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}

    .car-image-box img {{
      max-width: 95%;
      max-height: 95%;
      object-fit: contain;
      image-rendering: auto;
      transition: transform 0.2s ease;
    }}

    .vehicle-card:hover .car-image-box img {{
      transform: scale(1.05);
    }}

    .photo-type-chip {{
      position: absolute;
      bottom: 6px;
      left: 6px;
      background: #000000;
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.58rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 1px 5px;
    }}

    .dual-indicator-chip {{
      position: absolute;
      bottom: 6px;
      right: 6px;
      background: var(--orange);
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.58rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 1px 6px;
      border: 1px solid #000000;
      box-shadow: 1.5px 1.5px 0px #000000;
    }}

    /* CARD INFO BODY */
    .card-body {{
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      flex: 1;
      justify-content: space-between;
      gap: 10px;
    }}

    .car-name {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.05rem;
      letter-spacing: -0.02em;
      text-transform: uppercase;
      line-height: 1.25;
      color: var(--black);
    }}

    .car-meta-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      color: #4b5563;
    }}

    .car-series {{
      color: #000000;
      background: #f1f5f9;
      padding: 2px 6px;
      border: 1px solid #000000;
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
      max-width: 180px;
    }}

    .car-col-num {{
      font-weight: 800;
      color: var(--orange);
    }}

    .card-desc {{
      font-size: 0.8rem;
      line-height: 1.35;
      color: #374151;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .card-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 4px;
    }}

    .tag-chip {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.62rem;
      font-weight: 700;
      background: #f3f4f6;
      border: 1px solid #d1d5db;
      padding: 1px 4px;
      color: #374151;
    }}

    /* NO RESULTS */
    .empty-state {{
      grid-column: 1 / -1;
      background: #ffffff;
      border: var(--border-thick);
      box-shadow: var(--shadow-base);
      padding: 40px;
      text-align: center;
      margin: 20px 0;
    }}

    .empty-state h3 {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.5rem;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}

    /* ========================================================= */
    /* ENLARGED CARD MODAL (DUAL PHOTO SHOWCASE)                 */
    /* ========================================================= */
    .modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.72);
      backdrop-filter: blur(2px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }}

    .modal-backdrop.open {{
      display: flex;
    }}

    .modal-content {{
      background: #ffffff;
      border: var(--border-thick);
      box-shadow: var(--shadow-modal);
      max-width: 960px;
      width: 100%;
      max-height: 92vh;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      position: relative;
    }}

    .modal-header {{
      background: var(--black);
      color: #ffffff;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      position: sticky;
      top: 0;
      z-index: 10;
    }}

    .modal-header-left {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .modal-title {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.3rem;
      text-transform: uppercase;
      letter-spacing: -0.02em;
    }}

    .brand-chip {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 8px;
      border: 1px solid #ffffff;
    }}

    .brand-chip.hw {{
      background: var(--hw-blue);
      color: #ffffff;
    }}

    .brand-chip.mbx {{
      background: var(--mbx-red);
      color: #ffffff;
    }}

    .modal-close {{
      background: var(--orange);
      color: #ffffff;
      border: 2px solid #ffffff;
      width: 34px;
      height: 34px;
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.2rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.08s ease;
    }}

    .modal-close:hover {{
      background: var(--orange-hover);
      transform: scale(1.05);
    }}

    .modal-body {{
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}

    /* VIEW CONTROLS */
    .modal-view-controls {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background: #f3f4f6;
      border: var(--border-thin);
      padding: 8px 12px;
      flex-wrap: wrap;
    }}

    .view-ctrl-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      color: #374151;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .view-btn-group {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .view-toggle-btn {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 6px 12px;
      background: #ffffff;
      border: var(--border-thin);
      box-shadow: 2px 2px 0px #000000;
      cursor: pointer;
      border-radius: 0px;
      transition: all 0.08s ease;
    }}

    .view-toggle-btn:hover {{
      background: #f1f5f9;
    }}

    .view-toggle-btn.active {{
      background: var(--orange);
      color: #ffffff;
      box-shadow: 2px 2px 0px #000000;
    }}

    /* DUAL PHOTO SHOWCASE GRID */
    .modal-dual-showcase {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      width: 100%;
    }}

    .modal-dual-showcase.view-my {{
      grid-template-columns: 1fr;
    }}
    .modal-dual-showcase.view-my #card-stock-photo {{
      display: none;
    }}
    .modal-dual-showcase.view-my #card-my-photo {{
      display: flex;
    }}

    .modal-dual-showcase.view-stock {{
      grid-template-columns: 1fr;
    }}
    .modal-dual-showcase.view-stock #card-my-photo {{
      display: none;
    }}
    .modal-dual-showcase.view-stock #card-stock-photo {{
      display: flex;
    }}

    .modal-photo-card {{
      background: #ffffff;
      border: var(--border-mid);
      box-shadow: 4px 4px 0px #000000;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .modal-photo-header {{
      padding: 8px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      border-bottom: var(--border-thin);
    }}

    .modal-photo-header.my-photo {{
      background: #fef3c7;
      color: #92400e;
    }}

    .modal-photo-header.stock-photo {{
      background: #e0f2fe;
      color: #0369a1;
    }}

    .photo-subtag {{
      background: #000000;
      color: #ffffff;
      padding: 1px 6px;
      font-size: 0.62rem;
    }}

    .modal-img-frame {{
      width: 100%;
      height: 300px;
      background: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 14px;
      position: relative;
      cursor: zoom-in;
      overflow: hidden;
    }}

    .modal-img-frame img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform 0.2s ease;
    }}

    .modal-img-frame:hover img {{
      transform: scale(1.05);
    }}

    .zoom-pill {{
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(0,0,0,0.85);
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.62rem;
      font-weight: 800;
      text-transform: uppercase;
      padding: 3px 8px;
      border: 1px solid #ffffff;
      box-shadow: 2px 2px 0px #000000;
      opacity: 0.9;
      pointer-events: none;
    }}

    .stock-fallback {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 24px;
      gap: 6px;
    }}

    .stock-fallback span {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.1rem;
      text-transform: uppercase;
      color: #1f2937;
    }}

    .stock-fallback p {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      color: #6b7280;
    }}

    .modal-photo-caption {{
      background: #f9f9f9;
      border-top: 1px solid #e5e7eb;
      padding: 6px 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: #4b5563;
      text-align: center;
      font-weight: 700;
    }}

    /* METADATA GRID */
    .modal-info-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }}

    .modal-info-cell {{
      background: #f9f9f9;
      border: var(--border-thin);
      padding: 8px 12px;
      box-shadow: 2px 2px 0px #000000;
    }}

    .modal-info-cell .label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      font-weight: 800;
      text-transform: uppercase;
      color: #6b7280;
    }}

    .modal-info-cell .val {{
      font-family: 'Hanken Grotesk', sans-serif;
      font-weight: 700;
      font-size: 0.95rem;
      margin-top: 2px;
    }}

    .modal-desc-box {{
      background: #fdfdfd;
      border: var(--border-thin);
      padding: 14px 16px;
      font-size: 0.92rem;
      line-height: 1.5;
      box-shadow: 2px 2px 0px #000000;
    }}

    /* FOOTER */
    footer.page-footer {{
      background: #ffffff;
      border-top: var(--border-thick);
      padding: 18px 20px;
      text-align: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 700;
    }}

    @media (max-width: 768px) {{
      .cars-grid {{
        grid-template-columns: 1fr;
      }}
      .hero-card {{
        flex-direction: column;
        align-items: stretch;
      }}
      .stats-row {{
        justify-content: space-between;
      }}
      .modal-dual-showcase {{
        grid-template-columns: 1fr;
      }}
      .modal-img-frame {{
        height: 220px;
      }}
      .modal-info-grid {{
        grid-template-columns: 1fr 1fr;
      }}
    }}
  </style>
</head>
<body>

  <!-- TOP APP BAR -->
  <header class="top-bar">
    <div class="header-inner">
      <div class="brand-title">
        <span>HOT WHEELS & MATCHBOX</span>
        <span class="accent">GARAGE</span>
      </div>

      <nav class="nav-actions">
        <a href="index.html" class="btn">📦 Case Matrix</a>
        <a href="hot_wheels_2026_case_a_poster.html" class="btn">📄 Poster</a>
        <button class="btn primary" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">⬆ Top</button>
      </nav>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="hero-section">
    <div class="hero-card">
      <div class="hero-text">
        <h1>Owned Vehicles Collection</h1>
        <p>Interactive catalog of all {total_count} owned die-cast models. Click any vehicle card to view enlarged twin photos: your actual collection photo alongside the official stock art.</p>
      </div>

      <div class="stats-row">
        <div class="stat-box">
          <div class="stat-val" id="stat-total">{total_count}</div>
          <div class="stat-label">Total Owned</div>
        </div>
        <div class="stat-box pkg">
          <div class="stat-val">{pkg_count}</div>
          <div class="stat-label">In Packaging</div>
        </div>
        <div class="stat-box loose">
          <div class="stat-val">{loose_count}</div>
          <div class="stat-label">Loose</div>
        </div>
        <div class="stat-box hw">
          <div class="stat-val">{hw_count}</div>
          <div class="stat-label">Hot Wheels</div>
        </div>
        <div class="stat-box mbx">
          <div class="stat-val">{mbx_count}</div>
          <div class="stat-label">Matchbox</div>
        </div>
      </div>
    </div>
  </section>

  <!-- CONTROLS & FILTER BAR -->
  <section class="controls-section">
    <div class="controls-card">
      <div class="filter-row-primary">
        <div class="search-box-wrap">
          <input type="text" id="search-input" class="search-input" placeholder="🔍 Search model, color, series, tampo, brand..." oninput="handleSearch()">
        </div>

        <div class="condition-filters">
          <button class="filter-pill active" onclick="setConditionFilter('all', this)">All ({total_count})</button>
          <button class="filter-pill pkg" onclick="setConditionFilter('In Packaging', this)">📦 In Packaging ({pkg_count})</button>
          <button class="filter-pill loose" onclick="setConditionFilter('Loose', this)">🔓 Loose ({loose_count})</button>
          <button class="filter-pill" onclick="setBrandFilter('Hot Wheels', this)">🔥 Hot Wheels ({hw_count})</button>
          <button class="filter-pill" onclick="setBrandFilter('Matchbox', this)">🔴 Matchbox ({mbx_count})</button>
        </div>
      </div>

      <div class="category-filters" id="category-filters">
        <button class="cat-btn active" onclick="setCategoryFilter('all', this)">All Categories</button>
        <button class="cat-btn" onclick="setCategoryFilter('Muscle & Hot Rods', this)">Muscle & Hot Rods</button>
        <button class="cat-btn" onclick="setCategoryFilter('JDM & Tuners', this)">JDM & Tuners</button>
        <button class="cat-btn" onclick="setCategoryFilter('Exotics & Supercars', this)">Exotics & Supercars</button>
        <button class="cat-btn" onclick="setCategoryFilter('Trucks & 4x4', this)">Trucks & 4x4</button>
        <button class="cat-btn" onclick="setCategoryFilter('Emergency & First Responders', this)">Emergency & Rescue</button>
        <button class="cat-btn" onclick="setCategoryFilter('Construction & Industrial', this)">Construction & Heavy</button>
        <button class="cat-btn" onclick="setCategoryFilter('Concept & Track', this)">Concept & Track</button>
      </div>
    </div>
  </section>

  <!-- CARS GRID -->
  <main class="cars-container">
    <div class="cars-grid" id="cars-grid">
      <!-- Dynamically populated by JS -->
    </div>
  </main>

  <!-- VEHICLE DETAIL ENLARGED MODAL (DUAL PHOTOS) -->
  <div class="modal-backdrop" id="modal-backdrop" onclick="closeModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div class="modal-header-left">
          <span class="modal-title" id="m-title">Model Name</span>
          <span class="brand-chip" id="m-brand-chip">Hot Wheels</span>
        </div>
        <button class="modal-close" onclick="closeModal()" title="Close (Esc)">✕</button>
      </div>

      <div class="modal-body">
        <!-- View Mode Switcher -->
        <div class="modal-view-controls">
          <span class="view-ctrl-label">SHOWCASE MODE:</span>
          <div class="view-btn-group">
            <button class="view-toggle-btn active" id="view-mode-dual" onclick="setModalViewMode('dual')">⚡ SIDE-BY-SIDE DUAL VIEW</button>
            <button class="view-toggle-btn" id="view-mode-my" onclick="setModalViewMode('my')">📷 MY PHOTO</button>
            <button class="view-toggle-btn" id="view-mode-stock" onclick="setModalViewMode('stock')">🎨 OFFICIAL STOCK ART</button>
          </div>
        </div>

        <!-- Dual Photo Showcase Grid -->
        <div class="modal-dual-showcase" id="modal-showcase">
          <!-- CARD 1: MY PHOTO -->
          <div class="modal-photo-card" id="card-my-photo">
            <div class="modal-photo-header my-photo">
              <span>📷 MY GARAGE PHOTO</span>
              <span class="photo-subtag" id="m-photo-subtag">Actual Die-Cast</span>
            </div>
            <div class="modal-img-frame" onclick="openFullImage('my')" title="Click to open full resolution photo">
              <img id="m-my-img" src="" alt="My Vehicle Photo">
              <span class="zoom-pill">🔍 Zoom Full Size</span>
            </div>
            <div class="modal-photo-caption" id="m-my-caption">
              Actual physical item in collection
            </div>
          </div>

          <!-- CARD 2: STOCK IMAGE -->
          <div class="modal-photo-card" id="card-stock-photo">
            <div class="modal-photo-header stock-photo">
              <span>🎨 OFFICIAL STOCK ART</span>
              <span class="photo-subtag" id="m-stock-subtag">Mattel Catalog</span>
            </div>
            <div class="modal-img-frame" onclick="openFullImage('stock')" title="Click to open official stock photo">
              <img id="m-stock-img" src="" alt="Official Stock Art" onerror="handleStockImgError()">
              <div id="m-stock-fallback" class="stock-fallback" style="display:none;">
                <span>📦 Custom / Special Casting</span>
                <p>No official studio catalog image available</p>
              </div>
              <span class="zoom-pill" id="m-stock-zoom">🔍 Zoom Full Size</span>
            </div>
            <div class="modal-photo-caption" id="m-stock-caption">
              Official package card art & catalog studio render
            </div>
          </div>
        </div>

        <!-- Technical & Collector Specifications Grid -->
        <div class="modal-info-grid">
          <div class="modal-info-cell">
            <div class="label">Condition</div>
            <div class="val" id="m-condition">In Packaging</div>
          </div>
          <div class="modal-info-cell">
            <div class="label">Brand</div>
            <div class="val" id="m-brand">Hot Wheels</div>
          </div>
          <div class="modal-info-cell">
            <div class="label">Series / Sub-Series</div>
            <div class="val" id="m-series">HW J-Imports</div>
          </div>
          <div class="modal-info-cell">
            <div class="label">Color / Livery</div>
            <div class="val" id="m-color">World Rally Blue</div>
          </div>
          <div class="modal-info-cell">
            <div class="label">Collector Number</div>
            <div class="val" id="m-col">#176/250</div>
          </div>
          <div class="modal-info-cell">
            <div class="label">Category</div>
            <div class="val" id="m-cat">JDM & Tuners</div>
          </div>
        </div>

        <!-- Description Box -->
        <div class="modal-desc-box" id="m-desc">
          Description details go here.
        </div>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="page-footer">
    <p>Hot Wheels & Matchbox Personal Die-Cast Garage • Hosted on GitHub Pages • Made by Antigravity</p>
  </footer>

  <script>
    const allCars = {json.dumps(cars)};
    let activeCondition = 'all';
    let activeBrand = 'all';
    let activeCategory = 'all';
    let searchQuery = '';
    let currentCar = null;
    let currentViewMode = 'dual';

    function renderCars() {{
      const grid = document.getElementById('cars-grid');
      grid.innerHTML = '';

      const filtered = allCars.filter(car => {{
        if (activeCondition !== 'all' && car.condition !== activeCondition) return false;
        if (activeBrand !== 'all' && car.brand !== activeBrand) return false;
        if (activeCategory !== 'all' && car.category !== activeCategory) return false;
        if (searchQuery) {{
          const q = searchQuery.toLowerCase();
          const matchName = car.name.toLowerCase().includes(q);
          const matchSeries = car.series.toLowerCase().includes(q);
          const matchColor = car.color.toLowerCase().includes(q);
          const matchBrand = car.brand.toLowerCase().includes(q);
          const matchDesc = car.description.toLowerCase().includes(q);
          const matchTags = car.tags.some(t => t.toLowerCase().includes(q));
          if (!matchName && !matchSeries && !matchColor && !matchBrand && !matchDesc && !matchTags) return false;
        }}
        return true;
      }});

      if (filtered.length === 0) {{
        grid.innerHTML = `
          <div class="empty-state">
            <h3>No Vehicles Match Your Filter</h3>
            <p style="margin-top: 8px; color: #4b5563;">Try clearing your search query or selecting a different category.</p>
            <button class="btn primary" style="margin-top: 16px;" onclick="resetFilters()">Reset All Filters</button>
          </div>
        `;
        return;
      }}

      filtered.forEach(car => {{
        const isPkg = car.condition === 'In Packaging';
        const card = document.createElement('div');
        card.className = 'vehicle-card';
        card.onclick = () => openModal(car);

        const brandClass = car.brand === 'Hot Wheels' ? 'hw' : 'mbx';
        const brandIcon = car.brand === 'Hot Wheels' ? '🔥' : '🔴';

        card.innerHTML = `
          <div class="card-topbar">
            <span class="brand-tag ${{brandClass}}">${{brandIcon}} ${{car.brand}}</span>
            <span class="condition-badge ${{isPkg ? 'pkg' : 'loose'}}">${{isPkg ? '📦 IN PACKAGING' : '🔓 LOOSE'}}</span>
          </div>

          <div class="car-image-box">
            <img src="${{car.image}}" alt="${{car.name}}" loading="lazy" onerror="this.src='${{car.official_image || ''}}'">
            <span class="photo-type-chip">${{isPkg ? 'Blister Photo' : 'Actual Vehicle'}}</span>
            <span class="dual-indicator-chip">⚡ Dual View</span>
          </div>

          <div class="card-body">
            <div>
              <div class="car-name">${{car.name}}</div>
              <div class="car-meta-row" style="margin-top: 6px;">
                <span class="car-series">${{car.series}}</span>
                <span class="car-col-num">${{car.col_num || ''}}</span>
              </div>
            </div>

            <p class="card-desc">${{car.description}}</p>

            <div class="card-tags">
              <span class="tag-chip" style="background:#fef3c7; color:#92400e;">${{car.color}}</span>
              <span class="tag-chip">${{car.category}}</span>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function setConditionFilter(cond, btn) {{
      activeCondition = cond;
      activeBrand = 'all';
      document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderCars();
    }}

    function setBrandFilter(brand, btn) {{
      activeBrand = brand;
      activeCondition = 'all';
      document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderCars();
    }}

    function setCategoryFilter(cat, btn) {{
      activeCategory = cat;
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderCars();
    }}

    function handleSearch() {{
      searchQuery = document.getElementById('search-input').value.trim();
      renderCars();
    }}

    function resetFilters() {{
      activeCondition = 'all';
      activeBrand = 'all';
      activeCategory = 'all';
      searchQuery = '';
      document.getElementById('search-input').value = '';
      document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
      document.querySelector('.filter-pill').classList.add('active');
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      document.querySelector('.cat-btn').classList.add('active');
      renderCars();
    }}

    function openModal(car) {{
      currentCar = car;
      document.getElementById('m-title').textContent = car.name;

      const brandChip = document.getElementById('m-brand-chip');
      brandChip.textContent = car.brand;
      brandChip.className = 'brand-chip ' + (car.brand === 'Hot Wheels' ? 'hw' : 'mbx');

      // My photo
      const myImg = document.getElementById('m-my-img');
      myImg.src = car.image;
      document.getElementById('m-photo-subtag').textContent = car.condition === 'In Packaging' ? 'Carded Blister' : 'Loose Die-Cast';
      document.getElementById('m-my-caption').textContent = `${{car.condition}} collection photograph`;

      // Stock image
      const stockImg = document.getElementById('m-stock-img');
      const stockFallback = document.getElementById('m-stock-fallback');
      const stockZoom = document.getElementById('m-stock-zoom');

      if (car.official_image) {{
        stockImg.style.display = 'block';
        stockFallback.style.display = 'none';
        stockZoom.style.display = 'inline-block';
        stockImg.src = car.official_image;
        document.getElementById('m-stock-subtag').textContent = 'Catalog / Card Art';
        document.getElementById('m-stock-caption').textContent = 'Official Mattel / studio catalog render';
      }} else {{
        stockImg.style.display = 'none';
        stockFallback.style.display = 'flex';
        stockZoom.style.display = 'none';
        document.getElementById('m-stock-subtag').textContent = 'Unofficial / Custom';
        document.getElementById('m-stock-caption').textContent = 'Special build / custom casting without studio art';
      }}

      // Specifications
      document.getElementById('m-condition').textContent = car.condition;
      document.getElementById('m-condition').style.color = car.condition === 'In Packaging' ? '#047857' : '#b45309';
      document.getElementById('m-brand').textContent = car.brand;
      document.getElementById('m-series').textContent = car.series;
      document.getElementById('m-color').textContent = car.color;
      document.getElementById('m-col').textContent = car.col_num || 'N/A';
      document.getElementById('m-cat').textContent = car.category;
      document.getElementById('m-desc').textContent = car.description;

      setModalViewMode('dual');

      document.getElementById('modal-backdrop').classList.add('open');
      document.body.style.overflow = 'hidden';
    }}

    function setModalViewMode(mode) {{
      currentViewMode = mode;
      const showcase = document.getElementById('modal-showcase');
      showcase.className = 'modal-dual-showcase view-' + mode;

      document.querySelectorAll('.view-toggle-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById('view-mode-' + mode);
      if (activeBtn) activeBtn.classList.add('active');
    }}

    function openFullImage(which) {{
      if (!currentCar) return;
      const targetSrc = which === 'my' ? currentCar.image : currentCar.official_image;
      if (targetSrc) {{
        window.open(targetSrc, '_blank');
      }}
    }}

    function handleStockImgError() {{
      const stockImg = document.getElementById('m-stock-img');
      const stockFallback = document.getElementById('m-stock-fallback');
      stockImg.style.display = 'none';
      stockFallback.style.display = 'flex';
    }}

    function closeModal() {{
      document.getElementById('modal-backdrop').classList.remove('open');
      document.body.style.overflow = '';
    }}

    document.addEventListener('keydown', e => {{
      if (e.key === 'Escape') closeModal();
    }});

    // Initial render
    renderCars();
  </script>
</body>
</html>
'''

with open('collection.html', 'w') as f:
    f.write(html_template)

print("Generated collection.html successfully!")
