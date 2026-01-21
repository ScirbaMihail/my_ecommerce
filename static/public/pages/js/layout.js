import { is_logged, logout } from "./api.js"

async function init() {
    const profileContainer = document.getElementById('header-container__profile')
    const status = await is_logged()

    const loading_elem = profileContainer.querySelector('p')
    loading_elem.style.display = 'none'

    const link_elem = profileContainer.querySelector('a#header-container__login-link')
    link_elem.style.display = 'block'
    link_elem.innerText = status == true ? "My profile" : "Log in"

    const logoutBtn = document.getElementById("logout-btn")
    logoutBtn.style.display = status == true ? "block" : "none"
    logoutBtn.addEventListener("click", (event) => {
        event.preventDefault()
        logout()
    })
}

init()