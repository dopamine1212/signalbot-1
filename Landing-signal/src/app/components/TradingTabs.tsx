import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { MagneticButton } from '@/app/components/MagneticButton';

export function TradingTabs() {
  const [activeTab, setActiveTab] = useState(0);
  const [direction, setDirection] = useState(0);

  const tabs = [
    {
      id: 0,
      label: '1️⃣ Futures Trading',
      title: 'Futures Trading',
      description: 'Signals for active futures trading with built-in risk management.',
      features: [
        'AI-powered entry and exit levels',
        'Leverage and volatility-aware setup selection',
        'Integrated with the TomSawyer Telegram ecosystem'
      ],
      stats: { accuracy: '87%', trades: '350+', profit: '156%' }
    },
    {
      id: 1,
      label: '2️⃣ Spot Signals',
      title: 'Spot Signals',
      description: 'Real signals for spot trading with fast entries and exits.',
      features: [
        'Whale accumulation and distribution detection',
        'Clear spot entry and exit zones',
        'Built for traders who prefer no leverage'
      ],
      stats: { accuracy: '82%', trades: '420+', profit: '124%' }
    },
    {
      id: 2,
      label: '3️⃣ Scalping',
      title: 'Scalping',
      description: 'Short-term signals for quick profit opportunities.',
      features: [
        'Fast intraday setups for active execution',
        'Micro-movement signal logic',
        'Made for high-frequency decision makers'
      ],
      stats: { accuracy: '79%', trades: '1200+', profit: '98%' }
    },
    {
      id: 3,
      label: '4️⃣ Swing Trading',
      title: 'Swing Trading',
      description: 'Medium-term strategies to maximize profits in volatile markets.',
      features: [
        'Multi-day positions for bigger market moves',
        'Trend reversal and continuation focus',
        'Great for users who trade less often with higher conviction'
      ],
      stats: { accuracy: '91%', trades: '85+', profit: '203%' }
    }
  ];

  const activeContent = tabs[activeTab];

  const handleTabChange = (newTab: number) => {
    setDirection(newTab > activeTab ? 1 : -1);
    setActiveTab(newTab);
  };

  return (
    <section className="py-24 bg-black relative overflow-hidden">
      {/* Enhanced background effects with animation */}
      <motion.div 
        className="absolute top-1/4 right-0 w-[600px] h-[600px] bg-purple-600/10 rounded-full blur-[100px]"
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.1, 0.2, 0.1],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <motion.div 
        className="absolute bottom-1/4 left-0 w-[600px] h-[600px] bg-purple-600/10 rounded-full blur-[100px]"
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.1, 0.15, 0.1],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
      />

      {/* Animated grid pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#8b5cf605_1px,transparent_1px),linear-gradient(to_bottom,#8b5cf605_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_40%,transparent_100%)]"></div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <motion.div
            className="inline-block mb-4"
            initial={{ opacity: 0, scale: 0.5 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="px-4 py-2 rounded-full bg-purple-950/30 border border-purple-500/20 text-purple-300 text-sm">
              🔹 Main trading styles
            </div>
          </motion.div>
          <h2 className="text-3xl md:text-5xl font-bold mb-3 text-white">
            With TomSawyer you choose your trading style
          </h2>
          <p className="text-base md:text-lg text-gray-400 max-w-3xl mx-auto">
            Below are the core approaches - find the strategy that fits you best.
          </p>
        </motion.div>

        {/* Compact tabs to reduce vertical space */}
        <div className="flex flex-wrap justify-center gap-2 mb-6 max-w-3xl mx-auto">
          {tabs.map((tab, index) => {
            const isActive = activeTab === tab.id;
            return (
              <motion.div
                key={tab.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
              >
                <MagneticButton
                  onClick={() => handleTabChange(tab.id)}
                  className={`relative px-4 py-2.5 rounded-xl font-semibold text-sm transition-all duration-500 flex items-center gap-2 overflow-hidden group ${
                    isActive
                      ? 'bg-gradient-to-r from-purple-600 to-purple-500 text-white shadow-xl shadow-purple-500/50'
                      : 'bg-zinc-900/50 text-gray-400 hover:bg-zinc-800 hover:text-white border border-zinc-800 hover:border-purple-500/30'
                  }`}
                >
                  {/* Animated background for active tab */}
                  {isActive && (
                    <>
                      <motion.div
                        layoutId="activeTabBg"
                        className="absolute inset-0 bg-gradient-to-r from-purple-600 to-purple-500"
                        transition={{ type: 'spring', bounce: 0.15, duration: 0.8 }}
                      />
                      <motion.div
                        className="absolute inset-0 opacity-50"
                        animate={{
                          background: [
                            'radial-gradient(circle at 0% 0%, rgba(255,255,255,0.3) 0%, transparent 50%)',
                            'radial-gradient(circle at 100% 100%, rgba(255,255,255,0.3) 0%, transparent 50%)',
                            'radial-gradient(circle at 0% 0%, rgba(255,255,255,0.3) 0%, transparent 50%)',
                          ],
                        }}
                        transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                      />
                    </>
                  )}

                  <span className="relative z-10">{tab.label}</span>

                  {/* Hover glow effect for inactive tabs */}
                  {!isActive && (
                    <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                      <div className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-purple-500/10 rounded-xl" />
                    </div>
                  )}
                </MagneticButton>
              </motion.div>
            );
          })}
        </div>

        {/* Enhanced Tab content with advanced animations */}
        <AnimatePresence mode="wait" custom={direction}>
          <motion.div
            key={activeTab}
            custom={direction}
            initial={{ 
              opacity: 0, 
              x: direction > 0 ? 100 : -100,
              rotateY: direction > 0 ? 15 : -15,
              scale: 0.95
            }}
            animate={{ 
              opacity: 1, 
              x: 0,
              rotateY: 0,
              scale: 1
            }}
            exit={{ 
              opacity: 0, 
              x: direction > 0 ? -100 : 100,
              rotateY: direction > 0 ? -15 : 15,
              scale: 0.95
            }}
            transition={{ 
              duration: 0.7,
              type: "spring",
              bounce: 0.15
            }}
            className="bg-gradient-to-br from-zinc-950 to-black border border-zinc-800 rounded-2xl overflow-hidden relative"
            style={{ perspective: 1000 }}
          >
            {/* Animated border glow */}
            <motion.div
              className="absolute inset-0 opacity-50"
              animate={{
                background: [
                  'linear-gradient(0deg, rgba(168, 85, 247, 0.1) 0%, transparent 100%)',
                  'linear-gradient(90deg, rgba(168, 85, 247, 0.1) 0%, transparent 100%)',
                  'linear-gradient(180deg, rgba(168, 85, 247, 0.1) 0%, transparent 100%)',
                  'linear-gradient(270deg, rgba(168, 85, 247, 0.1) 0%, transparent 100%)',
                  'linear-gradient(360deg, rgba(168, 85, 247, 0.1) 0%, transparent 100%)',
                ],
              }}
              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            />

            <div className="grid lg:grid-cols-2 gap-8 p-8 md:p-12 relative z-10">
              {/* Left side - Content with staggered animations */}
              <div>
                <motion.h3 
                  className="text-3xl md:text-4xl font-bold text-white mb-4"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1, duration: 0.5 }}
                >
                  {activeContent.title}
                </motion.h3>
                <motion.p 
                  className="text-lg text-gray-400 mb-8 leading-relaxed"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2, duration: 0.5 }}
                >
                  {activeContent.description}
                </motion.p>

                <div className="space-y-3 mb-8">
                  {activeContent.features.map((feature, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -30 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ 
                        delay: 0.3 + index * 0.08,
                        duration: 0.5,
                        type: "spring",
                        stiffness: 100
                      }}
                      className="flex items-center gap-3 text-gray-300 group"
                    >
                      <motion.div 
                        className="w-2 h-2 bg-purple-500 rounded-full"
                        whileHover={{ scale: 1.5, boxShadow: "0 0 10px rgba(168, 85, 247, 0.8)" }}
                        transition={{ duration: 0.2 }}
                      />
                      <span className="group-hover:text-white transition-colors duration-300">
                        {feature}
                      </span>
                    </motion.div>
                  ))}
                </div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8, duration: 0.5 }}
                >
                  <MagneticButton
                    href="bonus"
                    className="px-8 py-4 bg-gradient-to-r from-purple-600 to-purple-500 hover:from-purple-500 hover:to-purple-400 text-white rounded-xl font-semibold transition-all duration-300 shadow-lg shadow-purple-600/30 hover:shadow-purple-500/50 relative overflow-hidden group"
                  >
                    <motion.div
                      className="absolute inset-0 bg-white opacity-0 group-hover:opacity-20"
                      initial={false}
                      animate={{
                        x: ['-100%', '100%'],
                      }}
                      transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        repeatDelay: 1,
                      }}
                    />
                    <span className="relative z-10">🚀 Start using TomSawyer AI Bot</span>
                  </MagneticButton>
                </motion.div>
              </div>

              {/* Right side - Stats with enhanced animations */}
              <div className="flex flex-col justify-center">
                <motion.div 
                  className="bg-black/50 border border-zinc-800 rounded-xl p-8 relative overflow-hidden"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.4, duration: 0.6 }}
                >
                  {/* Animated corner accents */}
                  <motion.div
                    className="absolute top-0 right-0 w-20 h-20 bg-purple-500/10 blur-2xl"
                    animate={{
                      scale: [1, 1.5, 1],
                      opacity: [0.3, 0.6, 0.3],
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  />
                  
                  <motion.h4 
                    className="text-xl font-semibold text-white mb-6"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                  >
                    Performance Metrics
                  </motion.h4>
                  
                  <div className="space-y-6">
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.6 }}
                    >
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-gray-400">Signal Accuracy</span>
                        <motion.span 
                          className="text-2xl font-bold text-purple-400"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ delay: 0.8, type: "spring", stiffness: 200 }}
                        >
                          {activeContent.stats.accuracy}
                        </motion.span>
                      </div>
                      <div className="w-full bg-zinc-900 rounded-full h-2 overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: activeContent.stats.accuracy }}
                          transition={{ duration: 1.5, ease: 'easeOut', delay: 0.7 }}
                          className="relative h-2 rounded-full overflow-hidden"
                        >
                          <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-purple-400" />
                          <motion.div
                            className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-50"
                            animate={{
                              x: ['-100%', '200%'],
                            }}
                            transition={{
                              duration: 2,
                              repeat: Infinity,
                              repeatDelay: 1,
                              ease: "easeInOut"
                            }}
                          />
                        </motion.div>
                      </div>
                    </motion.div>

                    <motion.div 
                      className="grid grid-cols-2 gap-4"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.9 }}
                    >
                      <motion.div 
                        className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-4 relative overflow-hidden group"
                        whileHover={{ 
                          scale: 1.05,
                        }}
                        transition={{ duration: 0.3 }}
                      >
                        <div className="absolute inset-0 bg-gradient-to-br from-purple-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                        <div className="text-sm text-gray-400 mb-1 relative z-10">Total Signals</div>
                        <div className="text-2xl font-bold text-white relative z-10">{activeContent.stats.trades}</div>
                      </motion.div>
                      <motion.div 
                        className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-4 relative overflow-hidden group"
                        whileHover={{ 
                          scale: 1.05,
                        }}
                        transition={{ duration: 0.3 }}
                      >
                        <div className="absolute inset-0 bg-gradient-to-br from-green-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                        <div className="text-sm text-gray-400 mb-1 relative z-10">Avg. Profit</div>
                        <div className="text-2xl font-bold text-green-400 relative z-10">+{activeContent.stats.profit}</div>
                      </motion.div>
                    </motion.div>

                    <motion.div 
                      className="bg-gradient-to-br from-purple-950/30 to-transparent border border-purple-500/20 rounded-lg p-4 relative overflow-hidden"
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 1 }}
                      whileHover={{ scale: 1.02 }}
                    >
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-transparent"
                        animate={{
                          x: ['-100%', '100%'],
                        }}
                        transition={{
                          duration: 3,
                          repeat: Infinity,
                          ease: "linear"
                        }}
                      />
                      <div className="flex items-center gap-2 text-sm text-purple-300 relative z-10">
                        <span>⚡️</span>
                        <span>Live since January 2026</span>
                      </div>
                    </motion.div>
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </section>
  );
}