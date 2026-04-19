import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

export function useCountUp(targetEl: string) {
  onMounted(() => {
    const elements = document.querySelectorAll<HTMLElement>(targetEl)
    elements.forEach((el) => {
      const end = parseFloat(el.dataset.count ?? '0')
      const obj = { val: 0 }
      gsap.to(obj, {
        val: end,
        duration: 1.5,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
          once: true,
        },
        onUpdate: () => {
          el.textContent = Number.isInteger(end)
            ? Math.round(obj.val).toString()
            : obj.val.toFixed(1)
        },
      })
    })
  })
}
