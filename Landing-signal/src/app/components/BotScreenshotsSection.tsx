import { motion } from 'motion/react';
import { ExternalLink, Send } from 'lucide-react';

const BOT_LINK = 'https://t.me/futures_signalfast_bot';

const MESSAGES = [
  { text: '📊 BTCUSDT Long 97.2k — 98.5k. SL 96.8k', out: false, time: '14:32' },
  { text: 'Signal opened. Waiting for target.', out: true, time: '14:33' },
  { text: '✅ Target hit +1.3%', out: false, time: '14:41' },
];

const SCREENSHOTS = [
  {
    title: 'Signal Feed',
    desc: 'Long/Short with entry and stop levels',
    placeholder: 'chart',
  },
  {
    title: 'Trading Panel',
    desc: 'Positions and trade history',
    placeholder: 'trading',
  },
  {
    title: 'Bot Analytics',
    desc: 'Stats and win rate',
    placeholder: 'stats',
  },
];

function ScreenshotCard({
  title,
  desc,
  placeholder,
  index,
}: {
  title: string;
  desc: string;
  placeholder: string;
  index: number;
}) {
  return (
    <motion.a
      href={BOT_LINK}
      target="_blank"
      rel="noopener noreferrer"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1 }}
      className="group block rounded-xl border border-zinc-800 overflow-hidden bg-zinc-950 hover:border-purple-500/50 transition-all"
    >
      <div className="aspect-[4/3] bg-zinc-900 flex items-center justify-center relative">
        <div className="w-16 h-16 rounded-xl bg-purple-600/20 flex items-center justify-center">
          <span className="text-2xl text-purple-400">
            {placeholder === 'chart' ? '📈' : placeholder === 'trading' ? '⚡' : '📊'}
          </span>
        </div>
        <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <span className="inline-flex items-center gap-1 text-xs text-purple-400 bg-black/60 px-2 py-1 rounded">
            <ExternalLink className="w-3 h-3" /> Open bot
          </span>
        </div>
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-white mb-1">{title}</h3>
        <p className="text-sm text-gray-500">{desc}</p>
      </div>
    </motion.a>
  );
}

export function BotScreenshotsSection() {
  return (
    <section className="py-16 md:py-20 bg-black relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-32 bg-gradient-to-b from-[#2aabee]/10 to-transparent" />
      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#2aabee]/10 border border-[#2aabee]/30 mb-4">
            <Send className="w-4 h-4 text-[#2aabee]" />
            <span className="text-sm text-[#2aabee]">All in One Bot</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-3">
            Bot Screenshots
          </h2>
          <p className="text-gray-500 text-lg">
            Click any card and open the bot in Telegram
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl border border-zinc-800 overflow-hidden bg-[#1c1c24] shadow-2xl max-w-md mx-auto mb-10"
        >
          <div className="flex items-center gap-3 px-4 py-3 bg-[#2aabee]/10 border-b border-zinc-800">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-purple-700 flex items-center justify-center">
              <span className="text-white font-bold text-sm">TB</span>
            </div>
            <div className="flex-1">
              <p className="font-semibold text-white">Trading Bot</p>
              <p className="text-xs text-gray-500">online</p>
            </div>
          </div>
          <div className="p-4 space-y-3 min-h-[200px]">
            {MESSAGES.map((msg, i) => (
              <div key={i} className={`flex ${msg.out ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-2.5 ${
                    msg.out ? 'bg-[#2aabee] text-white rounded-br-md' : 'bg-zinc-800 text-gray-100 rounded-bl-md'
                  }`}
                >
                  <p className="text-sm">{msg.text}</p>
                  <p className={`text-[10px] mt-1 ${msg.out ? 'text-blue-200' : 'text-gray-500'}`}>{msg.time}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {SCREENSHOTS.map((s, i) => (
            <ScreenshotCard
              key={s.title}
              title={s.title}
              desc={s.desc}
              placeholder={s.placeholder}
              index={i}
            />
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center mt-8"
        >
          <a
            href={BOT_LINK}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-purple-400 hover:text-purple-300 font-medium"
          >
            <ExternalLink className="w-4 h-4" />
            Open Bot
          </a>
        </motion.div>
      </div>
    </section>
  );
}
