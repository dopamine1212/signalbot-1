import React from 'react';
import { motion } from 'motion/react';
import { Database, Brain, Bell, TrendingUp, ExternalLink } from 'lucide-react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/app/components/ui/carousel';

const BOT_LINK = 'https://t.me/futures_signalfast_bot';

const STEPS = [
  {
    icon: Database,
    title: 'Data Collection',
    desc: 'Exchanges, whale wallets, funding, volume',
  },
  {
    icon: Brain,
    title: 'AI Analysis',
    desc: 'Model scores setups and signal strength',
  },
  {
    icon: Bell,
    title: 'Signals in Bot',
    desc: 'You get Long/Short in Telegram',
  },
  {
    icon: TrendingUp,
    title: 'Trading',
    desc: 'Entry, take-profit and stop-loss at our levels',
  },
];

export function BotAnalysisSection() {
  return (
    <section className="py-16 md:py-20 bg-black relative overflow-hidden">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff02_1px,transparent_1px),linear-gradient(to_bottom,#ffffff02_1px,transparent_1px)] bg-[size:3rem_3rem]" />
      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-14"
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-3">
            Как работает бот / искусственный интеллект
          </h2>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto">
            От данных к готовым сигналам в Telegram
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
                <CarouselItem key={step.title} className="pl-4 basis-full sm:basis-1/2 lg:basis-1/4">
                  <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 h-full flex flex-col items-center text-center hover:border-purple-500/40 transition-colors">
                    <div className="w-14 h-14 rounded-xl bg-purple-600/20 flex items-center justify-center mb-4">
                      <step.icon className="w-7 h-7 text-purple-400" />
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
                      Open Bot
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
          className="mt-10 flex flex-wrap justify-center gap-4 text-sm text-gray-500"
        >
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Whale wallets</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Funding rates</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Order book</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Liquidations</span>
          <span className="px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800">Sentiment</span>
        </motion.div>
      </div>
    </section>
  );
}
