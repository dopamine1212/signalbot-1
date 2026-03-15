import { motion } from 'motion/react';
import { ExternalLink, Send } from 'lucide-react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/app/components/ui/carousel';

import { BOT_LINKS } from '@/app/constants';
const FUTURES_BOT_LINK = BOT_LINKS.HUB;
const CHANNEL_LINK = 'https://t.me/SaawyerCrypto';
const PROOF_LINK = 'https://t.me/futuresreviewsTom';
const BONUS_BOT_LINK = BOT_LINKS.SCANNER;

const ECOSYSTEM_ITEMS = [
  {
    title: '1️⃣ AI Futures bot',
    link: FUTURES_BOT_LINK,
    desc: 'Automated futures signals',
    points: [
      'Whale and institutional activity analysis',
      'Optimal entry and exit levels',
    ],
  },
  {
    title: '2️⃣ Trading channel',
    link: CHANNEL_LINK,
    desc: 'Live trading and market analysis',
    points: [
      'Instant signal notifications',
      'Exclusive updates from the team',
    ],
  },
  {
    title: '3️⃣ Proof system',
    link: PROOF_LINK,
    desc: 'Verified signals and trade confirmations',
    points: [
      'Transparent performance statistics',
      'Proof-based visibility for every user',
    ],
  },
];

export function BotScreenshotsSection() {
  return (
    <section className="py-16 md:py-20 bg-black relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-32 bg-gradient-to-b from-[#2aabee]/10 to-transparent" />
      <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-10"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#2aabee]/10 border border-[#2aabee]/30 mb-4">
            <Send className="w-4 h-4 text-[#2aabee]" />
            <span className="text-sm text-[#2aabee]">Core ecosystem elements</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-3">
            Full TomSawyer ecosystem: your tools for profitable trading
          </h2>
          <p className="text-gray-400 text-base sm:text-lg max-w-4xl mx-auto">
            TomSawyer is not just a bot. It is a complete system that helps traders make decisions, track the market,
            and receive real-time signals.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="relative px-10 md:px-12 mb-10"
        >
          <Carousel opts={{ align: 'start', loop: true }} className="w-full">
            <CarouselContent className="-ml-4">
              {ECOSYSTEM_ITEMS.map((item) => (
                <CarouselItem key={item.title} className="pl-4 basis-full md:basis-1/2 lg:basis-1/3">
                  <a
                    href={item.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block rounded-xl border border-zinc-800 bg-zinc-950 p-6 h-full hover:border-purple-500/50 transition-all"
                  >
                    <h3 className="text-xl font-semibold text-white mb-2">{item.title}</h3>
                    <p className="text-gray-300 mb-3">{item.desc}</p>
                    <ul className="space-y-2 text-sm text-gray-500 mb-4">
                      {item.points.map((p) => (
                        <li key={p}>• {p}</li>
                      ))}
                    </ul>
                    <span className="inline-flex items-center gap-2 text-purple-400 font-medium">
                      <ExternalLink className="w-4 h-4" />
                      Open
                    </span>
                  </a>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious className="left-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
            <CarouselNext className="right-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
          </Carousel>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl border border-zinc-800 overflow-hidden bg-[#161622] shadow-2xl"
        >
          <div className="px-5 py-4 border-b border-zinc-800 bg-zinc-900/70">
            <h3 className="text-xl font-semibold text-white mb-1">4️⃣ Bonus tools & AI scanner</h3>
            <p className="text-gray-400 text-sm">Extra analysis tools and AI scanner to validate your own strategies</p>
          </div>

          <div className="grid lg:grid-cols-2 gap-0">
            <div className="p-5 border-b lg:border-b-0 lg:border-r border-zinc-800 flex items-center justify-center">
              <img src="/images/chart-analysis-screenshot.png" alt="Chart Analysis" className="rounded-xl border border-zinc-700 w-full max-w-sm h-auto object-contain shadow-lg" />
            </div>
            <div className="p-5 flex flex-col justify-center bg-[radial-gradient(circle_at_top,_rgba(124,58,237,0.25),transparent_60%)] relative">
              <img src="/images/raccoon.png" alt="" className="absolute top-4 right-4 w-16 h-16 object-contain opacity-90" />
              <p className="text-gray-300 mb-2 text-sm">✅ Makes market structure easier to understand</p>
              <p className="text-gray-400 mb-4 text-sm">✅ Helps you validate ideas faster and confirm setups directly from charts</p>
              <a
                href={BONUS_BOT_LINK}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex w-fit items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-purple-500 text-white font-semibold hover:from-purple-500 hover:to-purple-400 transition-all"
              >
                🚀 Start using TomSawyer AI Bot
              </a>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
