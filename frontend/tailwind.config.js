/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // ─── 背景层级 ────────────────────────────────
        canvas:  '#080C12',   // 页面底色：深海军蓝黑
        surface: '#0D1117',   // 卡片/面板
        raised:  '#131920',   // 悬浮元素
        // ─── 单一强调色：电气蓝 ──────────────────────
        blue: {
          dim:    '#1A3A5C',  // 微妙背景
          muted:  '#1E6FBA',  // 次要交互
          base:   '#2D8FE8',  // 主按钮、链接
          bright: '#4DAAFF',  // 高亮、图标
          glow:   '#6DC4FF',  // 发光边缘（克制使用）
        },
        // ─── 文字层级 ────────────────────────────────
        ink: {
          primary:   '#E8EDF2',  // 主标题
          secondary: '#8B9AB0',  // 描述文字
          muted:     '#4A5568',  // 占位符、辅助
        },
        // ─── 边框/线条 ───────────────────────────────
        line: {
          faint:  '#141C28',  // 几乎不可见的分隔
          base:   '#1E2D40',  // 默认边框
          bright: '#2D4A6A',  // hover 边框
        },
      },
      fontFamily: {
        sans:  ['Inter', 'PingFang SC', 'Noto Sans SC', 'system-ui', 'sans-serif'],
        mono:  ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      fontSize: {
        // 精密感的标签字号
        '2xs': ['0.625rem', { lineHeight: '1rem', letterSpacing: '0.1em' }],
      },
      boxShadow: {
        // 只保留蓝色，去除紫色
        'glow-sm': '0 0 12px rgba(45, 143, 232, 0.15)',
        'glow-md': '0 0 24px rgba(45, 143, 232, 0.25)',
        'glow-lg': '0 0 48px rgba(45, 143, 232, 0.35)',
        'inset-line': 'inset 0 1px 0 rgba(255,255,255,0.04)',
      },
      backgroundImage: {
        // 单色渐变，不再用青-紫双色
        'gradient-blue': 'linear-gradient(135deg, #1E6FBA 0%, #2D8FE8 100%)',
        'gradient-dark': 'linear-gradient(180deg, #080C12 0%, #0D1117 100%)',
        // 微妙网格
        'grid-subtle': `
          linear-gradient(rgba(45,143,232,0.04) 1px, transparent 1px),
          linear-gradient(90deg, rgba(45,143,232,0.04) 1px, transparent 1px)
        `,
      },
      animation: {
        'glow-pulse': 'glow-pulse 3s ease-in-out infinite',
        'float':      'float 8s ease-in-out infinite',
      },
      keyframes: {
        'glow-pulse': {
          '0%, 100%': { opacity: '0.6' },
          '50%':      { opacity: '1' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-10px)' },
        },
      },
      transitionTimingFunction: {
        'expo': 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
  plugins: [],
}
