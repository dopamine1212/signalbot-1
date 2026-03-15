import React from 'react';
import { motion } from 'motion/react';
import { ExternalLink } from 'lucide-react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/app/components/ui/carousel';

import { BOT_LINKS } from '@/app/constants';
const BOT_LINK = BOT_LINKS.HUB;

const STEPS = [
  {
    emoji: '1️⃣',
    title: 'Connect to bot',
    desc: 'Sign up in Telegram and link your account',
  },
  {
    emoji: '2️⃣',
    title: 'AI tracks big players',
    desc: 'TomSawyer scans whales and institutional activity in real time',
  },
  {
    emoji: '3️⃣',
    title: 'Instant futures signals',
    desc: 'Receive actionable crypto futures signals directly in Telegram',
  },
  {
    emoji: '4️⃣',
    title: 'Smart risk management',
    desc: 'AI calculates optimal entry and exit levels to maximize potential profit',
  },
  {
    emoji: '5️⃣',
    title: 'Monitor & optimize',
    desc: 'Track signals, history, and success rates in the ecosystem dashboard',
  },
];

const ADVANTAGES = [
  '⚡️ Fast AI analysis — signals in seconds',
  '🧠 Follow whales & big players — see where the money moves',
  '🤖 Automated futures bot — everything inside Telegram',
  '📈 High-conviction signals — validated by professional traders',
  '🌐 Part of full ecosystem — channel, bot, proof system',
  '📊 Full control — track history, evaluate results, improve your strategy',
];

export function BotAnalysisSection() {
  return (
    <section className="py-12 md:py-16 bg-black relative overflow-hidden">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff02_1px,transparent_1px),linear-gradient(to_bottom,#ffffff02_1px,transparent_1px)] bg-[size:3rem_3rem]" />
      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-10"
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-3">
            How the best AI futures bot TomSawyer works
          </h2>
          <p className="text-gray-400 text-base sm:text-lg max-w-3xl mx-auto">
            Your personal AI assistant that tracks the market, follows whales, and delivers actionable crypto futures
            signals instantly
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="relative px-10 md:px-12"
        >
          <Carousel opts={{ align: 'start', loop: true }} className="w-full">
            <CarouselContent className="-ml-4">
              {STEPS.map((step, i) => (
                <CarouselItem key={step.title} className="pl-4 basis-full sm:basis-1/2 lg:basis-1/3 xl:basis-1/4">
                  <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 h-full flex flex-col items-center text-center hover:border-purple-500/40 transition-colors">
                    <div className="w-14 h-14 rounded-xl bg-purple-600/20 flex items-center justify-center mb-4">
                      <span className="text-2xl">{step.emoji}</span>
                    </div>
                    <h3 className="text-lg font-semibold text-white mb-2">{step.title}</h3>
                    <p className="text-gray-500 text-sm mb-4">{step.desc}</p>
                    <a
                      href={BOT_LINK}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-purple-400 hover:text-purple-300 font-medium text-base mt-auto"
                    >
                      <ExternalLink className="w-4 h-4 shrink-0" />
                      🚀 Start using TomSawyer AI Bot
                    </a>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious className="left-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
            <CarouselNext className="right-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
          </Carousel>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-8 -mx-4 sm:mx-0"
        >
          <div className="flex gap-3 px-4 sm:px-0 overflow-x-auto pb-2 scrollbar-none">
            {ADVANTAGES.map((item) => (
              <span
                key={item}
                className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-xs sm:text-sm text-gray-300 whitespace-nowrap"
              >
                {item}
              </span>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
