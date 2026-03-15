import { ReactNode, useRef, useState } from 'react';
import { motion } from 'motion/react';

import { BOT_LINKS } from '@/app/constants';
/** Главная CTA (Start trading) — основной бот @TomSawyerHub_bot */
const BOT_LINK = BOT_LINKS.HUB;

interface MagneticButtonProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  /** "bot" opens Telegram, "bonus" scrolls to bonus section */
  href?: string;
}

export function MagneticButton({ children, className = '', onClick, href }: MagneticButtonProps) {
  const ref = useRef<HTMLButtonElement | HTMLAnchorElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement & HTMLAnchorElement>) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    setPosition({ x: x * 0.3, y: y * 0.3 });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  const motionProps = {
    ref,
    className,
    onMouseMove: handleMouseMove,
    onMouseLeave: handleMouseLeave,
    animate: { x: position.x, y: position.y },
    transition: { type: 'spring' as const, stiffness: 150, damping: 15, mass: 0.1 },
  };

  if (href === 'bot' || href === BOT_LINK || href === BOT_LINKS.HUB) {
    return (
      <motion.a
        {...motionProps}
        href={BOT_LINK}
        target="_blank"
        rel="noopener noreferrer"
      >
        {children}
      </motion.a>
    );
  }

  if (href === 'bonus' || href === '#bonus-section') {
    return (
      <motion.a
        {...motionProps}
        href="#bonus-section"
      >
        {children}
      </motion.a>
    );
  }

  if (href === 'products' || href === '#products-section') {
    return (
      <motion.a
        {...motionProps}
        href="#products-section"
      >
        {children}
      </motion.a>
    );
  }

  if (href && href.startsWith('http')) {
    return (
      <motion.a
        {...motionProps}
        href={href}
        target="_blank"
        rel="noopener noreferrer"
      >
        {children}
      </motion.a>
    );
  }

  return (
    <motion.button
      {...motionProps}
      onClick={onClick}
    >
      {children}
    </motion.button>
  );
}
