import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})
// เพิ่ม interceptor สำหรับ token อัตโนมัติ
api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) config.headers.Authorization = `Token ${token}`
  return config
})

export default api
