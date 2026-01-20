import { is_logged } from "./api.js"

async function init() {
    const profileContainer = document.getElementById('header-container__profile')
    const status = await is_logged()

    const loading_elem = profileContainer.querySelector('p')
    loading_elem.style.display = 'none'

    const link_elem = profileContainer.querySelector('a')
    link_elem.style.display = 'block'
    link_elem.innerText = status
}

init()