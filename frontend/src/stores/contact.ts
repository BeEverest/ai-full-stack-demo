import { defineStore } from 'pinia'
import { ref } from 'vue'
import { submitContact } from '@/api/contact'
import type { ContactForm } from '@/types'

export const useContactStore = defineStore('contact', () => {
  const submitting = ref(false)
  const result = ref<{ success: boolean; message: string } | null>(null)

  async function submit(form: ContactForm) {
    submitting.value = true
    result.value = null
    try {
      result.value = await submitContact(form)
    } catch (e: any) {
      const detail = e?.response?.data?.detail
      const msg =
        Array.isArray(detail)
          ? detail[0]?.msg ?? '提交失败'
          : typeof detail === 'string'
          ? detail
          : '提交失败，请稍后重试'
      result.value = { success: false, message: msg }
    } finally {
      submitting.value = false
    }
  }

  function reset() {
    result.value = null
  }

  return { submitting, result, submit, reset }
})
