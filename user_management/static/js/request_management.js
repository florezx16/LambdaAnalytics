function sessionDestroy() {
    fetch('/user_management/tokenLogout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.request_status) {
                window.location.href = '/user_management/user_login_view';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function ProtectRequest(url, method = 'GET', body) {
    const accessToken = sessionStorage.getItem('accessToken');
    return fetch(url, {
        method: method,
        headers: {
            'Authorization': 'Bearer ' + accessToken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    })
        .then(response => {
            if (response.status == 401) { //Expired access token
                return refreshAccessToken().then(() => {
                    //Try again the request
                    const newAccessToken = sessionStorage.getItem('accessToken');
                    return fetch(url, {
                        method: method,
                        headers: {
                            'Authorization': 'Bearer ' + newAccessToken,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(body),
                    });
                });
            }
            return response.json(); //Return response
        })
        .catch(error => console.error('Error al hacer la solicitud:', error));
}

function refreshAccessToken() {
    const refreshToken = sessionStorage.getItem('refreshToken');
    return fetch('/user_management/api/token/refresh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken })
    })
        .then(response => response.json())
        .then(data => {
            if (data.access) {
                //Update access token into sessionStorage
                sessionStorage.setItem('accessToken', data.access);
            } else {
                //Refresh token expired, redirect to login page
                sessionDestroy()
            }
        })
        .catch(error => {
            console.error('ERROR:', error);
            sessionDestroy()
        });
}

function makeNormalRequest(url, method = 'GET', body) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: method != 'GET' ? JSON.stringify(body) : null
    })
        .then(response => {
            return response.json();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}