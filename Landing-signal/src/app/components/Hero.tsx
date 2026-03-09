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
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-zinc-900 border border-zinc-800 mb-6"
        >
          <Sparkles className="w-4 h-4 text-purple-400" />
          <span className="text-sm text-gray-300">TomSawyer AI Futures bot</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1 }}
          className="text-4xl md:text-6xl lg:text-7xl font-bold mb-4 tracking-tight"
        >
          <span className="bg-gradient-to-r from-white via-gray-300 to-purple-400 bg-clip-text text-transparent inline-block animate-hero-float">
            Your AI-powered trading assistant
          </span>
          <br />
          <span className="text-white">for crypto futures</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.25 }}
          className="text-lg md:text-2xl text-gray-300 mb-4 max-w-3xl mx-auto leading-relaxed"
        >
          Track BlackRock and institutional whales. Receive high-conviction crypto futures signals directly in Telegram
          with advanced AI analysis. Built by professional traders.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <MagneticButton
            href="bot"
            className="group px-8 py-4 bg-[#229ED9] hover:bg-[#1c8ac0] text-white rounded-xl font-semibold text-lg transition-all duration-300 flex items-center gap-2 shadow-lg shadow-sky-600/40 hover:shadow-sky-500/60 relative overflow-hidden"
          >
            <span className="relative z-10">🚀 Start Trading bot</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform relative z-10" />
          </MagneticButton>

          <MagneticButton
            href="https://t.me/SaawyerCrypto"
            className="px-8 py-4 bg-zinc-900 border border-zinc-800 hover:border-sky-500/60 text-white rounded-xl font-semibold text-lg transition-all duration-300 hover:bg-zinc-800"
          >
            Join channel
          </MagneticButton>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.6 }}
          className="mt-10 flex justify-center"
        >
          <div className="relative w-full max-w-xs md:max-w-sm rounded-[32px] border border-zinc-800 bg-zinc-950/90 shadow-[0_0_40px_rgba(0,0,0,0.7)] overflow-hidden">
            <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800/80 bg-zinc-900/80">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-purple-500 to-sky-400 flex items-center justify-center text-xs font-bold">
                  TS
                </div>
                <div className="text-left">
                  <div className="text-sm font-semibold text-white">TomSawyer AI Futures bot</div>
                  <div className="text-[11px] text-gray-500">AI signals · Telegram</div>
                </div>
              </div>
              <span className="text-[11px] text-gray-500">now</span>
            </div>
            <div className="px-4 py-4 space-y-3 text-left text-sm">
              <p className="text-gray-300">
                📉 <span className="font-semibold">Open SHORT</span> at 2107.2 – 2130.5, leverage X25, 2% of deposit.
              </p>
              <p className="text-gray-400">
                🎯 Targets: 2090.3 · 2081.8 · 2063.2 · 2042.1 · 2009.9
              </p>
              <p className="text-gray-400">❗️ Stop-loss: 2200.34</p>
              <div className="mt-2 rounded-xl bg-zinc-900/80 border border-zinc-800 px-3 py-2 text-[11px] text-gray-400">
                The bot tracks BlackRock & whales and sends you high-conviction crypto futures setups in real time.
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.9 }}
          className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
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
