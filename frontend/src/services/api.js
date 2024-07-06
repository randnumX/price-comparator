import axios from 'axios';

const BASE_URL = 'https://fakestoreapi.com';

export const api = {
  scrape: async (payload) => {
    try {
      const response = await axios.get(`${BASE_URL}/products`);
      console.debug(response)
      return response.data;
    } catch (error) {
      console.error('Error in scrape API:', error);
      throw error;
    }
  },
  getHistory: async (payload) => {
    try {
      const response = await axios.get(`${BASE_URL}/products`);
      console.debug(response)
      return response.data;
    } catch (error) {
      console.error('Error in getHistory API:', error);
      throw error;
    }
  },
};