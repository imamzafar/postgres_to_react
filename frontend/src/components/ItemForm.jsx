import { useEffect, useState } from "react";

const emptyState = {
  name: "",
  description: "",
  quantity: 0,
  price: 0,
};

export default function ItemForm({
  onSubmit,
  onCancel,
  editingItem,
  disabled = false,
}) {
  const [formValues, setFormValues] = useState(emptyState);

  useEffect(() => {
    if (editingItem) {
      setFormValues({
        name: editingItem.name ?? "",
        description: editingItem.description ?? "",
        quantity: editingItem.quantity ?? 0,
        price: editingItem.price ?? 0,
      });
    } else {
      setFormValues(emptyState);
    }
  }, [editingItem]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormValues((current) => ({
      ...current,
      [name]: name === "quantity" || name === "price" ? Number(value) : value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(formValues);
  };

  const isEditing = Boolean(editingItem);
  const submitLabel = disabled
    ? isEditing
      ? "Saving..."
      : "Creating..."
    : isEditing
    ? "Save Changes"
    : "Create Item";

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h2>{isEditing ? "Update Item" : "Add New Item"}</h2>
      <label>
        Name
        <input
          name="name"
          type="text"
          value={formValues.name}
          onChange={handleChange}
          required
          disabled={disabled}
        />
      </label>
      <label>
        Description
        <textarea
          name="description"
          value={formValues.description}
          onChange={handleChange}
          disabled={disabled}
        />
      </label>
      <label>
        Quantity
        <input
          name="quantity"
          type="number"
          min="0"
          value={formValues.quantity}
          onChange={handleChange}
          required
          disabled={disabled}
        />
      </label>
      <label>
        Price
        <input
          name="price"
          type="number"
          min="0"
          step="0.01"
          value={formValues.price}
          onChange={handleChange}
          required
          disabled={disabled}
        />
      </label>
      <div className="form-actions">
        <button type="submit" className="primary" disabled={disabled}>
          {submitLabel}
        </button>
        {isEditing && (
          <button type="button" onClick={onCancel} disabled={disabled}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
