def generate_bioreactor_svg(volume: float, rpm: float, do: float, is_running: bool) -> str:
    """Génère le document HTML/SVG complet avec baie vitrée 3D et vagues animées."""
    
    max_height = 160
    h_liquid = min(max_height, max(4, int((volume / 5.0) * max_height)))
    y_liquid = 240 - h_liquid
    
    liquid_color_base = "#2563eb" if do > 30 else "#dc2626"
    liquid_color_top = "#60a5fa" if do > 30 else "#f87171"

    wave_duration = max(1.2, 4.0 - (rpm / 200.0)) if is_running else 6.0
    prop_duration = max(0.15, 2.0 - (rpm / 400.0)) if is_running and rpm > 0 else 0.0

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; padding: 0; background-color: transparent; overflow: hidden; }}
    @keyframes waveMotion {{
        0% {{ transform: translateX(0px); }}
        50% {{ transform: translateX(-30px); }}
        100% {{ transform: translateX(0px); }}
    }}
    @keyframes spinPropeller {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    .liquid-body {{
        transition: y 0.8s ease-in-out, height 0.8s ease-in-out, fill 0.8s ease;
    }}
    .wave-front {{
        animation: waveMotion {wave_duration:.2f}s ease-in-out infinite;
        transition: d 0.8s ease-in-out, fill 0.8s ease;
    }}
    .propeller-blade {{
        transform-origin: 150px 205px;
        animation: {'spinPropeller ' + str(round(prop_duration, 2)) + 's linear infinite' if prop_duration > 0 else 'none'};
    }}
</style>
</head>
<body>
<svg width="100%" height="295" viewBox="0 0 300 310" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: auto;">
    <defs>
        <linearGradient id="metalGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#334155"/>
            <stop offset="25%" stop-color="#94a3b8"/>
            <stop offset="50%" stop-color="#cbd5e1"/>
            <stop offset="75%" stop-color="#64748b"/>
            <stop offset="100%" stop-color="#1e293b"/>
        </linearGradient>

        <linearGradient id="glassReflection" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.45"/>
            <stop offset="15%" stop-color="#ffffff" stop-opacity="0.10"/>
            <stop offset="50%" stop-color="#ffffff" stop-opacity="0.02"/>
            <stop offset="85%" stop-color="#38bdf8" stop-opacity="0.15"/>
            <stop offset="100%" stop-color="#ffffff" stop-opacity="0.40"/>
        </linearGradient>

        <linearGradient id="liquidGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{liquid_color_base}" stop-opacity="0.85"/>
            <stop offset="50%" stop-color="{liquid_color_top}" stop-opacity="0.65"/>
            <stop offset="100%" stop-color="{liquid_color_base}" stop-opacity="0.90"/>
        </linearGradient>

        <radialGradient id="dropShadow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#000000" stop-opacity="0.5"/>
            <stop offset="100%" stop-color="#000000" stop-opacity="0.0"/>
        </radialGradient>
    </defs>

    <!-- Ombre sol -->
    <ellipse cx="150" cy="285" rx="90" ry="14" fill="url(#dropShadow)" />

    <!-- Socle Métallique 3D -->
    <ellipse cx="150" cy="265" rx="90" ry="20" fill="url(#metalGrad)" stroke="#0f172a" stroke-width="2"/>
    <path d="M 60 245 L 60 265 A 90 20 0 0 0 240 265 L 240 245 Z" fill="url(#metalGrad)" stroke="#0f172a" stroke-width="1"/>
    <ellipse cx="150" cy="245" rx="80" ry="18" fill="#1e293b" stroke="#475569" stroke-width="1"/>

    <!-- Liquide & Vague sinusoïdale -->
    <g id="liquid-group">
        <ellipse cx="150" cy="245" rx="78" ry="17" fill="{liquid_color_base}" opacity="0.85"/>
        <rect class="liquid-body" x="72" y="{y_liquid}" width="156" height="{h_liquid}" fill="url(#liquidGrad)"/>
        <g class="wave-front">
            <path d="M 40 {y_liquid} Q 75 {y_liquid - 5}, 110 {y_liquid} T 180 {y_liquid} T 260 {y_liquid} L 260 {y_liquid + 12} L 40 {y_liquid + 12} Z" fill="{liquid_color_top}" opacity="0.95"/>
        </g>
    </g>

    <!-- Graduations verre -->
    <g stroke="#cbd5e1" stroke-width="1" opacity="0.7">
        <line x1="74" y1="208" x2="86" y2="208"/><text x="90" y="211" fill="#cbd5e1" font-size="9" font-family="sans-serif">1L</text>
        <line x1="74" y1="176" x2="86" y2="176"/><text x="90" y="179" fill="#cbd5e1" font-size="9" font-family="sans-serif">2L</text>
        <line x1="74" y1="144" x2="86" y2="144"/><text x="90" y="147" fill="#cbd5e1" font-size="9" font-family="sans-serif">3L</text>
        <line x1="74" y1="112" x2="86" y2="112"/><text x="90" y="115" fill="#cbd5e1" font-size="9" font-family="sans-serif">4L</text>
        <line x1="74" y1="80" x2="86" y2="80"/><text x="90" y="83" fill="#cbd5e1" font-size="9" font-family="sans-serif">5L</text>
    </g>

    <!-- Arbre & Pales agitation -->
    <rect x="147" y="25" width="6" height="205" fill="url(#metalGrad)"/>
    <g class="propeller-blade">
        <ellipse cx="150" cy="205" rx="42" ry="9" fill="#475569" stroke="#0f172a" stroke-width="1.5"/>
        <rect x="110" y="200" width="14" height="10" rx="2" fill="url(#metalGrad)"/>
        <rect x="176" y="200" width="14" height="10" rx="2" fill="url(#metalGrad)"/>
        <ellipse cx="150" cy="205" rx="10" ry="3.5" fill="#94a3b8"/>
    </g>

    <!-- Sonde et Tuyau -->
    <rect x="195" y="45" width="5" height="145" rx="2.5" fill="#f59e0b" opacity="0.9"/>
    <circle cx="197.5" cy="190" r="6" fill="#fbbf24" stroke="#d97706" stroke-width="1.5"/>
    <path d="M 100 25 L 100 70 L 115 70" fill="none" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>

    <!-- === CYLINDRE EN VERRE 3D (BAIE VITRÉE) === -->
    <rect x="70" y="65" width="160" height="180" fill="url(#glassReflection)" stroke="#cbd5e1" stroke-width="2" opacity="0.85"/>
    <ellipse cx="150" cy="65" rx="80" ry="18" fill="url(#glassReflection)" stroke="#ffffff" stroke-width="1.5" opacity="0.9"/>
    <ellipse cx="150" cy="245" rx="80" ry="18" fill="none" stroke="#cbd5e1" stroke-width="1.5" opacity="0.6"/>
    <line x1="78" y1="65" x2="78" y2="245" stroke="#ffffff" stroke-width="3" opacity="0.4"/>
    <line x1="222" y1="65" x2="222" y2="245" stroke="#38bdf8" stroke-width="2" opacity="0.3"/>

    <!-- Couvercle métallique -->
    <ellipse cx="150" cy="60" rx="88" ry="19" fill="url(#metalGrad)" stroke="#0f172a" stroke-width="2"/>
    <rect x="122" y="15" width="56" height="35" rx="5" fill="url(#metalGrad)" stroke="#0f172a" stroke-width="2"/>
    <text x="150" y="36" fill="#f8fafc" font-size="10" text-anchor="middle" font-family="sans-serif" font-weight="bold">MOTEUR</text>

    <!-- Texte état -->
    <text x="150" y="303" fill="#cbd5e1" font-size="12" text-anchor="middle" font-family="sans-serif" font-weight="600">
        Volume: {volume:.2f} L  |  RPM: {int(rpm)}
    </text>
</svg>
</body>
</html>"""
    return html_content
