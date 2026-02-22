import { Award, Users, Briefcase, TrendingUp } from 'lucide-react';
import { motion } from 'motion/react';

export function WhyUs() {
  return (
    <section className="py-24 bg-black relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-block px-4 py-2 bg-zinc-900 border border-zinc-800 rounded-full mb-6">
              <span className="text-purple-400 text-sm font-semibold">PROFESSIONAL TRADERS</span>
            </div>
            
            <h2 className="text-4xl md:text-6xl font-bold mb-6 text-white">
              Built for the 2026 Market
            </h2>
            
            <p className="text-lg text-gray-400 mb-8 leading-relaxed">
              The crypto market has evolved. Large institutions like BlackRock now dominate price action. 
              Traditional analysis no longer works. That's why we built something unique.
            </p>
            
            <div className="space-y-6">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="flex gap-4"
              >
                <div className="flex-shrink-0 w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center">
                  <Award className="w-6 h-6 text-purple-500" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Extensive Trading Experience</h3>
                  <p className="text-gray-500">Years of proven track record navigating bull and bear markets with consistent profitability.</p>
                </div>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="flex gap-4"
              >
                <div className="flex-shrink-0 w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center">
                  <Users className="w-6 h-6 text-purple-500" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Dedicated Team of Assistants</h3>
                  <p className="text-gray-500">Professional trader assistants monitoring markets 24/7 to ensure signal quality and accuracy.</p>
                </div>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="flex gap-4"
              >
                <div className="flex-shrink-0 w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center">
                  <Briefcase className="w-6 h-6 text-purple-500" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Unique Market Approach</h3>
                  <p className="text-gray-500">Proprietary strategies specifically designed for the institutional-dominated market of 2026.</p>
                </div>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="flex gap-4"
              >
                <div className="flex-shrink-0 w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-purple-500" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2">Proven Case Studies</h3>
                  <p className="text-gray-500">Real results from traders who've used our signals to achieve consistent, stable profits.</p>
                </div>
              </motion.div>
            </div>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-purple-400 rounded-2xl blur-3xl opacity-10"></div>
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
                "We detect all triggers of the largest players - their forecasts, position entries and exits, and other critical factors that move the market."
              </blockquote>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}