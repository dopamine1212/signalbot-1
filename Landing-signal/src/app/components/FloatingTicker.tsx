import { TrendingUp, TrendingDown } from 'lucide-react';

export function FloatingTicker() {
  const cryptoData = [
    { symbol: 'BTC', change: '+5.2%', trending: 'up' },
    { symbol: 'ETH', change: '+3.8%', trending: 'up' },
    { symbol: 'SOL', change: '-1.2%', trending: 'down' },
    { symbol: 'BNB', change: '+2.4%', trending: 'up' },
    { symbol: 'XRP', change: '+8.7%', trending: 'up' },
    { symbol: 'ADA', change: '-0.5%', trending: 'down' },
    { symbol: 'AVAX', change: '+4.1%', trending: 'up' },
    { symbol: 'DOT', change: '+1.9%', trending: 'up' },
    { symbol: 'MATIC', change: '+6.3%', trending: 'up' },
    { symbol: 'LINK', change: '-2.1%', trending: 'down' },
    { symbol: 'UNI', change: '+3.5%', trending: 'up' },
    { symbol: 'ATOM', change: '+2.8%', trending: 'up' },
  ];

  const items = [...cryptoData, ...cryptoData, ...cryptoData];

  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-black/90 backdrop-blur-md border-b border-zinc-800/50 overflow-hidden">
      <div className="relative flex">
        <div className="flex gap-8 py-3 animate-ticker">
          {items.map((crypto, index) => (
            <div
              key={index}
              className="flex items-center gap-2 whitespace-nowrap px-2 flex-shrink-0"
            >
              <span className="text-white font-semibold text-sm">
                {crypto.symbol}
              </span>
              <span
                className={`flex items-center gap-1 text-sm font-semibold ${
                  crypto.trending === 'up' ? 'text-green-400' : 'text-red-400'
                }`}
              >
                {crypto.trending === 'up' ? (
                  <TrendingUp className="w-3 h-3" />
                ) : (
                  <TrendingDown className="w-3 h-3" />
                )}
                {crypto.change}
              </span>
              <div className="w-px h-4 bg-zinc-700 ml-4" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}