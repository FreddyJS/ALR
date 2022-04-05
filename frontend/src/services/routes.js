import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL;

const getRoutes = async () => {
  const response = await axios.get(`${baseURL}routes`);
  return response.data;
}

export { getRoutes };