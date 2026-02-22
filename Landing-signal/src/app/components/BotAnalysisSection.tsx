import React from 'react';
import { motion } from 'motion/react';
import { Database, Brain, Bell, TrendingUp, ArrowRight } from 'lucide-react';

const STEPS = [
  {
    icon: Database,
    title: 'Data Collection',
    desc: 'Exchanges, whale wallets, funding, volume',
  },
  {
    icon: Brain,
    title: 'AI Analysis',
    desc: 'Model scores setups and signal strength',
  },
  {
    icon: Bell,
    title: 'Signals in Bot',
    desc: 'You get Long/Short in Telegram',
  },
  {
    icon: TrendingUp,
    title: 'Trading',
    desc: 'Entry, take-profit and stop-loss at our levels',
  },
];

export function BotAnalysisSection() {
  return (
    <section className="py-16 md:py-20 bg-black relative overflow-hidden">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff02_1px,transparent_1px),linear-gradient(to_bottom,#ffffff02_1px,transparent_1px)] bg-[size:3rem_3rem]" />
      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-14"
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-3">
            How the Bot Analyzes the Market
          </h2>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto">
            From raw data to ready signals in your Telegram
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-4">
          {STEPS.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="relative"
            >
              <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 h-full flex flex-col items-center text-center hover:border-purple-500/40 transition-colors">
                <div className="w-14 h-14 rounded-xl bg-purple-600/20 flex items-center justify-center mb-4">
                  <step.icon className="w-7 h-7 text-purple-400" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{step.title}</h3>
                <p className="text-gray-500 text-sm">{step.desc}</p>
              </div>
              {i < STEPS.length - 1 && (
                <div className="hidden lg:flex absolute top-1/2 -right-2 lg:-right-3 z-10 -translate-y-1/2 text-purple-500/60">
                  <ArrowRight className="w-5 h-5" />
                </div>
              )}
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-10 flex flex-wrap justify-center gap-4 text-sm text-gray-500"
        >
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Whale wallets</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Funding rates</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Order book</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Liquidations</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Sentiment</span>
        </motion.div>
      </div>
    </section>
  );
}
