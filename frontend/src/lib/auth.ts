import type { RegisterFormValues } from "@/pages/Register.types";
import axios from "axios";
import type { InternalAxiosRequestConfig } from "axios";

type RegisterPayload = {
  email: string;
  password: string;
  full_name: string;
};

type RegisterResponse = {
  id: string;
  email: string;
  full_name: string;
  role: "admin" | "candidate" | "reviewer";
};

type RegisterResult =
  | { success: true; data: RegisterResponse }
  | { success: false; message: string; status?: number };

type LoginPayload = {
  email: string;
  password: string;
};

type LoginResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

type LoginResult =
  | { success: true; data: LoginResponse }
  | { success: false; message: string; status?: number };

export type AccessTokenClaims = {
  sub: string;
  role: "admin" | "candidate" | "reviewer";
  type: "access";
  exp: number;
};

export type AuthUserFromToken = {
  publicId: string;
  role: AccessTokenClaims["role"];
  exp: number;
  isExpired: boolean;
};

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";
const TOKEN_STORAGE_KEY = "decentrathon.auth.tokens";

type AuthTokens = LoginResponse;

let authTokens: AuthTokens | null = null;

if (typeof window !== "undefined") {
  const storedTokens = sessionStorage.getItem(TOKEN_STORAGE_KEY);
  if (storedTokens) {
    try {
      authTokens = JSON.parse(storedTokens) as AuthTokens;
    } catch {
      sessionStorage.removeItem(TOKEN_STORAGE_KEY);
    }
  }
}

const toPayload = (data: RegisterFormValues): RegisterPayload => ({
  email: data.email,
  password: data.password,
  full_name: data.fullName,
});

const toLoginPayload = (data: {
  email: string;
  password: string;
}): LoginPayload => ({
  email: data.email,
  password: data.password,
});

const persistTokens = (tokens: AuthTokens) => {
  authTokens = tokens;

  if (typeof window !== "undefined") {
    sessionStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(tokens));
  }
};

export const clearTokens = () => {
  authTokens = null;

  if (typeof window !== "undefined") {
    sessionStorage.removeItem(TOKEN_STORAGE_KEY);
  }
};

export const getAccessToken = (): string | null =>
  authTokens?.access_token ?? null;
export const getRefreshToken = (): string | null =>
  authTokens?.refresh_token ?? null;

const decodeJwtPayload = (token: string): Record<string, unknown> | null => {
  const parts = token.split(".");
  if (parts.length !== 3) {
    return null;
  }

  try {
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, "=");
    const json = atob(padded);
    const parsed = JSON.parse(json);

    if (!parsed || typeof parsed !== "object") {
      return null;
    }

    return parsed as Record<string, unknown>;
  } catch {
    return null;
  }
};

export const getAccessTokenClaims = (): AccessTokenClaims | null => {
  const accessToken = getAccessToken();
  if (!accessToken) {
    return null;
  }

  const payload = decodeJwtPayload(accessToken);
  if (!payload) {
    return null;
  }

  const sub = payload.sub;
  const role = payload.role;
  const tokenType = payload.type;
  const exp = payload.exp;

  if (
    typeof sub !== "string" ||
    (role !== "admin" && role !== "candidate" && role !== "reviewer") ||
    tokenType !== "access" ||
    typeof exp !== "number"
  ) {
    return null;
  }

  return {
    sub,
    role,
    type: "access",
    exp,
  };
};

export const getUserFromToken = (): AuthUserFromToken | null => {
  const claims = getAccessTokenClaims();
  if (!claims) {
    return null;
  }

  return {
    publicId: claims.sub,
    role: claims.role,
    exp: claims.exp,
    isExpired: Date.now() >= claims.exp * 1000,
  };
};

const getErrorMessage = (
  error: unknown,
): { message: string; status?: number } => {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const detail = (error.response?.data as { detail?: unknown } | undefined)
      ?.detail;

    if (typeof detail === "string") {
      return { message: detail, status };
    }

    if (Array.isArray(detail)) {
      const first = detail[0];
      if (
        first &&
        typeof first === "object" &&
        "msg" in first &&
        typeof first.msg === "string"
      ) {
        return { message: first.msg, status };
      }
    }

    return {
      message: error.message || "Registration failed. Please try again.",
      status,
    };
  }

  return { message: "Registration failed. Please try again." };
};

export const registerCandidate = async (
  data: RegisterFormValues,
): Promise<RegisterResult> => {
  try {
    const payload = toPayload(data);
    const res = await axios.post<RegisterResponse>(
      `${API_URL}/auth/register`,
      payload,
    );

    return {
      success: true,
      data: res.data,
    };
  } catch (error) {
    const { message, status } = getErrorMessage(error);
    return { success: false, message, status };
  }
};

export const loginCandidate = async (data: {
  email: string;
  password: string;
}): Promise<LoginResult> => {
  try {
    const payload = toLoginPayload(data);
    const formData = new URLSearchParams();
    formData.set("username", payload.email);
    formData.set("password", payload.password);

    const res = await axios.post<LoginResponse>(
      `${API_URL}/auth/login`,
      formData,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      },
    );

    persistTokens(res.data);

    return {
      success: true,
      data: res.data,
    };
  } catch (error) {
    const { message, status } = getErrorMessage(error);
    return { success: false, message, status };
  }
};

export const refreshAccessToken = async (): Promise<LoginResult> => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    return {
      success: false,
      message: "Refresh token not found.",
    };
  }

  try {
    const res = await axios.post<LoginResponse>(`${API_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });

    persistTokens(res.data);

    return {
      success: true,
      data: res.data,
    };
  } catch (error) {
    const { message, status } = getErrorMessage(error);
    return { success: false, message, status };
  }
};

export const logoutCandidate = async (): Promise<void> => {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    clearTokens();
    return;
  }

  try {
    await axios.post(`${API_URL}/auth/logout`, {
      refresh_token: refreshToken,
    });
  } catch {
    // Ignore logout API errors and always clear local auth state.
  } finally {
    clearTokens();
  }
};

type RetriableRequestConfig = InternalAxiosRequestConfig & {
  _retry?: boolean;
};

const setAuthorizationHeader = (
  config: InternalAxiosRequestConfig,
  token: string,
) => {
  const headers = config.headers as Record<string, string>;
  headers.Authorization = `Bearer ${token}`;
};

export const apiClient = axios.create({
  baseURL: API_URL,
});

let isRefreshing = false;
let pendingRequests: Array<(token: string | null) => void> = [];

const resolvePendingRequests = (token: string | null) => {
  pendingRequests.forEach((callback) => callback(token));
  pendingRequests = [];
};

apiClient.interceptors.request.use((config) => {
  const accessToken = getAccessToken();

  if (accessToken) {
    setAuthorizationHeader(config, accessToken);
  }

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: unknown) => {
    if (!axios.isAxiosError(error)) {
      return Promise.reject(error);
    }

    const originalRequest = error.config as RetriableRequestConfig | undefined;

    if (
      !originalRequest ||
      error.response?.status !== 401 ||
      originalRequest._retry
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        pendingRequests.push((token) => {
          if (!token) {
            reject(error);
            return;
          }

          setAuthorizationHeader(originalRequest, token);
          resolve(apiClient(originalRequest));
        });
      });
    }

    isRefreshing = true;

    try {
      const refreshed = await refreshAccessToken();

      if (!refreshed.success) {
        clearTokens();
        resolvePendingRequests(null);
        return Promise.reject(error);
      }

      const newAccessToken = refreshed.data.access_token;
      resolvePendingRequests(newAccessToken);
      setAuthorizationHeader(originalRequest, newAccessToken);
      return apiClient(originalRequest);
    } finally {
      isRefreshing = false;
    }
  },
);

export const isLoggedIn = () => {
  const user = getUserFromToken();
  return Boolean(user && !user.isExpired);
};
