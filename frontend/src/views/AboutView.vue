<template>
  <div class="pt-16">
    <!-- Mission -->
    <section class="section bg-canvas relative overflow-hidden">
      <div class="absolute inset-0 bg-grid-subtle opacity-100 pointer-events-none" />
      <div class="relative max-w-4xl mx-auto">
        <p class="label-tag mb-8 reveal">About Us</p>
        <h1 class="text-4xl md:text-6xl font-bold text-ink-primary mb-6 leading-tight reveal reveal-delay-1">
          让 AI 真正成为<br /><span class="text-blue-gradient">人类的延伸</span>
        </h1>
        <p class="text-ink-secondary text-lg leading-relaxed max-w-2xl reveal reveal-delay-2">
          我们是一家专注于AI硬件终端的科技公司，融合前沿人工智能、精密硬件工程与人机交互设计，
          致力于打造真正改变生活方式的智能产品。
        </p>
      </div>
    </section>

    <!-- Stats -->
    <section class="section bg-surface">
      <div class="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-px bg-line-base rounded-lg overflow-hidden">
        <div
          v-for="(s, i) in companyStats"
          :key="s.label"
          class="bg-surface px-6 py-8 text-center reveal"
          :class="`reveal-delay-${i + 1}`"
        >
          <div class="text-3xl font-bold font-mono text-blue-gradient mb-2">{{ s.value }}</div>
          <p class="text-ink-secondary text-sm">{{ s.label }}</p>
        </div>
      </div>
    </section>

    <!-- Story -->
    <section class="section bg-canvas">
      <div class="max-w-3xl mx-auto">
        <div class="mb-10 reveal">
          <p class="label-tag mb-4">Our Story</p>
          <h2 class="text-3xl font-bold text-ink-primary">我们的故事</h2>
        </div>
        <div class="space-y-5 text-ink-secondary leading-relaxed reveal reveal-delay-1">
          <p>
            AI智能终端成立于2023年，由一群来自顶尖科技公司的工程师与设计师共同创立。
            我们看到了一个明确的机会：AI技术正在从云端走向边缘，从屏幕走向现实世界。
          </p>
          <p>
            我们的三款产品——AI眼镜、AI机器人、AI玩具——代表了我们对未来人机交互形态的判断：
            视觉增强、自然交互、情感连接，将是下一个十年最重要的入口。
          </p>
          <p>
            我们相信，最好的技术不是让人感知到它的存在，而是悄然放大每一个人的潜能。
          </p>
        </div>
      </div>
    </section>

    <!-- Timeline -->
    <section class="section bg-surface">
      <div class="max-w-3xl mx-auto">
        <div class="mb-12 reveal">
          <p class="label-tag mb-4">Milestones</p>
          <h2 class="text-3xl font-bold text-ink-primary">发展历程</h2>
        </div>
        <div class="relative">
          <div class="absolute left-4 top-0 bottom-0 w-px bg-line-base" />
          <div
            v-for="(event, i) in timeline"
            :key="event.year + event.title"
            class="relative pl-12 pb-10 last:pb-0 reveal"
            :class="`reveal-delay-${Math.min(i + 1, 4)}`"
          >
            <div class="absolute left-0 top-1 w-8 h-8 rounded-full bg-surface border-2 border-blue-dim flex items-center justify-center">
              <div class="w-2 h-2 rounded-full bg-blue-base" />
            </div>
            <span class="text-blue-bright text-2xs font-mono tracking-wider">{{ event.year }}</span>
            <h3 class="text-ink-primary font-semibold mt-1 mb-1.5">{{ event.title }}</h3>
            <p class="text-ink-secondary text-sm">{{ event.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Join Us -->
    <section class="section bg-canvas text-center">
      <div class="max-w-2xl mx-auto reveal">
        <p class="label-tag mb-6 inline-flex">Join Us</p>
        <h2 class="text-3xl font-bold text-ink-primary mb-4">加入我们</h2>
        <p class="text-ink-secondary mb-8">
          我们正在寻找有激情、有能力的伙伴，一起构建AI硬件的未来。
        </p>
        <AppBtn variant="primary" size="lg" to="/contact">查看职位</AppBtn>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import AppBtn from '@/components/common/AppBtn.vue'
import { useScrollAnimation } from '@/composables/useScrollAnimation'

useScrollAnimation()

const companyStats = [
  { value: '2023', label: '成立年份' },
  { value: '50+', label: '核心团队' },
  { value: '30+', label: '技术专利' },
  { value: '3', label: '旗舰产品' },
]

const timeline = [
  { year: '2023 Q1', title: '公司成立', desc: '核心创始团队组建完成，完成天使轮融资。' },
  { year: '2023 Q3', title: 'AI眼镜原型发布', desc: '首款产品原型亮相，获得业界广泛关注。' },
  { year: '2024 Q1', title: 'AI机器人立项', desc: '家庭与企业双场景AI机器人正式进入研发阶段。' },
  { year: '2024 Q3', title: 'AI玩具产品线拓展', desc: '面向儿童教育市场的AI玩具产品正式立项。' },
  { year: '2025', title: '全产品线官网上线', desc: '三款旗舰产品同步亮相，开放商务合作咨询。' },
]
</script>
