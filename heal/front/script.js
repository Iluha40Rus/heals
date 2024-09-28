const token = localStorage.getItem("token") ?? false
if (!token) {
  window.location.href = "/auth/auth.html"
}

const { createApp } = Vue

const app = createApp({
  data() {
    return {
      token: localStorage.getItem("token"),
      userID: localStorage.getItem("userId"),
      userLogin: localStorage.getItem("userLogin"),
      userName: '',
      isTable: true,
      blood_sugar: 0,
      weight: 0,
      temperature: 0,
      pulse: 0,
      pressure: 0,
      overall_state: 0,
      oxygen_level: 0,
      cholesterol: 0,
      data: [],
    }
  },
  methods: {
    logout() {
      localStorage.clear()
      window.location.href = "/auth/auth.html"
    },
    onShowAddPost() {
      this.$refs.addPostModal.showModal()
    },
    onCloseAddPost() {
      this.$refs.addPostModal.close()
    },
    async addPost() {
      await addStatistics({
        blood_sugar: this.blood_sugar,
        weight: this.weight,
        temperature: this.temperature,
        pulse: this.pulse,
        pressure: this.pressure,
        overall_state: this.overall_state,
        oxygen_level: this.oxygen_level,
        cholesterol: this.cholesterol,
        user_id: this.userID
      })

      this.blood_sugar = 0
      this.weight = 0
      this.temperature = 0
      this.pulse = 0
      this.pressure = 0
      this.overall_state = 0
      this.oxygen_level = 0
      this.cholesterol = 0

      const data = await getStatisticsByYear(this.userID)
      this.data = data

      this.onCloseAddPost()
    }
  },
  async mounted() {
    const res = await getUserById(this.userID)
    this.userName = res.name

    const data = await getStatisticsByYear(this.userID)
    this.data = data
    console.log(this.data);
    
  },
  watch: {
    isTable(newValue) {
      if (newValue) {
        return
      }
      this.$nextTick(() => {
        new Chart(this.$refs.chart_body, {
          type: 'bar',
          data: {
            labels: ['Сахар', 'Вес', 'Температура', 'Пульс', 'Давление', 'Общее состояние', 'Уровень кислорода', 'Холестерин'],
            datasets: this.data.map((item) => ({
              label: item.date,
              data: [item.blood_sugar, item.weight, item.temperature, item.pulse, item.pressure, item.overall_state, item.oxygen_level, item.cholesterol],
              borderWidth: 1
            }))
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      })
    }
  }
})

app.mount('#app')
