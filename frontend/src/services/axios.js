import axios from "axios";

const baseURL = "https://jay-two-door-backend.vercel.app/api/v1";

const axiosInstance = axios.create({
  baseURL,
});

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
