import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const getModels = async () => {
    const response = await apiClient.get('/models');
    return response.data;
};

export const predictEmotion = async (imageFile, modelId) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('model_id', modelId);

    const response = await apiClient.post('/predict', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};
