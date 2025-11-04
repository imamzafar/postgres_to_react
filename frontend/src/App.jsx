import { useEffect, useState } from "react";

import {
  createItem,
  deleteItem,
  getItems,
  updateItem,
} from "./api.js";
import ItemForm from "./components/ItemForm.jsx";
import ItemList from "./components/ItemList.jsx";

export default function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    refreshItems();
  }, []);

  const refreshItems = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getItems();
      setItems(data);
    } catch (err) {
      setError(err.message || "Failed to load items");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateOrUpdate = async (payload) => {
    try {
      setSubmitting(true);
      setError(null);
      if (selectedItem) {
        await updateItem(selectedItem.id, payload);
      } else {
        await createItem(payload);
      }
      setSelectedItem(null);
      await refreshItems();
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Request failed");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this item?")) {
      return;
    }
    try {
      setSubmitting(true);
      setError(null);
      await deleteItem(id);
      await refreshItems();
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Delete failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Inventory Manager</h1>
        <p>
          Full CRUD example using FastAPI, PostgreSQL, and React. Manage your
          inventory items below.
        </p>
      </header>

      {error && <div className="alert">{error}</div>}

      <ItemForm
        editingItem={selectedItem}
        onSubmit={handleCreateOrUpdate}
        onCancel={() => setSelectedItem(null)}
        disabled={submitting}
      />

      {loading ? (
        <div className="card">Loading items...</div>
      ) : (
        <ItemList
          items={items}
          onEdit={setSelectedItem}
          onDelete={handleDelete}
          disabled={submitting}
        />
      )}
    </div>
  );
}
