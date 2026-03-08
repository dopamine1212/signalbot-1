import { ArrowRight, Sparkles } from 'lucide-react';
import { motion } from 'motion/react';
import { AnimatedCounter } from '@/app/components/AnimatedCounter';
import { MagneticButton } from '@/app/components/MagneticButton';
import FlowFieldBackground from '@/app/components/ui/flow-field-background';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-black">
      <FlowFieldBackground
        className="absolute inset-0 z-0"
        color="#a855f7"
        trailOpacity={0.1}
        particleCount={500}
        speed={0.8}
      />
      <div className="absolute inset-0 z-[1] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-950/20 via-transparent to-transparent pointer-events-none" />
      <div className="absolute inset-0 z-[1] bg-[linear-gradient(to_right,#ffffff03_1px,transparent_1px),linear-gradient(to_bottom,#ffffff03_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,#000_70%,transparent_100%)] pointer-events-none" />
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl animate-hero-orb z-[1] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-hero-orb-slow z-[1] pointer-events-none" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-zinc-900 border border-zinc-800 mb-8"
        >
          <Sparkles className="w-4 h-4 text-purple-400" />
          <span className="text-sm text-gray-300">Trusted by 1,000+ Professional Traders</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 tracking-tight"
        >
          <span className="text-white">AI-Powered</span>
          <br />
          <span className="bg-gradient-to-r from-white via-gray-300 to-purple-400 bg-clip-text text-transparent inline-block animate-hero-float">
            Futures Trading Signals
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="text-xl md:text-2xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed"
        >
          Track BlackRock and institutional whales. Get high-conviction crypto signals
          with advanced AI analysis. Built by professional traders.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <MagneticButton href="bonus" className="group px-8 py-4 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white rounded-xl font-semibold text-lg transition-all duration-300 flex items-center gap-2 shadow-lg shadow-purple-600/30 hover:shadow-purple-500/50 relative overflow-hidden">
            <span className="relative z-10">Start Trading Now</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform relative z-10" />
          </MagneticButton>

          <MagneticButton href="products" className="px-8 py-4 bg-zinc-900 border border-zinc-800 hover:border-purple-500/50 text-white rounded-xl font-semibold text-lg transition-all duration-300 hover:bg-zinc-800">
            Other Products
          </MagneticButton>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
          className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
        >
          <div className="text-center">
            <div className="text-4xl md:text-5xl font-bold text-white mb-2">
              <AnimatedCounter end={1000} suffix="+" />
            </div>
            <div className="text-sm text-gray-500 uppercase tracking-wider">Active Users</div>
          </div>
          <div className="text-center">
            <div className="text-4xl md:text-5xl font-bold text-white mb-2">
              <AnimatedCounter end={87} suffix="%" />
            </div>
            <div className="text-sm text-gray-500 uppercase tracking-wider">Win Rate</div>
          </div>
          <div className="text-center">
            <div className="text-4xl md:text-5xl font-bold text-white mb-2">
              $<AnimatedCounter end={24} />
            </div>
            <div className="text-sm text-gray-500 uppercase tracking-wider">3 Months</div>
          </div>
          <div className="text-center">
            <div className="text-4xl md:text-5xl font-bold text-white mb-2">24/7</div>
            <div className="text-sm text-gray-500 uppercase tracking-wider">AI Monitoring</div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
