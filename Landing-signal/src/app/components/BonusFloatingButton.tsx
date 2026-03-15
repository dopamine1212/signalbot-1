import { Gift } from 'lucide-react';
import { BOT_LINKS } from '@/app/constants';
import { motion } from 'motion/react';

export function BonusFloatingButton() {
  return (
    <motion.a
      href={BOT_LINKS.SCANNER}
      target="_blank"
      rel="noopener noreferrer"
      className="fixed bottom-6 right-6 z-50 inline-flex items-center gap-2 rounded-full border border-sky-400/60 bg-sky-600/90 px-4 py-3 text-white shadow-xl shadow-sky-500/40 backdrop-blur-sm"
      animate={{
        y: [0, -6, 0],
        boxShadow: [
          '0 10px 25px rgba(34, 158, 217, 0.25)',
          '0 16px 32px rgba(34, 158, 217, 0.45)',
          '0 10px 25px rgba(34, 158, 217, 0.25)',
        ],
      }}
      transition={{
        duration: 2.2,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
      aria-label="Open bonus scanner bot"
    >
      <Gift className="h-4 w-4" />
      <span className="text-sm font-semibold">Bonus</span>
    </motion.a>
  );
}
