import HeroSection from "@/components/landing/HeroSection";
import HowItWorksSection from "@/components/landing/HowItWorksSection";
import SupportedCropsSection from "@/components/landing/SupportedCropsSection";
import AIAssistantPreviewSection from "@/components/landing/AIAssistantPreviewSection";

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <HowItWorksSection />
      <SupportedCropsSection />
      <AIAssistantPreviewSection />
    </>
  );
}