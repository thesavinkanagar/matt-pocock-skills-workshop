import { useState } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

function HeartButton({ filled, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={filled ? 'Remove from Favourites' : 'Add to Favourites'}
      aria-pressed={filled}
      className="absolute right-3 top-3 flex h-10 w-10 items-center justify-center rounded-full bg-white/90 shadow-sm transition hover:bg-white"
    >
      <svg
        viewBox="0 0 24 24"
        className={`h-5 w-5 ${filled ? 'fill-rose-500 stroke-rose-500' : 'fill-none stroke-slate-600'}`}
        strokeWidth="2"
        aria-hidden="true"
      >
        <path d="M12 21s-7.5-4.6-9.5-9.2C1 8.4 3.2 5 6.6 5c2 0 3.6 1.1 4.4 2.6h2C13.8 6.1 15.4 5 17.4 5c3.4 0 5.6 3.4 4.1 6.8C19.5 16.4 12 21 12 21z" />
      </svg>
    </button>
  );
}

export default function ProductCard({ item, onAdded, isFavourite, onFavourite, onRemove }) {
  const { refreshBasket } = useAuth();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  async function handleAdd() {
    setLoading(true);
    setMessage('');
    try {
      await api.addToBasket(item.id);
      await refreshBasket();
      setMessage('Added!');
      onAdded?.();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <article className="card flex flex-col overflow-hidden p-0 transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="relative aspect-square overflow-hidden bg-slate-100">
        <img
          src={item.picture_uri}
          alt={item.name}
          className="h-full w-full object-cover"
        />
        {onFavourite && (
          <HeartButton filled={Boolean(isFavourite)} onClick={() => onFavourite(item.id)} />
        )}
      </div>
      <div className="flex flex-1 flex-col gap-3 p-4">
        <div className="flex-1">
          <p className="text-xs font-medium uppercase tracking-wide text-indigo-600">
            {item.brand_name} · {item.type_name}
          </p>
          <h3 className="mt-1 text-lg font-semibold text-slate-900">{item.name}</h3>
          <p className="mt-2 text-sm text-slate-500 line-clamp-2">{item.description}</p>
        </div>
        <div className="flex items-center justify-between gap-3">
          <p className="text-xl font-bold text-slate-900">${item.price.toFixed(2)}</p>
          <div className="flex items-center gap-2">
            {onRemove && (
              <button
                type="button"
                onClick={() => onRemove(item.id)}
                aria-label={`Remove ${item.name} from Favourites`}
                className="btn-secondary"
              >
                Remove
              </button>
            )}
            <button
              type="button"
              onClick={handleAdd}
              disabled={loading}
              className="btn-primary"
            >
              {loading ? 'Adding...' : 'Add to basket'}
            </button>
          </div>
        </div>
        {message && <p className="text-xs font-medium text-emerald-600">{message}</p>}
      </div>
    </article>
  );
}
