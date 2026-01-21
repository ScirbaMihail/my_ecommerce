import { login } from "./api.js"

const form = document.getElementById('login-form')

async function submitForm() {
    const formData = new FormData(form)
    await login(formData.get('email'), formData.get('password'))
}

form.addEventListener('submit', (event) => {
    event.preventDefault()
    submitForm()
})
