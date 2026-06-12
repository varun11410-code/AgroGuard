import React from 'react';
import { UploadCloud, Activity, FileText } from 'lucide-react';

export interface Step {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
}

const steps: Step[] = [
  {
    id: 'step-1',
    title: 'Upload Crop Image',
    description: 'Take a photo or upload an image of a tomato or potato plant showing signs of disease or stress.',
    icon: <UploadCloud className="w-8 h-8 text-white" />
  },
  {
    id: 'step-2',
    title: 'AI Disease Detection',
    description: 'Our advanced machine learning model analyzes the visual symptoms and identifies the potential disease with high accuracy.',
    icon: <Activity className="w-8 h-8 text-white" />
  },
  {
    id: 'step-3',
    title: 'Receive Recommendations',
    description: 'Get immediate, actionable treatment recommendations and insights to restore your crop\'s health.',
    icon: <FileText className="w-8 h-8 text-white" />
  }
];

export default function HowItWorksSection() {
  return (
    <section className="relative w-full py-[120px] px-[8%] z-10">
      <div className="container mx-auto max-w-[1400px]">
        {/* Section Header */}
        <div className="text-center mb-[70px] max-w-3xl mx-auto flex flex-col items-center">
          <h2 className="text-[3rem] font-[800] tracking-tight text-white mb-4 font-['Syne',sans-serif]">
            How It Works
          </h2>
          <p className="text-[1.15rem] text-[#cbd5e1] leading-[1.9]">
            Protect your crops in three simple steps. Our AI-driven platform makes disease detection fast, accurate, and accessible.
          </p>
        </div>

        {/* Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-[25px]">
          {steps.map((step, index) => (
            <div
              key={step.id}
              className="relative bg-[rgba(255,255,255,0.08)] backdrop-blur-[24px] border border-[rgba(255,255,255,0.12)] rounded-[28px] p-[30px] shadow-[0_10px_40px_rgba(0,0,0,0.25)] transition-transform duration-300 hover:-translate-y-[10px] group flex flex-col"
            >
              {/* Step Number Badge */}
              <div className="absolute top-6 right-6 text-5xl font-[800] text-white/5 pointer-events-none select-none font-['Syne',sans-serif]">
                0{index + 1}
              </div>

              {/* Gradient Icon Container */}
              <div className="w-[60px] h-[60px] rounded-full bg-[linear-gradient(135deg,#166534,#22C55E)] flex items-center justify-center mb-6 shadow-lg shadow-[#22C55E]/20">
                {step.icon}
              </div>

              {/* Step Content */}
              <h3 className="text-white text-xl font-[700] mb-3">
                {step.title}
              </h3>
              <p className="text-[#cbd5e1] text-[1.1rem] leading-[1.8] flex-1">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
