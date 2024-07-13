import axios from 'axios';

const BASE_URL = ' http://127.0.0.1:8000';

export const api = {
  scrape: async (searchTerm) => {
    try {
      const response = await axios.post(`${BASE_URL}/api/scrape/`, {
        data: searchTerm
      });
      console.debug(response);
      return response.data;
    } catch (error) {
      console.error('Error in scrape API:', error);
      throw error;
    }
  },
  gettrack: async () => {
    try {
      const response = await axios.get(`${BASE_URL}/api/trackedItem/`);
      console.debug(response);
      return response.data;
    } catch (error) {
      console.error('Error in getHistory API:', error);
      throw error;
    }
  },
 addtrackItem: async (item) => {
    try {
      const response = await axios.post(`${BASE_URL}/api/trackedItem/`, {
        data: item
      });
      console.debug(response);
      return response.data;
    } catch (error) {
      console.error('Error in getHistory API:', error);
      throw error;
    }
  },
  removeTrackedItem: async (item) => {
    try {
      const response = await axios.delete(`${BASE_URL}/api/trackedItem/`, {
        data: item
      });
      console.debug(response);
      return response.data;
    } catch (error) {
      console.error('Error in getHistory API:', error);
      throw error;
    }
  }
};
