const API_URL = 'http://127.0.0.1:8000/api'

async function refreshToken(): Promise<boolean> {
    const url = `${API_URL}/token/refresh`
    const response = await fetch(url, {
        headers: {
            "Content-type": "application/json"
        },
        credentials: "include"
    })
    return response.ok
}

async function fetchWithAuth<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
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
        window.location.href = ''
    }

    if (!response.ok) {
        throw new Error(`API ERROR: ${response.status}`)
    }

    return response.json()
}