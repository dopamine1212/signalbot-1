import React from 'react';
import { Check, Zap } from 'lucide-react';
import { motion } from 'motion/react';
import { MagneticButton } from '@/app/components/MagneticButton';

const PLANS = [
  {
    name: 'Monthly',
    price: 24,
    period: '/ month',
    description: 'Flexible start',
    features: ['All signals', '24/7 AI analysis', 'Whale tracking', 'Cancel anytime'],
    cta: 'Start now',
    popular: false,
  },
  {
    name: '6 Months',
    price: 100,
    period: '/ 6 months',
    save: 'Save 30%',
    description: 'Best value',
    features: ['Everything in Monthly', 'Priority support', 'Extended history', 'Best for active traders'],
    cta: 'Get 6 months',
    popular: true,
  },
  {
    name: 'Yearly',
    price: 200,
    period: '/ year',
    save: 'Save 31%',
    description: 'Maximum savings',
    features: ['Everything in 6 months', 'VIP channel access', 'Early feature access', 'Dedicated manager'],
    cta: 'Get 1 year',
    popular: false,
  },
];

export function Pricing() {
  return (
    <section className="py-16 md:py-20 bg-black relative overflow-visible">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-600/10 rounded-full blur-[120px] opacity-10 pointer-events-none" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 sm:pt-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-3 text-white">
            Transparent Pricing
          </h2>
          <p className="text-base sm:text-lg text-gray-500">
            $24 / month · $100 / 6 months · $200 / year
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {PLANS.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className={`relative rounded-2xl border p-6 md:p-8 flex flex-col ${
                plan.popular
                  ? 'bg-gradient-to-br from-zinc-950 to-black border-purple-500/50 shadow-lg shadow-purple-500/20'
                  : 'bg-zinc-950/80 border-zinc-800'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-20">
                  <div className="px-3 py-1 sm:px-4 sm:py-1.5 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center gap-1.5 shadow-lg shadow-purple-500/50">
                    <Zap className="w-3 h-3 text-white" />
                    <span className="text-white font-semibold text-[10px] sm:text-xs whitespace-nowrap">MOST POPULAR</span>
                  </div>
                </div>
              )}
              {plan.save && (
                <span className="absolute top-4 right-4 text-xs font-medium text-green-400 bg-green-500/10 px-2 py-0.5 rounded">
                  {plan.save}
                </span>
              )}
              <div className="pt-2">
                <h3 className="text-lg font-semibold text-white mb-1">{plan.name}</h3>
                <p className="text-gray-500 text-sm mb-4">{plan.description}</p>
                <div className="flex items-baseline gap-1 mb-4">
                  <span className="text-4xl md:text-5xl font-bold text-white">${plan.price}</span>
                  <span className="text-gray-500">{plan.period}</span>
                </div>
                <ul className="space-y-2.5 mb-6">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-gray-300">
                      <Check className="w-4 h-4 text-purple-400 flex-shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
                <MagneticButton
                  href="bot"
                  className={`w-full py-3 rounded-xl font-semibold text-sm transition-all ${
                    plan.popular
                      ? 'bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white shadow-lg shadow-purple-600/30'
                      : 'bg-zinc-800 border border-zinc-700 hover:border-purple-500/50 text-white'
                  }`}
                >
                  {plan.cta}
                </MagneticButton>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center text-gray-500 text-sm mt-8"
        >
          + 50% profit sharing on profits · Cancel anytime
        </motion.p>
      </div>
    </section>
  );
}
