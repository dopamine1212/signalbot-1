import { motion } from 'motion/react';

export function MarketEvolutionSection() {
  return (
    <section className="py-20 bg-black relative">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="relative"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-purple-400 rounded-2xl blur-3xl opacity-10" />
          <div className="relative bg-zinc-950 border border-zinc-800 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-white mb-6">Market Evolution</h3>

            <div className="space-y-4 mb-8">
              <div className="bg-black border border-zinc-800 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-500">2024 Market</span>
                  <span className="text-gray-400 font-semibold">Retail Driven</span>
                </div>
                <div className="w-full bg-zinc-900 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    whileInView={{ width: '45%' }}
                    viewport={{ once: true }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className="bg-zinc-700 h-2 rounded-full"
                  />
                </div>
              </div>

              <div className="bg-black border border-zinc-800 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-500">2026 Market</span>
                  <span className="text-purple-400 font-semibold">Institutional</span>
                </div>
                <div className="w-full bg-zinc-900 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    whileInView={{ width: '90%' }}
                    viewport={{ once: true }}
                    transition={{ duration: 1, delay: 0.7 }}
                    className="bg-gradient-to-r from-purple-600 to-purple-400 h-2 rounded-full"
                  />
                </div>
              </div>
            </div>

            <blockquote className="border-l-4 border-purple-500 pl-4 italic text-gray-400">
              &quot;We detect all triggers of the largest players – their forecasts, position entries and exits, and other
              critical factors that move the market.&quot;
            </blockquote>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

