const API_URL = 'http://127.0.0.1:8000/api'

async function refreshToken() {
    const url = `${API_URL}/auth/token/refresh/`
    const response = await fetch(url, {
        headers: {
            "Content-type": "application/json"
        },
        method: "POST",
        credentials: "include"
    })
    return response.ok
}

async function fetchWithAuth(endpoint, options = {}, raise_error = false) {
    const url = `${API_URL}/${endpoint}`
    const response = await fetch(url, {
        headers: {
            "Content-type": "application/json",
            ...options.headers
        },
        credentials: "include",
        ...options
    })

    if (response.status === 401) {
        const refreshed = await refreshToken()
        if (refreshed) {
            return fetchWithAuth(url, options)
        }
        if (raise_error) {
            throw new Error(`API ERROR: refresh token failed`)
        }
        window.location.href = '/login'
    }

    if (!response.ok) {
        throw new Error(`API ERROR: ${response.status}`)
    }

    return response.json()
}


export async function is_logged() {
    try {
        await fetchWithAuth('auth/authentication_status/', {}, true)
        return "My profile"
    } catch {
        return "Log in"
    }
}