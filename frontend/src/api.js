import axios from "axios";

const BACKEND_HOST = process.env.REACT_APP_BACKEND_HOST || "localhost";
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT || "8000";

const BACKEND_SERVER = `${BACKEND_HOST}:${BACKEND_PORT}/api/v1.0/`;

async function apiGet(route, payload = {}) {
    const config = {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    };

    console.log(`http://${BACKEND_SERVER}${route}`);

    return axios.get(
        `http://${BACKEND_SERVER}${route}/`,
        {
            ...payload,
        },
        config
    );
}

async function apiPost(route, payload = {}) {
    const config = {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    };

    return axios.post(
        `http://${BACKEND_SERVER}${route}`,
        {
            ...payload,
        },
        config
    );
}

const api = {
    get: apiGet,
    post: apiPost,
};

export default api;
