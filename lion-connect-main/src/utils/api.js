import axios from 'axios';

export const api = axios.create({
  baseURL: 'https://lion-connect-backend.onrender.com',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
});

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    // 로그인과 회원가입 요청에는 토큰을 포함하지 않음
    if (config.url && (config.url.includes('/auth/login') || config.url.includes('/auth/signup'))) {
      delete config.headers['Authorization'];
      return config;
    }
    
    // 다른 요청에는 토큰 포함
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const apis = {
  // 로그인
  postLogin: async (data) => {
    try {
      const response = await api.post("/auth/login", data);
      return response;
    } catch (error) {
      throw error;
    }
  },

  // 회원가입
  postSignUp: async (data) => {
    try {
      const response = await api.post("/auth/signup", {
        ...data,
        user_type: data.userType,
        name: data.userType === "company" ? data.companyName : data.name,
      });
      return response;
    } catch (error) {
      throw error;
    }
  },

  // 이력서 - 프로젝트 추가
  postProject: async (data) => {
    try {
      const response = await api.post("/user/project", data);
      return response;
    } catch (error) {
      throw error;
    }
  },
}; 