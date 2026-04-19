<template>
  <div class="pt-16 min-h-screen bg-canvas">
    <section class="section">
      <div class="max-w-5xl mx-auto">
        <!-- Header -->
        <div class="mb-16 reveal">
          <p class="label-tag mb-6">Contact</p>
          <h1 class="text-4xl md:text-5xl font-bold text-ink-primary mb-4">联系我们</h1>
          <p class="text-ink-secondary text-lg max-w-xl">
            无论是商务合作、媒体采访还是产品咨询，我们将在 24 小时内回复您。
          </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-5 gap-12">
          <!-- Contact info -->
          <div class="lg:col-span-2 space-y-4 reveal reveal-delay-1">
            <div
              v-for="info in contactInfo"
              :key="info.label"
              class="card p-5 flex items-start gap-4"
            >
              <div class="w-10 h-10 rounded bg-blue-dim/60 flex items-center justify-center text-lg flex-shrink-0">
                {{ info.icon }}
              </div>
              <div>
                <p class="text-ink-muted text-2xs tracking-wider uppercase mb-1">{{ info.label }}</p>
                <p class="text-ink-primary text-sm font-medium">{{ info.value }}</p>
              </div>
            </div>
          </div>

          <!-- Form -->
          <div class="lg:col-span-3 reveal reveal-delay-2">
            <!-- Success state -->
            <div
              v-if="result?.success"
              class="card p-8 text-center"
            >
              <div class="text-4xl mb-4">✅</div>
              <h3 class="text-ink-primary font-semibold text-lg mb-2">提交成功</h3>
              <p class="text-ink-secondary">{{ result.message }}</p>
              <button
                class="mt-6 text-blue-bright text-sm hover:underline"
                @click="handleReset"
              >
                再次提交
              </button>
            </div>

            <!-- Form -->
            <form v-else class="card p-8 space-y-5" @submit.prevent="handleSubmit">
              <div v-if="result?.success === false" class="bg-red-900/20 border border-red-500/30 rounded p-3 text-red-400 text-sm">
                {{ result.message }}
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                <div>
                  <label class="block text-ink-secondary text-xs mb-2">姓名 *</label>
                  <input
                    v-model="form.name"
                    type="text"
                    required
                    placeholder="您的姓名"
                    class="input-field"
                  />
                </div>
                <div>
                  <label class="block text-ink-secondary text-xs mb-2">邮箱 *</label>
                  <input
                    v-model="form.email"
                    type="email"
                    required
                    placeholder="your@email.com"
                    class="input-field"
                  />
                </div>
              </div>

              <div>
                <label class="block text-ink-secondary text-xs mb-2">公司</label>
                <input
                  v-model="form.company"
                  type="text"
                  placeholder="您的公司名称（选填）"
                  class="input-field"
                />
              </div>

              <div>
                <label class="block text-ink-secondary text-xs mb-2">需求类型 *</label>
                <select v-model="form.inquiry_type" class="input-field">
                  <option value="cooperation">商务合作</option>
                  <option value="media">媒体采访</option>
                  <option value="other">其他</option>
                </select>
              </div>

              <div>
                <label class="block text-ink-secondary text-xs mb-2">留言内容 *</label>
                <textarea
                  v-model="form.message"
                  required
                  rows="5"
                  placeholder="请描述您的需求或问题..."
                  class="input-field resize-none"
                />
              </div>

              <AppBtn
                type="submit"
                variant="primary"
                size="lg"
                class="w-full justify-center"
                :disabled="submitting"
              >
                <span v-if="submitting" class="flex items-center gap-2">
                  <span class="w-4 h-4 border-2 border-canvas/40 border-t-canvas rounded-full animate-spin" />
                  提交中...
                </span>
                <span v-else>发送消息</span>
              </AppBtn>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { storeToRefs } from 'pinia'
import AppBtn from '@/components/common/AppBtn.vue'
import { useContactStore } from '@/stores/contact'
import { useScrollAnimation } from '@/composables/useScrollAnimation'
import type { ContactForm } from '@/types'

useScrollAnimation()

const store = useContactStore()
const { submitting, result } = storeToRefs(store)

const form = reactive<ContactForm>({
  name: '',
  email: '',
  company: '',
  inquiry_type: 'cooperation',
  message: '',
})

function handleSubmit() {
  store.submit({ ...form })
}

function handleReset() {
  store.reset()
  form.name = ''
  form.email = ''
  form.company = ''
  form.inquiry_type = 'cooperation'
  form.message = ''
}

const contactInfo = [
  { icon: '📧', label: '商务邮箱', value: 'contact@ai-terminal.com' },
  { icon: '🤝', label: '商务合作', value: 'business@ai-terminal.com' },
  { icon: '📍', label: '总部地址', value: '中国 · 深圳' },
]
</script>

<style scoped>
.input-field {
  @apply w-full bg-canvas border border-line-base rounded px-4 py-3 text-ink-primary text-sm
    placeholder:text-ink-muted
    focus:outline-none focus:border-blue-base/60 focus:ring-1 focus:ring-blue-base/20
    transition-colors duration-200;
}
</style>
