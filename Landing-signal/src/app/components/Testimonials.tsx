import { Star, Quote } from 'lucide-react';
import { motion } from 'motion/react';
import { AnimatedCounter } from '@/app/components/AnimatedCounter';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/app/components/ui/carousel';

export function Testimonials() {
  const testimonials = [
    {
      name: 'Michael Chen',
      role: 'Day Trader',
      content: 'The whale wallet tracking is incredible. I\'ve been able to anticipate major moves before they happen. Best $24 I\'ve ever spent in crypto.',
      rating: 5,
    },
    {
      name: 'Sarah Martinez',
      role: 'Crypto Investor',
      content: 'Finally, a bot that understands how the 2026 market actually works. The signals are accurate and the profit-sharing model keeps the team motivated.',
      rating: 5,
    },
    {
      name: 'David Thompson',
      role: 'Professional Trader',
      content: 'I\'ve tried dozens of trading bots. This is the only one that actually tracks institutional movements. The AI analysis is top-tier.',
      rating: 5,
    },
  ];

  return (
    <section className="py-14 md:py-16 bg-black overflow-x-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full max-w-[100vw] box-border">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-8"
        >
          <h2 className="text-3xl md:text-5xl font-bold mb-3 text-white">
            Trusted by Professionals
          </h2>
          <p className="text-base md:text-lg text-gray-500">
            Real traders, real results
          </p>
        </motion.div>

        <div className="relative px-10 md:px-12 mb-8">
          <Carousel opts={{ align: 'start', loop: true }} className="w-full">
            <CarouselContent className="-ml-4">
              {testimonials.map((testimonial, index) => (
                <CarouselItem key={index} className="pl-4 basis-full md:basis-1/2 lg:basis-1/3">
                  <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 h-full flex flex-col hover:border-purple-500/30 transition-all duration-300 min-h-[245px]">
                    <div className="flex items-center gap-1 mb-3">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="w-4 h-4 fill-purple-500 text-purple-500" />
                      ))}
                    </div>
                    <Quote className="w-6 h-6 text-purple-600/30 mb-3 shrink-0" />
                    <p className="text-gray-400 text-sm leading-relaxed flex-1 min-h-0">
                      {testimonial.content}
                    </p>
                    <div className="border-t border-zinc-800 pt-3 mt-3 shrink-0">
                      <p className="font-semibold text-white">{testimonial.name}</p>
                      <p className="text-sm text-purple-400">{testimonial.role}</p>
                    </div>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious className="left-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
            <CarouselNext className="right-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
          </Carousel>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center overflow-hidden mb-6"
        >
          <div className="inline-flex flex-col sm:flex-row items-center gap-3 sm:gap-7 px-4 sm:px-7 py-4 bg-zinc-950 border border-zinc-800 rounded-2xl w-full max-w-full sm:w-auto box-border">
            <div className="text-center min-w-0">
              <div className="text-3xl font-bold text-white mb-1">
                <AnimatedCounter end={1000} suffix="+" />
              </div>
              <div className="text-xs text-gray-500 uppercase tracking-wider whitespace-nowrap">Active Users</div>
            </div>
            <div className="w-12 h-px sm:w-px sm:h-12 bg-zinc-800 shrink-0"></div>
            <div className="text-center min-w-0">
              <div className="text-3xl font-bold text-white mb-1">
                <AnimatedCounter end={4.9} decimals={1} suffix="★" />
              </div>
              <div className="text-xs text-gray-500 uppercase tracking-wider whitespace-nowrap">Average Rating</div>
            </div>
            <div className="w-12 h-px sm:w-px sm:h-12 bg-zinc-800 shrink-0"></div>
            <div className="text-center min-w-0">
              <div className="text-3xl font-bold text-white mb-1">
                <AnimatedCounter end={98} suffix="%" />
              </div>
              <div className="text-xs text-gray-500 uppercase tracking-wider whitespace-nowrap">Satisfaction</div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="mt-10"
        >
          <h3 className="text-xl md:text-2xl font-bold text-white text-center mb-6">
            Start with us for stable results
          </h3>
          <div className="relative px-10 md:px-12">
            <Carousel opts={{ align: 'start', loop: true }} className="w-full">
              <CarouselContent className="-ml-4">
                {['/images/trade-1.png', '/images/trade-2.png', '/images/trade-3.png', '/images/trade-4.png', '/images/trade-5.png'].map((src, index) => (
                  <CarouselItem key={index} className="pl-4 basis-full sm:basis-2/3 md:basis-1/2 lg:basis-1/3">
                    <div className="rounded-xl border border-zinc-800 bg-zinc-950 overflow-hidden">
                      <img src={src} alt={`Trade result ${index + 1}`} className="w-full h-auto object-contain" />
                    </div>
                  </CarouselItem>
                ))}
              </CarouselContent>
              <CarouselPrevious className="left-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
              <CarouselNext className="right-0 border-zinc-700 bg-zinc-900 text-white hover:bg-zinc-800 hover:text-white" />
            </Carousel>
          </div>
        </motion.div>
      </div>
    </section>
  );
}