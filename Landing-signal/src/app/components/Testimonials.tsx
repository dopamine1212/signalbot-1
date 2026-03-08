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
    <section className="py-24 bg-black overflow-x-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full max-w-[100vw] box-border">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-6xl font-bold mb-4 text-white">
            Trusted by Professionals
          </h2>
          <p className="text-xl text-gray-500">
            Real traders, real results
          </p>
        </motion.div>

        <div className="relative px-10 md:px-12 mb-16">
          <Carousel opts={{ align: 'start', loop: true }} className="w-full">
            <CarouselContent className="-ml-4">
              {testimonials.map((testimonial, index) => (
                <CarouselItem key={index} className="pl-4 basis-full md:basis-1/2 lg:basis-1/3">
                  <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-8 h-full flex flex-col hover:border-purple-500/30 transition-all duration-300 min-h-[280px]">
                    <div className="flex items-center gap-1 mb-4">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="w-5 h-5 fill-purple-500 text-purple-500" />
                      ))}
                    </div>
                    <Quote className="w-8 h-8 text-purple-600/30 mb-4 shrink-0" />
                    <p className="text-gray-400 leading-relaxed flex-1 min-h-0">
                      {testimonial.content}
                    </p>
                    <div className="border-t border-zinc-800 pt-4 mt-4 shrink-0">
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
          className="text-center overflow-hidden"
        >
          <div className="inline-flex flex-col sm:flex-row items-center gap-4 sm:gap-8 px-4 sm:px-8 py-6 bg-zinc-950 border border-zinc-800 rounded-2xl w-full max-w-full sm:w-auto box-border">
            <div className="text-center min-w-0">
              <div className="text-4xl font-bold text-white mb-1">
                <AnimatedCounter end={1000} suffix="+" />
              </div>
              <div className="text-sm text-gray-500 uppercase tracking-wider whitespace-nowrap">Active Users</div>
            </div>
            <div className="w-12 h-px sm:w-px sm:h-12 bg-zinc-800 shrink-0"></div>
            <div className="text-center min-w-0">
              <div className="text-4xl font-bold text-white mb-1">
                <AnimatedCounter end={4.9} decimals={1} suffix="★" />
              </div>
              <div className="text-sm text-gray-500 uppercase tracking-wider whitespace-nowrap">Average Rating</div>
            </div>
            <div className="w-12 h-px sm:w-px sm:h-12 bg-zinc-800 shrink-0"></div>
            <div className="text-center min-w-0">
              <div className="text-4xl font-bold text-white mb-1">
                <AnimatedCounter end={98} suffix="%" />
              </div>
              <div className="text-sm text-gray-500 uppercase tracking-wider whitespace-nowrap">Satisfaction</div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}