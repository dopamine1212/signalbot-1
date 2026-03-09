import { Hero } from '@/app/components/Hero';
import { BotAnalysisSection } from '@/app/components/BotAnalysisSection';
import { MarketEvolutionSection } from '@/app/components/MarketEvolutionSection';
import { TradingTabs } from '@/app/components/TradingTabs';
import { BotScreenshotsSection } from '@/app/components/BotScreenshotsSection';
import { Testimonials } from '@/app/components/Testimonials';
import { Pricing } from '@/app/components/Pricing';
import { Footer } from '@/app/components/Footer';
import { FloatingTicker } from '@/app/components/FloatingTicker';
import { BonusFloatingButton } from '@/app/components/BonusFloatingButton';

export default function App() {
  return (
    <div className="min-h-screen bg-black text-white antialiased overflow-x-hidden max-w-[100vw]">
      <FloatingTicker />
      <BonusFloatingButton />
      <div className="pt-12">
        <Hero />
        <BotAnalysisSection />
        <TradingTabs />
        <MarketEvolutionSection />
        <BotScreenshotsSection />
        <Testimonials />
        <Pricing />
        <Footer />
      </div>
    </div>
  );
}
