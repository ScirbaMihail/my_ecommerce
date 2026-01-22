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

    // Perform fetch to endpoint
    const response = await fetch(url, {
        headers: {
            "Content-type": "application/json",
            ...options.headers
        },
        credentials: "include",
        ...options
    })

    // If unauthorized, try to refresh token
    if (response.status === 401) {
        const refreshed = await refreshToken()
        // If refreshing succeeded, try to fetch again
        if (refreshed) {
            return fetchWithAuth(endpoint, options)
        }
        // If refreshing failed, either raise error or redirect to login page
        // Rising error is meant to handle no action. 
        // Example: header buttons, if not logged there just have to be `Log in` button,
        //          no need to redirect to login.
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

async function fetchWithNoAuth(endpoint, options = {}) {
    const url = `${API_URL}/${endpoint}`
    const response = await fetch(url, {
        headers: {
            "Content-type": "application/json",
            ...options.headers
        },
        ...options
    })

    if (!response.ok) {
        throw new Error(`API ERROR: ${response.status}`)
    }

    return response.json()
}


export async function is_logged() {
    try {
        await fetchWithAuth('auth/authentication_status/', {}, true)
        return true
    } catch {
        return false
    }
}

export async function login(email, password) {
    const credentials = {
        "email": email,
        "password": password
    }
    try {
        await fetchWithNoAuth('auth/login/', { method: "POST", body: JSON.stringify(credentials) })
        window.location.href = '/'
    } catch {
        window.location.href = '/login'
    }
}

export async function logout() {
    await fetchWithAuth("auth/logout/", { method: "POST" })
    window.location.href = '/'
}