const token = localStorage.getItem('token') ?? false;
if (token) {
  window.location.href = '/index.html';
}

const { createApp } = Vue

const app = createApp({
  data() {
    return {
      isRegister: false,
      login: '',
      password: '',
      passwordRepeat: '',
      username: '',
      blood_group: '',
      height: ''
    }
  },
  methods: {
    async loginUser() {
      if (this.login === '' || this.password === '') {
        alert('Fill in all fields')
        return
      }

      const res = await loginUser({login: this.login, password: this.password})
      if (res.error) {
        alert(res.error)
      } else {
        localStorage.setItem('token', res.token)
        localStorage.setItem('userId', res.id)
        localStorage.setItem('userLogin', res.login)
        window.location.href = '/index.html'
      }
    },
    async registerUser() {
      if (this.login === '' || this.password === '' || this.passwordRepeat === '' || this.username === '' || this.blood_group === '' || this.height === '') {
        alert('Fill in all fields')
        return
      }

      if (this.password !== this.passwordRepeat) {
        alert('Passwords do not match')
        return
      }

      const res = await registerUser({
        login: this.login,
        password: this.password,
        name: this.username,
        blood_group: this.blood_group,
        height: this.height
      })
      if (res.error) {
        alert(res.error)
      } else {
        localStorage.setItem('token', res.token)
        localStorage.setItem('userId', res.id)
        localStorage.setItem('userLogin', res.login)
        window.location.href = '/index.html'
      }
    },
  }
})

app.mount('#app')