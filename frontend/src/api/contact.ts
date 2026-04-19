import client from './client'
import type { ContactForm } from '@/types'

export const submitContact = (data: ContactForm): Promise<{ success: boolean; message: string }> =>
  client.post('/contact', data)
