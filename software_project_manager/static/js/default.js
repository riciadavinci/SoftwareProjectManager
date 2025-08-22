
async function logout() {
    const resp = await fetch("/api/logout", {
        method: "POST",
        credentials: "include"
    });
    if (resp.ok) {
        localStorage.removeItem("spm_access_token");
        localStorage.removeItem("spm_refresh_token");
        window.location.href = "/login";
    }
}


async function fetchWithAuth(url, method="GET", options = {}, data=null) {
    let token = localStorage.getItem("spm_access_token");

    if (data !== null) {
        options.body = JSON.stringify(data);
    }

    // First attempt with access token
    let res = await fetch(url, {
        method: method,
        ...options,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${token}`
        }
    });

    // If expired, try refresh
    if (res.status === 401) {
        const refreshed = await refreshToken();
        if (!refreshed) {
            // redirect to login
            window.location.href = "/login";
            return;
        }

        // Retry original request with new token
        access_token = localStorage.getItem("spm_access_token");
        if (data !== null) {
            options.body = JSON.stringify(data);
        }

        res = await fetch(url, {
            method: method,
                ...options,
            headers: {
                ...options.headers,
                Authorization: `Bearer ${access_token}`
            }
        });
    }

    return res;
}

async function refreshToken() {
    const refresh = localStorage.getItem("spm_refresh_token");
    if (!refresh) {
        return false
    };

    const res = await fetch("/api/refresh-token", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${refresh}`},
        credentials: "include"
    });

    if (!res.ok) {
        return false
    };

    const { access_token } = await res.json();
    console.log(access_token);
    localStorage.setItem("spm_access_token", access_token);
    return true;
}
