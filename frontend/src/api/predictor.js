import apiClient from "./client";

export const getPrediction = async (formData) => {
  const response = await apiClient.post("/predict", formData);
  return response.data;
};

export const getColleges = async (params) => {
  const response = await apiClient.get("/predict", { params });
  return response.data;
};