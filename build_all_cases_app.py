import re
import json

# 1. Load the comprehensive 2026 cases dataset with localized images
with open("cases_2026_full.json", "r", encoding="utf-8") as f:
    cases_dict = json.load(f)

json_str = json.dumps(cases_dict)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <meta name="theme-color" content="#ff5f1f">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <title>Hot Wheels 2026 Mainlines — Master Case Matrix (All Cases)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anybody:wght@700;800;900&family=Hanken+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #ffffff;
      --surface: #f9f9f9;
      --black: #000000;
      --accent: #ff5f1f;
      --accent-hover: #e04f14;
      --sth-gold: #fbbf24;
      --th-green: #34d399;
      --new-blue: #38bdf8;
      --border-thick: 3px solid #000000;
      --border-thin: 2px solid #000000;
      --shadow-base: 3px 3px 0px #000000;
      --shadow-hover: 5px 5px 0px #000000;
      --shadow-modal: 10px 10px 0px #000000;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100vw;
      height: 100vh;
      min-height: 100dvh;
      overflow: hidden; /* STRICT NO-SCROLL ON DESKTOP */
      background-color: #f1f2f4;
      background-image: radial-gradient(#d1d5db 1.2px, transparent 1.2px);
      background-size: 16px 16px;
      font-family: 'Hanken Grotesk', -apple-system, sans-serif;
      color: #000000;
      display: flex;
      flex-direction: column;
    }}

    body.modal-open {{
      overflow: hidden !important;
    }}

    /* HEADER TOOLBAR */
    .header-bar {{
      background: #ffffff;
      border-bottom: var(--border-thick);
      z-index: 50;
      box-sizing: border-box;
    }}

    /* DESKTOP HEADER (>= 1025px) */
    @media (min-width: 1025px) {{
      .header-bar {{
        height: 54px;
        min-height: 54px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 12px;
        gap: 10px;
      }}

      .header-top-row {{
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }}

      .cases-nav-container {{
        display: flex;
        align-items: center;
        flex-shrink: 0;
      }}

      .cases-nav {{
        display: flex;
        align-items: center;
        gap: 4px;
        background: #f1f5f9;
        border: var(--border-thin);
        padding: 3px;
        box-shadow: 2px 2px 0px #000000;
      }}

      .stats-pills-container {{
        display: flex;
        align-items: center;
        flex-shrink: 0;
      }}

      .stats-pills {{
        display: flex;
        gap: 6px;
        flex-shrink: 0;
      }}

      .header-actions.desktop-only {{
        display: flex;
        gap: 6px;
        align-items: center;
        flex-shrink: 0;
      }}

      .mobile-only {{
        display: none !important;
      }}
    }}

    .brand-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }}

    .brand-title {{
      font-family: 'Anybody', sans-serif;
      font-weight: 900;
      font-size: 1.15rem;
      letter-spacing: -0.03em;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .case-pill {{
      padding: 4px 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 800;
      background: #ffffff;
      border: 1.5px solid #000000;
      cursor: pointer;
      user-select: none;
      transition: all 0.08s ease;
      color: #000000;
    }}

    .case-pill:hover {{
      background: #e2e8f0;
      transform: translateY(-1px);
    }}

    .case-pill.active {{
      background: var(--accent);
      color: #ffffff;
      box-shadow: 2px 2px 0px #000000;
      transform: translate(-1px, -1px);
    }}

    .pill {{
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 2px 6px;
      border: var(--border-thin);
      background: #ffffff;
      box-shadow: 2px 2px 0px #000000;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
      white-space: nowrap;
    }}

    .pill.sth {{ background: var(--sth-gold); }}
    .pill.th {{ background: #bbf7d0; }}
    .pill.new {{ background: #bae6fd; }}
    .pill.recolor {{ background: #e2e8f0; }}

    .btn-action {{
      background: var(--accent);
      color: #ffffff;
      border: var(--border-thin);
      box-shadow: 2px 2px 0px #000000;
      font-family: 'Anybody', sans-serif;
      font-weight: 800;
      font-size: 0.72rem;
      text-transform: uppercase;
      padding: 5px 10px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      text-decoration: none;
      transition: all 0.08s ease;
    }}

    .btn-action:hover {{
      background: var(--accent-hover);
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }}

    .btn-action:active {{
      transform: translate(2px, 2px);
      box-shadow: 0px 0px 0px #000000;
    }}

    /* DESKTOP GRID CONTAINER (FITS STRICTLY WITHIN VIEWPORT) */
    @media (min-width: 1025px) {{
      .grid-container {{
        width: 100%;
        height: calc(100vh - 54px);
        padding: 6px 8px;
        display: grid;
        grid-template-columns: repeat(9, minmax(0, 1fr));
        grid-template-rows: repeat(3, minmax(0, 1fr));
        gap: 6px;
        box-sizing: border-box;
        perspective: 1200px;
      }}

      .grid-container.layout-7x4 {{
        grid-template-columns: repeat(7, minmax(0, 1fr));
        grid-template-rows: repeat(4, minmax(0, 1fr));
      }}
    }}

    /* INDIVIDUAL CAR CARD */
    .card-wrap {{
      position: relative;
      width: 100%;
      height: 100%;
      min-width: 0;
      min-height: 0;
      perspective: 1000px;
    }}

    .car-card {{
      width: 100%;
      height: 100%;
      min-width: 0;
      min-height: 0;
      background: #ffffff;
      border: var(--border-thick);
      box-shadow: var(--shadow-base);
      display: flex;
      flex-direction: column;
      cursor: pointer;
      transform-style: preserve-3d;
      transition: transform 0.45s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.15s ease;
      position: relative;
      overflow: hidden;
      user-select: none;
    }}

    .car-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-hover);
      border-color: #000000;
    }}

    .car-card.is-sth {{
      border: 3px solid #000000;
      background: #fffbeb;
      box-shadow: 3px 3px 0px var(--sth-gold), 3px 3px 0px 2px #000000;
    }}

    .car-card.is-th {{
      border: 3px solid #000000;
      background: #f0fdf4;
      box-shadow: 3px 3px 0px var(--th-green), 3px 3px 0px 2px #000000;
    }}

    /* CARD HEADER */
    .card-header {{
      height: 20px;
      min-height: 20px;
      min-width: 0;
      background: #ececec;
      border-bottom: 2px solid #000000;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: clamp(0.5rem, 0.65vw, 0.62rem);
      font-weight: 800;
      overflow: hidden;
    }}

    .card-col {{
      background: #000000;
      color: #ffffff;
      padding: 1px 3px;
      white-space: nowrap;
    }}

    .card-toy {{
      color: #4b5563;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    /* CARD IMAGE VIEWPORT */
    .card-img-box {{
      flex: 1;
      min-height: 0;
      min-width: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      padding: 2px 4px;
      background: #ffffff;
      overflow: hidden;
    }}

    .card-img-box img {{
      max-width: 96%;
      max-height: 96%;
      object-fit: contain;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.18));
      transition: transform 0.2s ease;
      pointer-events: none;
    }}

    .car-card:hover .card-img-box img {{
      transform: scale(1.08);
    }}

    /* CARD BADGES */
    .micro-badge {{
      position: absolute;
      top: 3px;
      right: 3px;
      padding: 1px 3px;
      font-family: 'JetBrains Mono', monospace;
      font-size: clamp(0.45rem, 0.55vw, 0.52rem);
      font-weight: 800;
      border: 1.5px solid #000000;
      box-shadow: 1px 1px 0px #000000;
      text-transform: uppercase;
      z-index: 2;
      white-space: nowrap;
    }}

    .micro-badge.sth {{ background: var(--sth-gold); color: #000000; }}
    .micro-badge.th {{ background: #4ade80; color: #000000; }}
    .micro-badge.new {{ background: var(--accent); color: #ffffff; }}
    .micro-badge.recolor {{ background: #e2e8f0; color: #000000; }}

    /* CARD FOOTER */
    .card-info {{
      height: 34px;
      min-height: 34px;
      min-width: 0;
      background: #fafafa;
      border-top: 2px solid #000000;
      padding: 2px 4px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      overflow: hidden;
    }}

    .car-title {{
      font-family: 'Anybody', sans-serif;
      font-weight: 800;
      font-size: clamp(0.55rem, 0.72vw, 0.68rem);
      line-height: 1.1;
      text-transform: uppercase;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      letter-spacing: -0.01em;
      min-width: 0;
    }}

    .car-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: clamp(0.48rem, 0.58vw, 0.56rem);
      font-weight: 700;
      color: #6b7280;
      margin-top: 1px;
      min-width: 0;
    }}

    .car-series {{
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 70%;
      color: #111827;
      font-weight: 800;
      min-width: 0;
    }}

    /* ========================================================
       SHARED-ELEMENT 3D MORPHING CARD & BACKDROP
       ======================================================== */
    .morph-backdrop {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.72);
      backdrop-filter: blur(4px);
      z-index: 100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.4s ease;
    }}

    .morph-backdrop.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    .morph-card {{
      position: fixed;
      z-index: 101;
      pointer-events: auto;
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
      display: none;
      box-sizing: border-box;
      user-select: none;
    }}

    .morph-face {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      box-sizing: border-box;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    .morph-face-front {{
      transform: rotateY(0deg);
      background: #ffffff;
      border: var(--border-thick);
      box-shadow: var(--shadow-base);
    }}

    .morph-face-back {{
      transform: rotateY(180deg);
      background: #ffffff;
      border: 4px solid #000000;
      box-shadow: var(--shadow-modal);
    }}

    /* EXPANDED BACK FACE LAYOUT */
    .modal-topbar {{
      height: 44px;
      min-height: 44px;
      background: #ffffff;
      border-bottom: 4px solid #000000;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      box-sizing: border-box;
    }}

    .modal-title-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.95rem;
      font-weight: 800;
    }}

    .modal-col-tag {{
      background: #000000;
      color: #ffffff;
      padding: 2px 8px;
    }}

    .modal-close-btn {{
      background: #000000;
      color: #ffffff;
      border: none;
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Anybody', sans-serif;
      font-size: 1.1rem;
      font-weight: 900;
      cursor: pointer;
      transition: background 0.1s ease;
    }}

    .modal-close-btn:hover {{
      background: var(--accent);
    }}

    .modal-body {{
      flex: 1;
      min-height: 0;
      display: grid;
      grid-template-columns: 1fr 240px;
      border-bottom: 4px solid #000000;
      box-sizing: border-box;
    }}

    /* CLICKABLE HIGH-RES IMAGE LINK TO FANDOM WIKI */
    .modal-image-stage {{
      background: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      border-right: 4px solid #000000;
      position: relative;
      overflow: hidden;
      height: 100%;
      box-sizing: border-box;
    }}

    .modal-image-link {{
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
      text-decoration: none;
      cursor: pointer;
    }}

    .modal-image-link img {{
      max-width: 95%;
      max-height: 95%;
      object-fit: contain;
      filter: drop-shadow(0 12px 20px rgba(0,0,0,0.25));
      transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
    }}

    .modal-image-link:hover img {{
      transform: scale(1.08) rotate(-1deg);
    }}

    /* HOVER PILL HINT */
    .wiki-hint-pill {{
      position: absolute;
      bottom: 12px;
      background: #000000;
      color: #ffffff;
      border: 2px solid #ffffff;
      box-shadow: 2px 2px 0px rgba(0,0,0,0.5);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 800;
      padding: 5px 12px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      opacity: 0.85;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 6px;
      pointer-events: none;
    }}

    .modal-image-link:hover .wiki-hint-pill {{
      opacity: 1;
      background: var(--accent);
      border-color: #000000;
      box-shadow: 3px 3px 0px #000000;
      transform: translateY(-2px);
    }}

    .modal-sidebar {{
      background: #f8fafc;
      padding: 18px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-sizing: border-box;
      height: 100%;
    }}

    .spec-group {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .spec-item {{
      display: flex;
      flex-direction: column;
    }}

    .spec-lbl {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      font-weight: 800;
      text-transform: uppercase;
      color: #64748b;
    }}

    .spec-val {{
      font-family: 'Anybody', sans-serif;
      font-size: 1.12rem;
      font-weight: 900;
      line-height: 1.2;
      text-transform: uppercase;
      color: #000000;
      margin-top: 2px;
    }}

    .spec-val.badge-wrap {{
      display: inline-flex;
      margin-top: 4px;
    }}

    /* DIRECT FANDOM WIKI BUTTON */
    .btn-fandom {{
      margin-top: 8px;
      background: #ffffff;
      color: #000000;
      border: 2px solid #000000;
      box-shadow: 2px 2px 0px #000000;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 6px 10px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.1s ease;
      text-transform: uppercase;
    }}

    .btn-fandom:hover {{
      background: #000000;
      color: #ffffff;
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }}

    .modal-nav {{
      display: flex;
      gap: 8px;
      margin-top: 12px;
    }}

    .btn-nav {{
      flex: 1;
      padding: 9px;
      background: #ffffff;
      border: 3px solid #000000;
      box-shadow: 2px 2px 0px #000000;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
      font-weight: 800;
      cursor: pointer;
      text-transform: uppercase;
      transition: all 0.1s ease;
    }}

    .btn-nav:hover {{
      background: var(--accent);
      color: #ffffff;
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }}

    .modal-footer {{
      height: 36px;
      min-height: 36px;
      padding: 0 16px;
      background: #eeeeee;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      font-weight: 700;
      box-sizing: border-box;
    }}

    /* ========================================================
       RESPONSIVE MOBILE & TABLET LAYOUT (< 1025px)
       ======================================================== */
    @media (max-width: 1024px) {{
      html, body {{
        width: 100%;
        height: auto !important;
        min-height: 100dvh;
        overflow-x: hidden !important;
        overflow-y: auto !important;
      }}

      .desktop-only {{
        display: none !important;
      }}

      .mobile-only {{
        display: flex !important;
      }}

      .header-bar {{
        position: sticky;
        top: 0;
        z-index: 50;
        display: flex;
        flex-direction: column;
        width: 100%;
        border-bottom: var(--border-thick);
        background: #ffffff;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
      }}

      .header-top-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        border-bottom: 2px solid #000000;
        background: #ffffff;
        width: 100%;
        box-sizing: border-box;
      }}

      .brand-title {{
        font-size: 1.05rem;
      }}

      .cases-nav-container {{
        width: 100%;
        background: #f8fafc;
        border-bottom: 2px solid #000000;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        box-sizing: border-box;
      }}

      .cases-nav-container::-webkit-scrollbar {{
        display: none;
      }}

      .cases-nav {{
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 7px 12px;
        width: max-content;
        background: transparent;
        border: none;
        box-shadow: none;
      }}

      .case-pill {{
        flex-shrink: 0;
        min-width: 38px;
        height: 36px;
        padding: 0 10px;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #000000;
        box-shadow: 2px 2px 0px #000000;
        border-radius: 0;
      }}

      .stats-pills-container {{
        width: 100%;
        background: #ffffff;
        border-bottom: 2px solid #000000;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        box-sizing: border-box;
      }}

      .stats-pills-container::-webkit-scrollbar {{
        display: none;
      }}

      .stats-pills {{
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        width: max-content;
      }}

      .pill {{
        font-size: 0.72rem;
        padding: 4px 8px;
        flex-shrink: 0;
        border: 1.5px solid #000000;
        box-shadow: 1.5px 1.5px 0px #000000;
      }}

      /* RESPONSIVE CAR GRID */
      .grid-container {{
        width: 100%;
        height: auto !important;
        min-height: calc(100dvh - 140px);
        overflow: visible !important;
        padding: 12px 10px 48px 10px;
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        grid-template-rows: auto;
        gap: 10px;
        box-sizing: border-box;
      }}

      @media (min-width: 640px) {{
        .grid-container {{
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 12px;
        }}
      }}

      @media (min-width: 820px) {{
        .grid-container {{
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 12px;
        }}
      }}

      .card-wrap {{
        height: auto;
        aspect-ratio: 0.74;
        min-height: 220px;
        max-height: 280px;
        position: relative;
        width: 100%;
      }}

      .car-card {{
        border: 3px solid #000000;
        box-shadow: 3px 3px 0px #000000;
      }}

      .car-card:active {{
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #000000;
      }}

      .card-header {{
        height: 24px;
        min-height: 24px;
        font-size: 0.68rem;
        padding: 0 6px;
      }}

      .card-img-box {{
        padding: 6px;
        min-height: 110px;
      }}

      .card-img-box img {{
        max-width: 92%;
        max-height: 92%;
      }}

      .micro-badge {{
        top: 6px;
        right: 6px;
        font-size: 0.62rem;
        padding: 2px 5px;
        border: 1.5px solid #000000;
        box-shadow: 1.5px 1.5px 0px #000000;
      }}

      .card-info {{
        height: auto;
        min-height: 48px;
        padding: 5px 6px;
        border-top: 2px solid #000000;
      }}

      .car-title {{
        font-size: 0.78rem;
        font-weight: 800;
        white-space: normal;
        line-height: 1.15;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }}

      .car-meta {{
        font-size: 0.65rem;
        margin-top: 2px;
      }}
    }}

    /* MOBILE MODAL (< 768px) */
    @media (max-width: 768px) {{
      .morph-face-back {{
        border: 3px solid #000000;
        box-shadow: 6px 6px 0px #000000;
      }}

      .modal-topbar {{
        height: 44px;
        min-height: 44px;
        padding: 0 12px;
        border-bottom: 3px solid #000000;
      }}

      .modal-title-group {{
        font-size: 0.85rem;
        gap: 8px;
      }}

      .modal-close-btn {{
        width: 32px;
        height: 32px;
        min-width: 32px;
        font-size: 1.2rem;
      }}

      .modal-body {{
        display: flex;
        flex-direction: column;
        grid-template-columns: none;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        border-bottom: 3px solid #000000;
        flex: 1;
        min-height: 0;
      }}

      .modal-image-stage {{
        height: 190px;
        min-height: 180px;
        border-right: none;
        border-bottom: 3px solid #000000;
        padding: 10px;
        background: #ffffff;
        flex-shrink: 0;
      }}

      .modal-image-link img {{
        max-width: 90%;
        max-height: 90%;
        filter: drop-shadow(0 8px 14px rgba(0,0,0,0.22));
      }}

      .wiki-hint-pill {{
        bottom: 8px;
        font-size: 0.62rem;
        padding: 4px 10px;
      }}

      .modal-sidebar {{
        padding: 12px 14px;
        gap: 10px;
        height: auto;
        overflow-y: visible;
        flex: 1;
        justify-content: flex-start;
        background: #f8fafc;
      }}

      .spec-group {{
        gap: 8px;
      }}

      .spec-lbl {{
        font-size: 0.62rem;
      }}

      .spec-val {{
        font-size: 1rem;
        line-height: 1.2;
      }}

      .btn-fandom {{
        margin-top: 4px;
        padding: 8px 12px;
        font-size: 0.78rem;
        min-height: 40px;
      }}

      .modal-nav {{
        margin-top: 10px;
        gap: 8px;
      }}

      .btn-nav {{
        padding: 10px;
        font-size: 0.82rem;
        min-height: 42px;
      }}

      .modal-footer {{
        height: 30px;
        min-height: 30px;
        padding: 0 10px;
        font-size: 0.58rem;
      }}
    }}
  </style>
</head>
<body>

  <!-- RESPONSIVE HEADER WITH CASE SELECTOR AND STATS -->
  <header class="header-bar">
    <div class="header-top-row">
      <div class="brand-group">
        <div class="brand-title">
          <span>HOT WHEELS</span>
          <span style="color: var(--accent);">2026</span>
        </div>
      </div>
      
      <!-- MOBILE-ONLY ACTIONS -->
      <div class="header-actions mobile-only">
        <a href="hot_wheels_2026_case_a_poster.html" class="btn-action" id="link-poster-mobile">📄 Poster</a>
      </div>
    </div>

    <!-- 15 CASE SELECTOR (A TO Q) -->
    <div class="cases-nav-container">
      <div class="cases-nav" id="cases-nav">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- CURRENT CASE STATS -->
    <div class="stats-pills-container">
      <div class="stats-pills" id="stats-pills">
        <div class="pill" id="stat-count">-- Models</div>
        <div class="pill sth" id="stat-sth">★ $TH</div>
        <div class="pill th" id="stat-th">♨ TH</div>
        <div class="pill new" id="stat-new">★ NEW</div>
      </div>
    </div>

    <!-- DESKTOP ACTIONS -->
    <div class="header-actions desktop-only">
      <button class="btn-action" id="btn-layout" onclick="toggleLayout()">Grid: 9×3</button>
      <a href="hot_wheels_2026_case_a_poster.html" class="btn-action" id="link-poster" style="text-decoration: none;">📄 Printable Poster</a>
      <button class="btn-action" onclick="toggleFullscreen()" title="Fullscreen">⛶ Fullscreen</button>
    </div>
  </header>

  <!-- GRID VIEWPORT (ZERO SCROLLING) -->
  <main class="grid-container" id="grid-container">
    <!-- Cards dynamically populated by JavaScript -->
  </main>

  <!-- SHARED-ELEMENT 3D MORPHING CARD & BACKDROP -->
  <div class="morph-backdrop" id="morph-backdrop" onclick="closeMorphCard()"></div>
  <div class="morph-card" id="morph-card">
    <!-- FRONT FACE (Exact visual twin of the grid card during flight) -->
    <div class="morph-face morph-face-front" id="morph-front">
      <div class="card-header">
        <span class="card-col" id="mf-col">#001</span>
        <span class="card-toy" id="mf-toy">JJJ02</span>
      </div>
      <div class="card-img-box">
        <img id="mf-img" src="" alt="Thumbnail">
        <div id="mf-badge"></div>
      </div>
      <div class="card-info">
        <div class="car-title" id="mf-name">Model</div>
        <div class="car-meta">
          <span class="car-series" id="mf-series">Series</span>
          <span id="mf-subnum">1/5</span>
        </div>
      </div>
    </div>

    <!-- BACK FACE (Expanded, high-detail inspector card, upright at 180deg) -->
    <div class="morph-face morph-face-back" id="morph-back">
      <div class="modal-topbar">
        <div class="modal-title-group">
          <span class="modal-col-tag" id="mb-col">#001</span>
          <span id="mb-toy">JJJ02</span>
        </div>
        <button class="modal-close-btn" onclick="closeMorphCard()">✕</button>
      </div>
      <div class="modal-body">
        <!-- CLICKABLE IMAGE LINK -->
        <div class="modal-image-stage">
          <a id="mb-link" href="#" target="_blank" rel="noopener noreferrer" class="modal-image-link" title="Click to open this car on Hot Wheels Fandom Wiki">
            <img id="mb-img" src="" alt="Expanded View">
            <div class="wiki-hint-pill">🔗 OPEN FANDOM WIKI ↗</div>
          </a>
        </div>
        <div class="modal-sidebar">
          <div class="spec-group">
            <div class="spec-item">
              <span class="spec-lbl">Model Casting</span>
              <span class="spec-val" id="mb-name">Model Name</span>
            </div>
            <div class="spec-item">
              <span class="spec-lbl">Sub-Series</span>
              <span class="spec-val" id="mb-series" style="font-size: 0.95rem;">Series</span>
            </div>
            <div class="spec-item">
              <span class="spec-lbl">Series Number</span>
              <span class="spec-val" id="mb-subnum" style="font-size: 0.95rem;">1 of 5</span>
            </div>
            <div class="spec-item">
              <span class="spec-lbl">Edition Tier</span>
              <div class="spec-val badge-wrap" id="mb-badge">
                <!-- Tier Pill -->
              </div>
            </div>
            <div class="spec-item">
              <a id="mb-link-btn" href="#" target="_blank" rel="noopener noreferrer" class="btn-fandom">
                🌐 Fandom Wiki Page ↗
              </a>
            </div>
          </div>
          <div class="modal-nav">
            <button class="btn-nav" onclick="navigateMorph(-1)">◀ Prev</button>
            <button class="btn-nav" onclick="navigateMorph(1)">Next ▶</button>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <span>CLICK IMAGE TO OPEN FANDOM WIKI • <strong>ESC</strong> TO CLOSE</span>
        <span id="mb-case-label">ANTIGRAVITY 2026 CASE ENGINE</span>
      </div>
    </div>
  </div>

  <script>
    const casesData = {json_str};
    const caseLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q"];
    let currentCaseLetter = "A";
    let currentCaseCars = [];

    let activeIndex = -1;
    let activeCardEl = null;
    let isAnimating = false;

    // Render Navigation Pills
    const navEl = document.getElementById("cases-nav");
    caseLetters.forEach(letter => {{
      const btn = document.createElement("button");
      btn.className = "case-pill" + (letter === "A" ? " active" : "");
      btn.id = `pill-case-${{letter}}`;
      btn.textContent = letter;
      btn.title = `Switch to 2026 Mix ${{letter}}`;
      btn.onclick = () => selectCase(letter);
      navEl.appendChild(btn);
    }});

    function selectCase(letter) {{
      if (isAnimating) return;
      if (document.getElementById("morph-backdrop").classList.contains("active")) {{
        closeMorphCard();
      }}

      currentCaseLetter = letter;
      const cData = casesData[letter];
      if (!cData) return;

      // Update active nav button and scroll pill into view
      document.querySelectorAll(".case-pill").forEach(p => p.classList.remove("active"));
      const activePill = document.getElementById(`pill-case-${{letter}}`);
      if (activePill) {{
        activePill.classList.add("active");
        activePill.scrollIntoView({{ behavior: "smooth", inline: "center", block: "nearest" }});
      }}

      // Scroll page to top on mobile/tablet when switching case
      if (window.innerWidth <= 1024) {{
        window.scrollTo({{ top: 0, behavior: "smooth" }});
      }}

      // Update header stats
      document.getElementById("stat-count").innerHTML = `<strong>${{cData.total_count}}</strong> Models`;
      document.getElementById("stat-sth").innerHTML = `★ $TH: ${{cData.sth_name}}`;
      document.getElementById("stat-th").innerHTML = `♨ TH: ${{cData.th_name}}`;
      document.getElementById("stat-new").innerHTML = `★ ${{cData.new_count}} New`;
      document.getElementById("mb-case-label").textContent = `2026 MIX ${{letter}} • 72-COUNT CASE ASSORTMENT`;

      currentCaseCars = cData.cars;
      renderGrid(currentCaseCars);
    }}

    function renderGrid(cars) {{
      const grid = document.getElementById("grid-container");
      grid.innerHTML = "";

      cars.forEach((car, index) => {{
        const wrap = document.createElement("div");
        wrap.className = "card-wrap";

        const card = document.createElement("div");
        card.className = "car-card" + (car.is_sth ? " is-sth" : (car.is_th ? " is-th" : ""));
        card.id = `card-${{index}}`;

        let badgeHtml = "";
        if (car.is_sth) {{
          badgeHtml = '<span class="micro-badge sth">★ $TH</span>';
        }} else if (car.is_th) {{
          badgeHtml = '<span class="micro-badge th">♨ TH</span>';
        }} else if (car.is_new) {{
          badgeHtml = '<span class="micro-badge new">★ NEW</span>';
        }} else if (car.is_recolor) {{
          badgeHtml = '<span class="micro-badge recolor">2ND COLOR</span>';
        }}

        const carImg = car.local_img || car.img;
        card.innerHTML = `
          <div class="card-header">
            <span class="card-col">#${{car.col}}</span>
            <span class="card-toy">${{car.toy}}</span>
          </div>
          <div class="card-img-box">
            <img src="${{carImg}}" alt="${{car.name}}" loading="lazy" onerror="if(this.src!=='${{car.img}}'){{this.src='${{car.img}}';}}else{{this.onerror=null;this.src='https://placehold.co/240x140/000/fff?text=${{encodeURIComponent(car.name)}}';}}">
            ${{badgeHtml}}
          </div>
          <div class="card-info">
            <div class="car-title">${{car.name}}</div>
            <div class="car-meta">
              <span class="car-series">${{car.series}}</span>
              <span>${{car.sub_num}}</span>
            </div>
          </div>
        `;

        card.addEventListener("click", () => {{
          openMorphCard(index, card);
        }});

        wrap.appendChild(card);
        grid.appendChild(wrap);
      }});
    }}

    function updateFrontFace(car) {{
      const carImg = car.local_img || car.img;
      document.getElementById("mf-col").textContent = `#${{car.col}}`;
      document.getElementById("mf-toy").textContent = car.toy;
      document.getElementById("mf-img").src = carImg;
      document.getElementById("mf-name").textContent = car.name;
      document.getElementById("mf-series").textContent = car.series;
      document.getElementById("mf-subnum").textContent = car.sub_num;

      const bBox = document.getElementById("mf-badge");
      if (car.is_sth) {{
        bBox.innerHTML = '<span class="micro-badge sth">★ $TH</span>';
      }} else if (car.is_th) {{
        bBox.innerHTML = '<span class="micro-badge th">♨ TH</span>';
      }} else if (car.is_new) {{
        bBox.innerHTML = '<span class="micro-badge new">★ NEW</span>';
      }} else if (car.is_recolor) {{
        bBox.innerHTML = '<span class="micro-badge recolor">2ND COLOR</span>';
      }} else {{
        bBox.innerHTML = '';
      }}
    }}

    function updateBackFace(car) {{
      const carImg = car.local_img || car.img;
      document.getElementById("mb-col").textContent = `#${{car.col}}`;
      document.getElementById("mb-toy").textContent = car.toy;
      document.getElementById("mb-name").textContent = car.name;
      document.getElementById("mb-series").textContent = car.series;
      document.getElementById("mb-subnum").textContent = `${{car.sub_num}} in sub-series`;
      document.getElementById("mb-img").src = carImg;

      // Clickable image link & sidebar button to Hot Wheels Fandom Wiki
      const wikiTarget = car.wiki_url || "https://hotwheels.fandom.com/wiki/List_of_2026_Hot_Wheels";
      document.getElementById("mb-link").href = wikiTarget;
      document.getElementById("mb-link-btn").href = wikiTarget;

      const bBox = document.getElementById("mb-badge");
      if (car.is_sth) {{
        bBox.innerHTML = '<span class="pill sth">★ SUPER TREASURE HUNT ($TH)</span>';
      }} else if (car.is_th) {{
        bBox.innerHTML = '<span class="pill th">♨ REGULAR TREASURE HUNT (TH)</span>';
      }} else if (car.is_new) {{
        bBox.innerHTML = '<span class="pill new">★ NEW CASTING FOR 2026</span>';
      }} else if (car.is_recolor) {{
        bBox.innerHTML = '<span class="pill recolor">RECOLOR VARIATION</span>';
      }} else {{
        bBox.innerHTML = '<span class="pill">STANDARD MAINLINE</span>';
      }}
    }}

    function openMorphCard(index, cardEl) {{
      if (isAnimating) return;
      isAnimating = true;
      activeIndex = index;
      activeCardEl = cardEl;

      document.body.classList.add("modal-open");

      const car = currentCaseCars[index];
      updateFrontFace(car);
      updateBackFace(car);

      const rect = cardEl.getBoundingClientRect();
      const morphCard = document.getElementById("morph-card");
      const backdrop = document.getElementById("morph-backdrop");

      morphCard.style.transition = "none";
      morphCard.style.left = rect.left + "px";
      morphCard.style.top = rect.top + "px";
      morphCard.style.width = rect.width + "px";
      morphCard.style.height = rect.height + "px";
      morphCard.style.transform = "perspective(1400px) rotateY(0deg)";
      morphCard.style.display = "block";

      cardEl.style.opacity = "0";
      if (cardEl.parentElement) {{
        cardEl.parentElement.style.outline = "2px dashed #9ca3af";
        cardEl.parentElement.style.outlineOffset = "-2px";
      }}

      void morphCard.offsetWidth;

      const isMobile = window.innerWidth <= 768;
      const targetW = isMobile ? Math.min(window.innerWidth - 16, 440) : Math.min(window.innerWidth * 0.74, 760);
      const targetH = isMobile ? Math.min(window.innerHeight - 24, 620) : Math.min(window.innerHeight * 0.78, 500);
      const targetL = (window.innerWidth - targetW) / 2;
      const targetT = (window.innerHeight - targetH) / 2;

      backdrop.classList.add("active");
      morphCard.style.transition = "top 0.48s cubic-bezier(0.16, 1, 0.3, 1), left 0.48s cubic-bezier(0.16, 1, 0.3, 1), width 0.48s cubic-bezier(0.16, 1, 0.3, 1), height 0.48s cubic-bezier(0.16, 1, 0.3, 1), transform 0.48s cubic-bezier(0.16, 1, 0.3, 1)";
      morphCard.style.left = targetL + "px";
      morphCard.style.top = targetT + "px";
      morphCard.style.width = targetW + "px";
      morphCard.style.height = targetH + "px";
      morphCard.style.transform = "perspective(1400px) rotateY(180deg)";

      setTimeout(() => {{
        isAnimating = false;
      }}, 500);
    }}

    function closeMorphCard() {{
      if (isAnimating || activeIndex === -1) return;
      isAnimating = true;

      document.body.classList.remove("modal-open");

      const targetCardEl = document.getElementById(`card-${{activeIndex}}`);
      if (targetCardEl) {{
        const r = targetCardEl.getBoundingClientRect();
        const inView = r.top >= 0 && r.bottom <= window.innerHeight;
        if (!inView) {{
          targetCardEl.scrollIntoView({{ block: "center" }});
        }}
      }}

      const rect = targetCardEl ? targetCardEl.getBoundingClientRect() : null;
      const morphCard = document.getElementById("morph-card");
      const backdrop = document.getElementById("morph-backdrop");

      backdrop.classList.remove("active");

      if (rect) {{
        updateFrontFace(currentCaseCars[activeIndex]);

        morphCard.style.transition = "top 0.42s cubic-bezier(0.2, 0.8, 0.2, 1), left 0.42s cubic-bezier(0.2, 0.8, 0.2, 1), width 0.42s cubic-bezier(0.2, 0.8, 0.2, 1), height 0.42s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.42s cubic-bezier(0.2, 0.8, 0.2, 1)";
        morphCard.style.left = rect.left + "px";
        morphCard.style.top = rect.top + "px";
        morphCard.style.width = rect.width + "px";
        morphCard.style.height = rect.height + "px";
        morphCard.style.transform = "perspective(1400px) rotateY(0deg)";

        setTimeout(() => {{
          morphCard.style.display = "none";
          if (targetCardEl) {{
            targetCardEl.style.opacity = "1";
            if (targetCardEl.parentElement) targetCardEl.parentElement.style.outline = "none";
          }}
          if (activeCardEl && activeCardEl !== targetCardEl) {{
            activeCardEl.style.opacity = "1";
            if (activeCardEl.parentElement) activeCardEl.parentElement.style.outline = "none";
          }}
          activeCardEl = null;
          activeIndex = -1;
          isAnimating = false;
        }}, 430);
      }} else {{
        morphCard.style.display = "none";
        if (activeCardEl) activeCardEl.style.opacity = "1";
        isAnimating = false;
      }}
    }}

    function navigateMorph(direction) {{
      if (isAnimating || activeIndex === -1) return;
      isAnimating = true;

      const prevCard = document.getElementById(`card-${{activeIndex}}`);
      if (prevCard) {{
        prevCard.style.opacity = "1";
        if (prevCard.parentElement) {{
          prevCard.parentElement.style.outline = "none";
        }}
      }}

      activeIndex = (activeIndex + direction + currentCaseCars.length) % currentCaseCars.length;
      
      const newCard = document.getElementById(`card-${{activeIndex}}`);
      if (newCard) {{
        newCard.style.opacity = "0";
        if (newCard.parentElement) {{
          newCard.parentElement.style.outline = "2px dashed #9ca3af";
          newCard.parentElement.style.outlineOffset = "-2px";
        }}
      }}

      const morphCard = document.getElementById("morph-card");
      morphCard.style.transition = "transform 0.22s ease-in";
      morphCard.style.transform = "perspective(1400px) rotateY(270deg)";

      setTimeout(() => {{
        updateBackFace(currentCaseCars[activeIndex]);
        updateFrontFace(currentCaseCars[activeIndex]);
        morphCard.style.transition = "transform 0.22s ease-out";
        morphCard.style.transform = "perspective(1400px) rotateY(180deg)";
        setTimeout(() => {{
          isAnimating = false;
        }}, 230);
      }}, 220);
    }}

    // Touch swipe gesture navigation on mobile for morph card
    let touchStartX = 0;
    let touchStartY = 0;

    const morphCardEl = document.getElementById("morph-card");
    morphCardEl.addEventListener("touchstart", (e) => {{
      if (e.touches.length === 1) {{
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }}
    }}, {{ passive: true }});

    morphCardEl.addEventListener("touchend", (e) => {{
      if (e.changedTouches.length === 1) {{
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const diffX = touchEndX - touchStartX;
        const diffY = touchEndY - touchStartY;
        const absX = Math.abs(diffX);
        const absY = Math.abs(diffY);

        if (absX > 45 && absX > absY * 1.5) {{
          if (diffX < 0) {{
            navigateMorph(1); // Swipe left -> Next
          }} else {{
            navigateMorph(-1); // Swipe right -> Prev
          }}
        }} else if (diffY > 80 && absY > absX * 1.5) {{
          closeMorphCard(); // Swipe down -> Close
        }}
      }}
    }}, {{ passive: true }});

    document.addEventListener("keydown", (e) => {{
      const backdrop = document.getElementById("morph-backdrop");
      if (!backdrop.classList.contains("active")) return;

      if (e.key === "Escape") {{
        closeMorphCard();
      }} else if (e.key === "ArrowLeft") {{
        navigateMorph(-1);
      }} else if (e.key === "ArrowRight") {{
        navigateMorph(1);
      }}
    }});

    function toggleLayout() {{
      const grid = document.getElementById("grid-container");
      const btn = document.getElementById("btn-layout");
      grid.classList.toggle("layout-7x4");
      if (grid.classList.contains("layout-7x4")) {{
        btn.textContent = "Grid: 7×4";
      }} else {{
        btn.textContent = "Grid: 9×3";
      }}
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }}

    selectCase("A");
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Successfully generated index.html with Fandom Wiki hyperlinks embedded!")
