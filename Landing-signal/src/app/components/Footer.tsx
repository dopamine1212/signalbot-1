import { Twitter, Send, MessageCircle, Mail } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-black border-t border-purple-500/20 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div className="col-span-2">
            <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-purple-600 bg-clip-text text-transparent mb-4">
              AI Trading Bot
            </h3>
            <p className="text-gray-400 mb-6 max-w-md">
              Professional-grade crypto trading signals powered by AI. 
              Track whale wallets and institutional movements in real-time.
            </p>
            <div className="flex gap-4">
              <a
                href="#"
                className="w-10 h-10 bg-purple-950/50 border border-purple-500/30 rounded-lg flex items-center justify-center hover:bg-purple-900/50 hover:border-purple-400/50 transition-all"
              >
                <Twitter className="w-5 h-5 text-purple-400" />
              </a>
              <a
                href="https://t.me/futures_signalfast_bot"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-purple-950/50 border border-purple-500/30 rounded-lg flex items-center justify-center hover:bg-purple-900/50 hover:border-purple-400/50 transition-all"
                title="Telegram Bot"
              >
                <Send className="w-5 h-5 text-purple-400" />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-purple-950/50 border border-purple-500/30 rounded-lg flex items-center justify-center hover:bg-purple-900/50 hover:border-purple-400/50 transition-all"
              >
                <MessageCircle className="w-5 h-5 text-purple-400" />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-purple-950/50 border border-purple-500/30 rounded-lg flex items-center justify-center hover:bg-purple-900/50 hover:border-purple-400/50 transition-all"
              >
                <Mail className="w-5 h-5 text-purple-400" />
              </a>
            </div>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-4">Product</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Features</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Pricing</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">FAQ</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Demo</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-semibold mb-4">Company</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">About Us</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Contact</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Terms of Service</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Privacy Policy</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-purple-500/20 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-400 text-sm">
              © 2026 AI Trading Bot. All rights reserved.
            </p>
            <p className="text-gray-500 text-sm">
              Trading cryptocurrencies carries risk. Past performance does not guarantee future results.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
