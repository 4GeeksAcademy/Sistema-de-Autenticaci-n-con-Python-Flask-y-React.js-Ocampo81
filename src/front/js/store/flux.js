const getState = ({ getStore, getActions, setStore }) => {
    return {
        store: {
            message: null,
            token: sessionStorage.getItem('token') || null, 
            user: {}, // Datos del usuario logueado
        },
        actions: {
            fetchWithCheck: async (url, options = {}) => {
                try {
                    const response = await fetch(url, options);
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(JSON.stringify(errorData));
                    }
                    return await response.json();
                } catch (error) {
                    console.error("Error in fetch:", error.message);
                    return null;
                }
            },

            signup: async (email, password) => {
                const response = await getActions().fetchWithCheck(process.env.BACKEND_URL + "/api/signup", {
                    method: "POST",
                    body: JSON.stringify({ email, password }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                if (response) {
                    setStore({ message: response.message });
                    return true;
                } else {
                    setStore({ message: "Signup failed" });
                    return false;
                }
            },

            login: async (email, password) => {
                const response = await getActions().fetchWithCheck(process.env.BACKEND_URL + "/api/login", {
                    method: "POST",
                    body: JSON.stringify({ email, password }),
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                if (response && response.token) {
                    sessionStorage.setItem('token', response.token); 
                    setStore({ token: response.token, user: response });
                    return true;
                } else {
                    setStore({ message: "Login failed" });
                    return false;
                }
            },

            getPrivateData: async () => {
                const store = getStore();
                const response = await getActions().fetchWithCheck(process.env.BACKEND_URL + "/api/private", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${store.token}`,
                        "Content-Type": "application/json"
                    }
                });

                if (response) {
                    setStore({ user: response });
                    return response;
                } else {
                    setStore({ message: "Failed to fetch private data" });
                    return null;
                }
            },

            logout: () => {
                sessionStorage.removeItem('token'); 
                setStore({ token: null, user: {} });
            },
        }
    };
};

export default getState;
