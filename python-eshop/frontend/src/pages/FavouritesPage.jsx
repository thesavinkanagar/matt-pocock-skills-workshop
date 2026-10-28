import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import ProductCard from '../components/ProductCard';
import { useAuth } from '../context/AuthContext';

export default function FavouritesPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [favourites, setFavourites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/favourites' } });
      return;
    }

    api
      .getFavourites()
      .then(setFavourites)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [isAuthenticated, navigate]);

  async function handleRemove(productId) {
    try {
      await api.removeFavourite(productId);
      setFavourites((current) => current.filter((item) => item.id !== productId));
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) {
    return <p className="text-center text-slate-500">Loading favourites...</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">My Favourites</h1>
        <p className="mt-1 text-slate-500">Products you saved to come back to, newest first.</p>
      </div>

      {error && <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>}

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {favourites.map((item) => (
          <ProductCard key={item.id} item={item} onRemove={handleRemove} />
        ))}
      </div>
    </div>
  );
}
