import { Gift } from 'lucide-react';
import { motion } from 'motion/react';

export function BonusFloatingButton() {
  return (
    <motion.a
      href="#bonus-section"
      className="fixed bottom-6 right-6 z-50 inline-flex items-center gap-2 rounded-full border border-purple-400/50 bg-purple-600/90 px-4 py-3 text-white shadow-xl shadow-purple-600/30 backdrop-blur-sm"
      animate={{
        y: [0, -6, 0],
        boxShadow: [
          '0 10px 25px rgba(147, 51, 234, 0.25)',
          '0 16px 32px rgba(147, 51, 234, 0.45)',
          '0 10px 25px rgba(147, 51, 234, 0.25)',
        ],
      }}
      transition={{
        duration: 2.2,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
      aria-label="Go to bonus section"
    >
      <Gift className="h-4 w-4" />
      <span className="text-sm font-semibold">Bonus</span>
    </motion.a>
  );
}
