export default function ItemList({ items, onEdit, onDelete, disabled = false }) {
  if (!items.length) {
    return (
      <div className="card">
        <p>No items yet. Create your first item to get started.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Inventory</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Updated</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.description}</td>
              <td>{item.quantity}</td>
              <td>${Number(item.price).toFixed(2)}</td>
              <td>{new Date(item.updated_at).toLocaleString()}</td>
              <td className="actions">
                <button onClick={() => onEdit(item)} disabled={disabled}>
                  Edit
                </button>
                <button
                  className="danger"
                  onClick={() => onDelete(item.id)}
                  disabled={disabled}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
