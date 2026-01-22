import { is_logged, logout } from "./api.js"

async function init() {
    // Read profile container and get auth status
    const profileContainer = document.getElementById("header-container__profile-container")
    const logged = await is_logged()

    // Set display:none for text "Loading ..."
    const loading_text = profileContainer.querySelector("p")
    loading_text.style.display = "none"

    // Read all buttons
    const loginBtn = profileContainer.querySelector("a#header-container__login-link")
    const profileBtn = profileContainer.querySelector("a#header-container__profile-link")
    const logoutBtnContainer = document.getElementById("header-container__logout-container")

    // Set page for logged user
    if (logged) {
        loginBtn.style.display = "none"
        profileBtn.style.display = "block"
        logoutBtnContainer.style.display = "block"
    } else {
        loginBtn.style.display = "block"
        profileBtn.style.display = "none"
        logoutBtnContainer.style.display = "none"
    }

    const logoutBtn = document.getElementById("logout-btn")
    logoutBtn.addEventListener("click", (event) => {
        event.preventDefault()
        logout()
    })
}

init()