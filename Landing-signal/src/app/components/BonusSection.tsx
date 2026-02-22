import { Gift, Star, ArrowRight } from 'lucide-react';
import { motion } from 'motion/react';

export function BonusSection() {
  return (
    <section id="bonus-section" className="py-24 bg-black relative overflow-hidden scroll-mt-24">
      <div className="absolute top-0 right-1/4 w-72 h-72 bg-purple-600/5 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-1/4 w-72 h-72 bg-purple-600/5 rounded-full blur-3xl" />

      <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="bg-zinc-950 border border-zinc-800 rounded-2xl overflow-hidden"
        >
          <div className="relative p-8 md:p-12">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl" />

            <div className="relative text-center">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-zinc-900 border border-purple-500/30 rounded-full mb-6">
                <Gift className="w-5 h-5 text-purple-400" />
                <span className="text-purple-300 font-semibold">EXCLUSIVE BONUS</span>
              </div>

              <h2 className="text-4xl md:text-6xl font-bold mb-6 text-white">
                Unlock Your Bonus Product
              </h2>

              <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto leading-relaxed">
                Subscribe to our sponsor channel and receive an additional unique product
                that will enhance your trading experience even further.
              </p>

              <div className="grid md:grid-cols-3 gap-6 mb-10">
                {[
                  { title: 'Premium Content', desc: 'Exclusive trading insights and market analysis' },
                  { title: 'Advanced Tools', desc: 'Additional analytical tools for better decisions' },
                  { title: 'Community Access', desc: 'Join our private community of successful traders' },
                ].map((item, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    className="bg-black border border-zinc-800 rounded-xl p-6"
                  >
                    <div className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                      <Star className="w-6 h-6 text-purple-500" />
                    </div>
                    <h3 className="text-lg font-semibold text-white mb-2">{item.title}</h3>
                    <p className="text-gray-500 text-sm">{item.desc}</p>
                  </motion.div>
                ))}
              </div>

              <motion.a
                href="https://t.me/futures_signalfast_bot"
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="group inline-flex items-center gap-3 px-8 py-4 bg-purple-600 hover:bg-purple-500 text-white rounded-xl font-semibold text-lg transition-all duration-300 shadow-lg shadow-purple-600/30"
              >
                Subscribe to Sponsor Channel
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </motion.a>

              <p className="text-gray-500 text-sm mt-4">
                Limited time offer • Exclusive benefits for subscribers
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
