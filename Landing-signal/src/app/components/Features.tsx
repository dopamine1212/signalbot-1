import { Brain, TrendingUp, Bell, Shield, Zap, Target } from 'lucide-react';
import { motion } from 'motion/react';

export function Features() {
  const features = [
    {
      icon: Brain,
      title: 'Advanced AI Analysis',
      description: 'Our bot uses cutting-edge artificial intelligence to analyze market patterns, whale movements, and institutional trading behaviors in real-time.',
    },
    {
      icon: Target,
      title: 'Whale Wallet Tracking',
      description: 'Monitor specific wallets of major players like BlackRock and other market manipulators to detect entry and exit positions before the crowd.',
    },
    {
      icon: Bell,
      title: 'Advance Signal Alerts',
      description: 'Receive high-quality trading signals with advance warnings, giving you time to prepare and execute trades strategically.',
    },
    {
      icon: TrendingUp,
      title: 'Multi-Platform Monitoring',
      description: 'Comprehensive analysis across exchanges, platforms, and social media to capture every market-moving trigger and sentiment shift.',
    },
    {
      icon: Shield,
      title: 'Professional Team',
      description: 'Backed by experienced traders with extensive market knowledge and unique strategies developed through years of successful trading.',
    },
    {
      icon: Zap,
      title: 'Real-Time Execution',
      description: 'Lightning-fast signal delivery ensures you never miss critical market opportunities, even during high volatility periods.',
    },
  ];

  return (
    <section id="products-section" className="py-24 bg-black relative overflow-hidden">
      <motion.div
        className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-purple-600/10 rounded-full blur-[120px]"
        animate={{
          scale: [1, 1.2, 1],
          x: [0, 50, 0],
          opacity: [0.05, 0.1, 0.05],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      <motion.div
        className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-purple-600/10 rounded-full blur-[120px]"
        animate={{
          scale: [1, 1.3, 1],
          x: [0, -50, 0],
          opacity: [0.05, 0.15, 0.05],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 1,
        }}
      />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-6xl font-bold mb-4 text-white">
            Professional-Grade Intelligence
          </h2>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto">
            Tools and insights that institutional traders use
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{
                y: -8,
                transition: { duration: 0.3 },
              }}
              className="group p-6 bg-zinc-950 border border-zinc-800 rounded-xl hover:border-purple-500/50 transition-all duration-300 relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-purple-600/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <motion.div
                className="w-12 h-12 bg-zinc-900 rounded-lg flex items-center justify-center mb-4 group-hover:bg-purple-600/20 transition-all duration-300 relative z-10"
                whileHover={{ rotate: 360, scale: 1.1 }}
                transition={{ duration: 0.6 }}
              >
                <feature.icon className="w-6 h-6 text-purple-500 group-hover:text-purple-400 transition-colors" />
              </motion.div>
              <h3 className="text-xl font-semibold mb-3 text-white relative z-10">{feature.title}</h3>
              <p className="text-gray-500 leading-relaxed relative z-10">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
