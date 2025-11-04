import axios from "axios";

const baseURL =
  import.meta.env.VITE_API_BASE_URL?.trim() || "http://localhost:8000";

const client = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getItems = async () => {
  const response = await client.get("/items");
  return response.data;
};

export const createItem = async (payload) => {
  const response = await client.post("/items", payload);
  return response.data;
};

export const updateItem = async (id, payload) => {
  const response = await client.put(`/items/${id}`, payload);
  return response.data;
};

export const deleteItem = async (id) => {
  await client.delete(`/items/${id}`);
};
