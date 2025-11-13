import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const isLoggedIn = ref(!!localStorage.getItem('authToken'))
const userData = ref(JSON.parse(localStorage.getItem('userData') || 'null'))

export function useAuth() {
  const router = useRouter()

  const login = async (username, password) => {
    const { data: loginData } = await api.post('auth/login/', { username, password })
    const token = loginData.key

    const { data: user } = await api.get('auth/user/', {
      headers: { Authorization: `Token ${token}` },
    })

    localStorage.setItem('authToken', token)
    localStorage.setItem('userData', JSON.stringify(user))
    isLoggedIn.value = true
    userData.value = user

    router.push('/')
  }

  const logout = () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('userData')
    isLoggedIn.value = false
    userData.value = null
    router.push('/')
  }

  return { isLoggedIn, userData, login, logout }
}
