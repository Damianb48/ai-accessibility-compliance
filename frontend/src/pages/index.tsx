import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [scanId, setScanId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg);
      }
      const data = await res.json();
      setScanId(data.id);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <h1 className="text-3xl font-extrabold text-gray-900 mb-4">AI‑Powered Accessibility Compliance</h1>
      <p className="text-gray-600 mb-8 text-center max-w-xl">
        Wprowadź adres URL swojej strony, aby wygenerować raport dostępności. Narzędzie wykona skan przy użyciu
        zaawansowanego audytu (axe‑core/Pa11y) i wygeneruje PDF/JSON z wynikami.
      </p>
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4">
        <input
          type="url"
          required
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {loading ? 'Przetwarzanie…' : 'Rozpocznij skan'}
        </button>
      </form>
      {scanId && (
        <p className="mt-6 text-green-600">Twój skan zostal zapisany z identyfikatorem {scanId}. Mozesz sprawdzic status w panelu uzytkownika.</p>
      )}
      {error && (
        <p className="mt-6 text-red-600">Wystąpił błąd: {error}</p>
      )}
    </div>
  );
}
