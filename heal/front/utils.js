const baseUrl = 'http://127.0.0.1:3000';

async function registerUser(userData) {
    const response = await fetch(`${baseUrl}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    });
    return await response.json();
}

async function loginUser(userData) {
    const response = await fetch(`${baseUrl}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    });
    return await response.json();
}

async function getUserById(userId) {
    const response = await fetch(`${baseUrl}/user/${userId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

async function getUserByLogin(login) {
    const response = await fetch(`${baseUrl}/user/login/${login}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

async function deleteUser(userId) {
    const response = await fetch(`${baseUrl}/user/${userId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

async function addStatistics(statisticsData) {
    const response = await fetch(`${baseUrl}/statistics`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(statisticsData)
    });
    return await response.json();
}

async function getStatisticsByDay(userId) {
    const response = await fetch(`${baseUrl}/statistics/day/${userId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

async function getStatisticsByWeek(userId) {
    const response = await fetch(`${baseUrl}/statistics/week/${userId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

async function getStatisticsByMonth(userId) {
    const response = await fetch(`${baseUrl}/statistics/month/${userId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

async function getStatisticsByYear(userId) {
    const response = await fetch(`${baseUrl}/statistics/year/${userId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}
