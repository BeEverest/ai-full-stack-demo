<template>
  <div class="w-full h-full">

    <!-- ══════════════════════════════════════
         VISION G1 — AI 眼镜
         ══════════════════════════════════════ -->
    <svg v-if="slug === 'ai-glasses'"
      viewBox="0 0 320 200" fill="none" xmlns="http://www.w3.org/2000/svg"
      class="w-full h-full" preserveAspectRatio="xMidYMid meet">
      <defs>
        <filter id="g-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="2.5" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <clipPath id="g-left-clip">
          <rect x="22" y="62" width="119" height="71" rx="12"/>
        </clipPath>
        <clipPath id="g-right-clip">
          <rect x="179" y="62" width="119" height="71" rx="12"/>
        </clipPath>
        <linearGradient id="g-lens-bg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0A1020"/>
          <stop offset="100%" stop-color="#050810"/>
        </linearGradient>
      </defs>

      <!-- HUD corner brackets -->
      <path d="M16 38 L16 26 L28 26" stroke="#2D8FE8" stroke-width="1.2" opacity="0.5"/>
      <path d="M304 38 L304 26 L292 26" stroke="#2D8FE8" stroke-width="1.2" opacity="0.5"/>
      <path d="M16 162 L16 174 L28 174" stroke="#2D8FE8" stroke-width="1.2" opacity="0.5"/>
      <path d="M304 162 L304 174 L292 174" stroke="#2D8FE8" stroke-width="1.2" opacity="0.5"/>

      <!-- Temple arms (left / right) -->
      <path d="M22 78 C12 78 6 84 4 96" stroke="#4A5568" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M298 78 C308 78 314 84 316 96" stroke="#4A5568" stroke-width="1.5" stroke-linecap="round"/>

      <!-- ── Left lens ── -->
      <rect x="22" y="62" width="119" height="71" rx="14"
        stroke="#4DAAFF" stroke-width="1.5" fill="url(#g-lens-bg)" filter="url(#g-glow)"/>
      <!-- inner grid (clipped) -->
      <g clip-path="url(#g-left-clip)" opacity="0.35">
        <line x1="47"  y1="62" x2="47"  y2="133" stroke="#2D8FE8" stroke-width="0.5"/>
        <line x1="72"  y1="62" x2="72"  y2="133" stroke="#2D8FE8" stroke-width="0.5"/>
        <line x1="97"  y1="62" x2="97"  y2="133" stroke="#2D8FE8" stroke-width="0.5"/>
        <line x1="122" y1="62" x2="122" y2="133" stroke="#2D8FE8" stroke-width="0.5"/>
        <line x1="22"  y1="80" x2="141" y2="80"  stroke="#2D8FE8" stroke-width="0.5"/>
        <line x1="22"  y1="97" x2="141" y2="97"  stroke="#2D8FE8" stroke-width="0.5"/>
        <line x1="22"  y1="114" x2="141" y2="114" stroke="#2D8FE8" stroke-width="0.5"/>
      </g>
      <!-- scan line (clipped so it stays inside lens) -->
      <g clip-path="url(#g-left-clip)">
        <line x1="22" y1="62" x2="141" y2="62" stroke="#4DAAFF" stroke-width="1.2" opacity="0.85">
          <animateTransform attributeName="transform" type="translate"
            values="0 0;0 71;0 0" dur="2.8s" repeatCount="indefinite"
            calcMode="ease-in-out"/>
          <animate attributeName="opacity" values="0.85;0.3;0.85" dur="2.8s" repeatCount="indefinite"/>
        </line>
      </g>
      <!-- active dot top-right of left lens -->
      <circle cx="131" cy="72" r="3" fill="#4DAAFF">
        <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>

      <!-- ── Bridge ── -->
      <rect x="141" y="89" width="38" height="20" rx="5"
        stroke="#2D8FE8" stroke-width="1" fill="#080C12"/>
      <circle cx="160" cy="99" r="3.5" fill="#2D8FE8" opacity="0.7">
        <animate attributeName="opacity" values="0.7;1;0.7" dur="2.2s" repeatCount="indefinite"/>
      </circle>
      <line x1="148" y1="99" x2="156" y2="99" stroke="#1E6FBA" stroke-width="1" opacity="0.6"/>
      <line x1="164" y1="99" x2="172" y2="99" stroke="#1E6FBA" stroke-width="1" opacity="0.6"/>

      <!-- ── Right lens ── -->
      <rect x="179" y="62" width="119" height="71" rx="14"
        stroke="#4DAAFF" stroke-width="1.5" fill="url(#g-lens-bg)" filter="url(#g-glow)"/>
      <!-- neural nodes -->
      <g clip-path="url(#g-right-clip)">
        <!-- connection lines -->
        <line x1="205" y1="82" x2="244" y2="74" stroke="#2D8FE8" stroke-width="0.75" opacity="0.45"/>
        <line x1="244" y1="74" x2="275" y2="90" stroke="#2D8FE8" stroke-width="0.75" opacity="0.45"/>
        <line x1="205" y1="82" x2="228" y2="108" stroke="#2D8FE8" stroke-width="0.75" opacity="0.45"/>
        <line x1="275" y1="90" x2="258" y2="117" stroke="#2D8FE8" stroke-width="0.75" opacity="0.45"/>
        <line x1="228" y1="108" x2="193" y2="115" stroke="#2D8FE8" stroke-width="0.75" opacity="0.45"/>
        <line x1="228" y1="108" x2="258" y2="117" stroke="#2D8FE8" stroke-width="0.75" opacity="0.45"/>
        <line x1="275" y1="90" x2="291" y2="106" stroke="#2D8FE8" stroke-width="0.75" opacity="0.45"/>
        <!-- node dots -->
        <circle cx="205" cy="82"  r="2.5" fill="#4DAAFF" opacity="0.8"/>
        <circle cx="244" cy="74"  r="2.5" fill="#4DAAFF" opacity="0.6"/>
        <circle cx="275" cy="90"  r="2.5" fill="#4DAAFF" opacity="0.8"/>
        <circle cx="228" cy="108" r="2.5" fill="#4DAAFF" opacity="0.7"/>
        <circle cx="258" cy="117" r="2"   fill="#4DAAFF" opacity="0.6"/>
        <circle cx="193" cy="115" r="2"   fill="#4DAAFF" opacity="0.6"/>
        <circle cx="291" cy="106" r="2"   fill="#4DAAFF" opacity="0.5"/>
        <!-- pulse ring on one node -->
        <circle cx="244" cy="74" r="6" fill="none" stroke="#4DAAFF" stroke-width="0.75">
          <animate attributeName="r"       values="4;9;4"     dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.6;0;0.6" dur="2.2s" repeatCount="indefinite"/>
        </circle>
      </g>
      <!-- active dot -->
      <circle cx="189" cy="72" r="3" fill="#4DAAFF">
        <animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite" begin="0.8s"/>
      </circle>

      <!-- serial labels -->
      <text x="81"  y="153" text-anchor="middle" fill="#2D4A6A" font-family="monospace" font-size="7.5" letter-spacing="1.5">AR · VISION G1</text>
      <text x="238" y="153" text-anchor="middle" fill="#2D4A6A" font-family="monospace" font-size="7.5" letter-spacing="1.5">NEURAL LENS</text>
    </svg>

    <!-- ══════════════════════════════════════
         NEXUS R2 — AI 机器人
         ══════════════════════════════════════ -->
    <svg v-else-if="slug === 'ai-robot'"
      viewBox="0 0 280 300" fill="none" xmlns="http://www.w3.org/2000/svg"
      class="w-full h-full" preserveAspectRatio="xMidYMid meet">
      <defs>
        <filter id="r-glow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="4" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <clipPath id="r-eye-clip">
          <circle cx="140" cy="80" r="27"/>
        </clipPath>
      </defs>

      <!-- corner marks -->
      <path d="M12 44 L12 24 L32 24" stroke="#1E2D40" stroke-width="1"/>
      <path d="M268 44 L268 24 L248 24" stroke="#1E2D40" stroke-width="1"/>
      <path d="M12 256 L12 276 L32 276" stroke="#1E2D40" stroke-width="1"/>
      <path d="M268 256 L268 276 L248 276" stroke="#1E2D40" stroke-width="1"/>

      <!-- ── Shoulders ── -->
      <rect x="28" y="170" width="36" height="72" rx="10"
        stroke="#1E2D40" stroke-width="1.5" fill="#0A0E16"/>
      <rect x="216" y="170" width="36" height="72" rx="10"
        stroke="#1E2D40" stroke-width="1.5" fill="#0A0E16"/>
      <!-- shoulder panel lines -->
      <line x1="28" y1="196" x2="64"  y2="196" stroke="#141C28" stroke-width="1"/>
      <line x1="216" y1="196" x2="252" y2="196" stroke="#141C28" stroke-width="1"/>
      <!-- arm joints -->
      <circle cx="46"  cy="170" r="10" fill="#080C12" stroke="#2D8FE8" stroke-width="1.2"/>
      <circle cx="234" cy="170" r="10" fill="#080C12" stroke="#2D8FE8" stroke-width="1.2"/>
      <circle cx="46"  cy="170" r="4"  fill="#1E6FBA" opacity="0.6"/>
      <circle cx="234" cy="170" r="4"  fill="#1E6FBA" opacity="0.6"/>

      <!-- ── Torso ── -->
      <rect x="64" y="162" width="152" height="110" rx="14"
        stroke="#1E2D40" stroke-width="1.5" fill="#0A0E16"/>
      <!-- torso panel dividers -->
      <line x1="64"  y1="195" x2="216" y2="195" stroke="#141C28" stroke-width="1"/>
      <line x1="64"  y1="232" x2="216" y2="232" stroke="#141C28" stroke-width="1"/>
      <!-- status LED bar -->
      <rect x="84"  y="175" width="112" height="6" rx="3" fill="#0D1117"/>
      <rect x="84"  y="175" width="80"  height="6" rx="3" fill="#2D8FE8" opacity="0.75">
        <animate attributeName="width" values="80;102;80" dur="3.5s" repeatCount="indefinite"/>
      </rect>
      <!-- chest data panels -->
      <rect x="80"  y="205" width="54" height="16" rx="3" stroke="#1E2D40" stroke-width="1" fill="none"/>
      <rect x="146" y="205" width="54" height="16" rx="3" stroke="#1E2D40" stroke-width="1" fill="none"/>
      <text x="107" y="217" text-anchor="middle" fill="#2D4A6A" font-family="monospace" font-size="6.5">7B LLM</text>
      <text x="173" y="217" text-anchor="middle" fill="#2D4A6A" font-family="monospace" font-size="6.5">SLAM</text>
      <!-- lower panel micro-lines -->
      <line x1="84"  y1="243" x2="130" y2="243" stroke="#1A3A5C" stroke-width="1" opacity="0.6"/>
      <line x1="84"  y1="249" x2="110" y2="249" stroke="#1A3A5C" stroke-width="1" opacity="0.4"/>
      <line x1="150" y1="243" x2="196" y2="243" stroke="#1A3A5C" stroke-width="1" opacity="0.6"/>
      <line x1="164" y1="249" x2="196" y2="249" stroke="#1A3A5C" stroke-width="1" opacity="0.4"/>

      <!-- ── Neck ── -->
      <rect x="116" y="148" width="48" height="20" rx="5"
        stroke="#1E2D40" stroke-width="1" fill="#0A0E16"/>
      <line x1="116" y1="156" x2="164" y2="156" stroke="#141C28" stroke-width="1"/>

      <!-- ── Head ── -->
      <rect x="72" y="38" width="136" height="114" rx="20"
        stroke="#4DAAFF" stroke-width="1.5" fill="#0A0E16" filter="url(#r-glow)"/>
      <!-- head panel line -->
      <line x1="72"  y1="118" x2="208" y2="118" stroke="#141C28" stroke-width="1"/>
      <line x1="72"  y1="96"  x2="208" y2="96"  stroke="#141C28" stroke-width="0.5" opacity="0.4"/>

      <!-- ── Eye / Radar ── -->
      <!-- outer ring -->
      <circle cx="140" cy="80" r="30" stroke="#2D8FE8" stroke-width="1.5" fill="#080C12"/>
      <!-- mid ring -->
      <circle cx="140" cy="80" r="22" stroke="#1E2D40" stroke-width="0.75" fill="none"/>
      <!-- inner ring -->
      <circle cx="140" cy="80" r="14" stroke="#1E2D40" stroke-width="0.75" fill="none"/>
      <!-- range tick marks -->
      <g opacity="0.3" stroke="#2D8FE8" stroke-width="0.75">
        <line x1="140" y1="50" x2="140" y2="53"/>
        <line x1="140" y1="107" x2="140" y2="110"/>
        <line x1="110" y1="80" x2="113" y2="80"/>
        <line x1="167" y1="80" x2="170" y2="80"/>
      </g>
      <!-- radar sweep (clipped to eye circle) -->
      <g clip-path="url(#r-eye-clip)">
        <line x1="140" y1="80" x2="140" y2="50" stroke="#4DAAFF" stroke-width="1.5" stroke-linecap="round">
          <animateTransform attributeName="transform" type="rotate"
            from="0 140 80" to="360 140 80" dur="3s" repeatCount="indefinite"/>
        </line>
        <path d="M140 80 L140 50 A30 30 0 0 1 168 92 Z" fill="#4DAAFF" fill-opacity="0.06">
          <animateTransform attributeName="transform" type="rotate"
            from="0 140 80" to="360 140 80" dur="3s" repeatCount="indefinite"/>
        </path>
      </g>
      <!-- center pupil -->
      <circle cx="140" cy="80" r="6" fill="#4DAAFF" opacity="0.9">
        <animate attributeName="opacity" values="0.9;0.4;0.9" dur="2s" repeatCount="indefinite"/>
      </circle>
      <!-- pupil specular -->
      <circle cx="143" cy="77" r="2" fill="white" opacity="0.35"/>

      <!-- side sensor dots -->
      <circle cx="86"  cy="128" r="5" fill="#080C12" stroke="#2D8FE8" stroke-width="1"/>
      <circle cx="194" cy="128" r="5" fill="#080C12" stroke="#2D8FE8" stroke-width="1"/>
      <circle cx="86"  cy="128" r="2" fill="#4DAAFF">
        <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <circle cx="194" cy="128" r="2" fill="#4DAAFF">
        <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" begin="0.9s" repeatCount="indefinite"/>
      </circle>

      <!-- head status text -->
      <text x="98"  y="138" fill="#2D4A6A" font-family="monospace" font-size="6.5">NEXUS R2</text>
      <text x="164" y="138" fill="#2D4A6A" font-family="monospace" font-size="6.5">ONLINE</text>

      <!-- antenna -->
      <line x1="140" y1="38" x2="140" y2="22" stroke="#2D8FE8" stroke-width="1.5" stroke-linecap="round"/>
      <circle cx="140" cy="19" r="3.5" fill="#4DAAFF">
        <animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/>
      </circle>
      <circle cx="140" cy="19" r="7" fill="none" stroke="#4DAAFF" stroke-width="0.75">
        <animate attributeName="r"       values="5;12;5"   dur="1.2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.6;0;0.6" dur="1.2s" repeatCount="indefinite"/>
      </circle>
    </svg>

    <!-- ══════════════════════════════════════
         MOCHI A1 — AI 玩具
         ══════════════════════════════════════ -->
    <svg v-else
      viewBox="0 0 280 300" fill="none" xmlns="http://www.w3.org/2000/svg"
      class="w-full h-full" preserveAspectRatio="xMidYMid meet">
      <defs>
        <filter id="t-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="5" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <radialGradient id="t-body-glow" cx="50%" cy="45%" r="50%">
          <stop offset="0%"   stop-color="#1A3A5C" stop-opacity="0.25"/>
          <stop offset="100%" stop-color="#080C12" stop-opacity="0"/>
        </radialGradient>
        <clipPath id="t-face-clip">
          <rect x="76" y="80" width="128" height="100" rx="18"/>
        </clipPath>
      </defs>

      <!-- corner marks -->
      <path d="M12 44 L12 24 L32 24" stroke="#1E2D40" stroke-width="1" opacity="0.5"/>
      <path d="M268 44 L268 24 L248 24" stroke="#1E2D40" stroke-width="1" opacity="0.5"/>
      <path d="M12 256 L12 276 L32 276" stroke="#1E2D40" stroke-width="1" opacity="0.5"/>
      <path d="M268 256 L268 276 L248 276" stroke="#1E2D40" stroke-width="1" opacity="0.5"/>

      <!-- ambient glow -->
      <ellipse cx="140" cy="160" rx="95" ry="115" fill="url(#t-body-glow)"/>

      <!-- ── Ear handles ── -->
      <rect x="32"  y="105" width="36" height="58" rx="18"
        stroke="#2D8FE8" stroke-width="1.5" fill="#0A0E16"/>
      <rect x="212" y="105" width="36" height="58" rx="18"
        stroke="#2D8FE8" stroke-width="1.5" fill="#0A0E16"/>
      <!-- ear inner ring -->
      <rect x="41"  y="116" width="18" height="36" rx="9"
        stroke="#1A3A5C" stroke-width="1" fill="none"/>
      <rect x="221" y="116" width="18" height="36" rx="9"
        stroke="#1A3A5C" stroke-width="1" fill="none"/>
      <!-- ear mic dots -->
      <circle cx="50"  cy="134" r="3" fill="#1E6FBA" opacity="0.6">
        <animate attributeName="opacity" values="0.6;1;0.6" dur="2.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="230" cy="134" r="3" fill="#1E6FBA" opacity="0.6">
        <animate attributeName="opacity" values="0.6;1;0.6" dur="2.5s" begin="1.25s" repeatCount="indefinite"/>
      </circle>

      <!-- ── Body ── -->
      <rect x="60" y="58" width="160" height="208" rx="44"
        stroke="#4DAAFF" stroke-width="1.5" fill="#0A0E16" filter="url(#t-glow)"/>
      <!-- body panel lines -->
      <line x1="60"  y1="168" x2="220" y2="168" stroke="#141C28" stroke-width="1"/>
      <line x1="60"  y1="230" x2="220" y2="230" stroke="#141C28" stroke-width="1"/>

      <!-- ── Face panel ── -->
      <rect x="76" y="80" width="128" height="100" rx="18"
        fill="#080C12" stroke="#1E2D40" stroke-width="1"/>

      <!-- Left eye -->
      <circle cx="112" cy="120" r="16" fill="#0A0E16" stroke="#2D8FE8" stroke-width="1.5"/>
      <circle cx="112" cy="120" r="10" fill="#080C12"/>
      <circle cx="112" cy="120" r="6"  fill="#4DAAFF" opacity="0.95">
        <animate attributeName="opacity" values="0.95;0.35;0.95" dur="3.5s" repeatCount="indefinite"/>
      </circle>
      <!-- blink animation -->
      <rect x="96" y="112" width="32" height="16" rx="8" fill="#080C12" opacity="0">
        <animate attributeName="opacity" values="0;0;0;0;0;0;0;0;1;0" dur="6s" repeatCount="indefinite"/>
      </rect>
      <!-- eye specular -->
      <circle cx="115" cy="117" r="2.5" fill="white" opacity="0.5"/>

      <!-- Right eye -->
      <circle cx="168" cy="120" r="16" fill="#0A0E16" stroke="#2D8FE8" stroke-width="1.5"/>
      <circle cx="168" cy="120" r="10" fill="#080C12"/>
      <circle cx="168" cy="120" r="6"  fill="#4DAAFF" opacity="0.95">
        <animate attributeName="opacity" values="0.95;0.35;0.95" dur="3.5s" begin="1.75s" repeatCount="indefinite"/>
      </circle>
      <!-- blink -->
      <rect x="152" y="112" width="32" height="16" rx="8" fill="#080C12" opacity="0">
        <animate attributeName="opacity" values="0;0;0;0;0;0;0;0;1;0" dur="6s" begin="0.05s" repeatCount="indefinite"/>
      </rect>
      <circle cx="171" cy="117" r="2.5" fill="white" opacity="0.5"/>

      <!-- smile (LED dot strip) -->
      <path d="M104 154 Q140 172 176 154"
        stroke="#4DAAFF" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.4"/>
      <circle cx="108" cy="157" r="2.5" fill="#4DAAFF" opacity="0.8"/>
      <circle cx="122" cy="164" r="2.5" fill="#4DAAFF" opacity="0.8"/>
      <circle cx="140" cy="167" r="2.5" fill="#4DAAFF">
        <animate attributeName="opacity" values="0.8;1;0.8" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <circle cx="158" cy="164" r="2.5" fill="#4DAAFF" opacity="0.8"/>
      <circle cx="172" cy="157" r="2.5" fill="#4DAAFF" opacity="0.8"/>

      <!-- ── Audio waveform ── -->
      <g transform="translate(72, 184)" opacity="0.8">
        <line x1="0"   y1="14" x2="0"   y2="16" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="10;6;13;8;11" dur="1.1s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="20;24;17;22;19" dur="1.1s" repeatCount="indefinite"/>
        </line>
        <line x1="11"  y1="10" x2="11"  y2="20" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="6;11;4;9;7" dur="0.8s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="24;19;26;21;23" dur="0.8s" repeatCount="indefinite"/>
        </line>
        <line x1="22"  y1="6"  x2="22"  y2="24" stroke="#4DAAFF" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="3;9;1;6;4" dur="1.4s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="27;21;29;24;26" dur="1.4s" repeatCount="indefinite"/>
        </line>
        <line x1="33"  y1="10" x2="33"  y2="20" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="7;12;5;10;8" dur="1.0s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="23;18;25;20;22" dur="1.0s" repeatCount="indefinite"/>
        </line>
        <line x1="44"  y1="5"  x2="44"  y2="25" stroke="#4DAAFF" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="2;8;0;5;3" dur="1.6s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="28;22;30;25;27" dur="1.6s" repeatCount="indefinite"/>
        </line>
        <line x1="55"  y1="10" x2="55"  y2="20" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="8;13;6;11;9" dur="0.9s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="22;17;24;19;21" dur="0.9s" repeatCount="indefinite"/>
        </line>
        <line x1="66"  y1="7"  x2="66"  y2="23" stroke="#4DAAFF" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="4;10;2;7;5" dur="1.3s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="26;20;28;23;25" dur="1.3s" repeatCount="indefinite"/>
        </line>
        <line x1="77"  y1="10" x2="77"  y2="20" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="7;11;5;9;8" dur="1.2s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="23;19;25;21;22" dur="1.2s" repeatCount="indefinite"/>
        </line>
        <line x1="88"  y1="6"  x2="88"  y2="24" stroke="#4DAAFF" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="3;9;1;6;4" dur="0.7s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="27;21;29;24;26" dur="0.7s" repeatCount="indefinite"/>
        </line>
        <line x1="99"  y1="10" x2="99"  y2="20" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="8;12;6;10;9" dur="1.5s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="22;18;24;20;21" dur="1.5s" repeatCount="indefinite"/>
        </line>
        <line x1="110" y1="5"  x2="110" y2="25" stroke="#4DAAFF" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="2;8;0;5;3" dur="1.1s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="28;22;30;25;27" dur="1.1s" repeatCount="indefinite"/>
        </line>
        <line x1="121" y1="10" x2="121" y2="20" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="6;11;4;8;7" dur="0.9s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="24;19;26;22;23" dur="0.9s" repeatCount="indefinite"/>
        </line>
        <line x1="132" y1="12" x2="132" y2="18" stroke="#2D8FE8" stroke-width="2.5" stroke-linecap="round">
          <animate attributeName="y1" values="9;13;7;11;10" dur="1.3s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="21;17;23;19;20" dur="1.3s" repeatCount="indefinite"/>
        </line>
      </g>

      <!-- bottom charge indicator -->
      <rect x="112" y="246" width="56" height="8" rx="4" fill="#0D1117" stroke="#1E2D40" stroke-width="1"/>
      <rect x="114" y="248" width="38" height="4" rx="2" fill="#2D8FE8" opacity="0.7">
        <animate attributeName="width" values="38;48;38" dur="4s" repeatCount="indefinite"/>
      </rect>
      <rect x="168" y="249" width="4" height="6" rx="1" fill="#1E2D40"/>

      <!-- model label -->
      <text x="140" y="270" text-anchor="middle" fill="#2D4A6A" font-family="monospace" font-size="8" letter-spacing="2">MOCHI A1</text>
    </svg>

  </div>
</template>

<script setup lang="ts">
defineProps<{ slug: string }>()
</script>
