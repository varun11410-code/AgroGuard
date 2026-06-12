import React from 'react';

export interface Crop {
  id: string;
  name: string;
  icon: string;
  diseases: string[];
}

const supportedCrops: Crop[] = [
  {
    id: 'tomato',
    name: 'Tomato',
    icon: '🍅',
    diseases: ['Healthy', 'Early Blight', 'Late Blight'],
  },
  {
    id: 'potato',
    name: 'Potato',
    icon: '🥔',
    diseases: ['Healthy'],
  }
];

export default function SupportedCropsSection() {
  return (
    <section className="relative w-full py-[80px] lg:py-[120px] px-[8%] z-10" id="crops">
      <div className="container mx-auto max-w-[1400px]">

        {/* Section Header */}
        <div className="text-center mb-[48px] max-w-3xl mx-auto flex flex-col items-center">
          <div className="inline-flex items-center gap-2 font-mono text-[0.7rem] tracking-[0.15em] uppercase text-[#22c55e] px-4 py-2 rounded-full border border-[#22c55e]/25 bg-[#22c55e]/[0.06] mb-6">
            <span className="w-1.5 h-1.5 bg-[#22c55e] rounded-full animate-blink"></span>
            Current Detection Capabilities
          </div>
          <h2 className="text-[clamp(2.5rem,8vw,3.5rem)] font-[800] tracking-tight text-white mb-4 font-['Syne',sans-serif] leading-[1.1]">
            Built for Real<br />Field Conditions
          </h2>
          <p className="text-[1.05rem] text-white/50 leading-[1.8] max-w-[520px]">
            Version 1 currently supports disease detection for tomato and potato crops using a custom deep learning model.
          </p>
        </div>

        {/* Crops Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-[25px] max-w-[800px] mx-auto">
          {supportedCrops.map((crop) => (
            <div
              key={crop.id}
              className="relative bg-[rgba(255,255,255,0.08)] backdrop-blur-[24px] border border-[rgba(255,255,255,0.12)] rounded-[28px] p-8 lg:p-[50px_40px] text-center shadow-[0_10px_40px_rgba(0,0,0,0.25)] transition-transform duration-300 hover:-translate-y-[8px] group overflow-hidden cursor-pointer"
            >
              {/* Subtle hover glow effect matching template */}
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(34,197,94,0.1),transparent_65%)] opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>

              {/* Crop Icon */}
              <span className="text-[64px] lg:text-[80px] block mb-[20px] drop-shadow-[0_10px_20px_rgba(0,0,0,0.4)] transition-transform duration-300 group-hover:scale-110 group-hover:-translate-y-[6px] leading-none">
                {crop.icon}
              </span>

              {/* Crop Name */}
              <h3 className="text-white text-[1.4rem] font-[700] mb-[10px] font-['Syne',sans-serif]">
                {crop.name}
              </h3>

              {/* Diseases */}
              <p className="text-white/45 text-[0.9rem] leading-[1.6]">
                {crop.diseases.join(' · ')}
              </p>

              {/* Status Badge */}
              <div className="inline-flex items-center gap-[6px] mt-[16px] px-[14px] py-[6px] rounded-full text-[0.75rem] font-['Space_Mono',monospace] bg-[rgba(34,197,94,0.1)] border border-[rgba(34,197,94,0.2)] text-[#22c55e]">
                <span className="text-[10px]">●</span> Currently Supported
              </div>
            </div>
          ))}
        </div>

        {/* Informational Note */}
        <div className="text-center mt-[28px]">
          <div className="block lg:inline-block px-[20px] lg:px-[24px] py-[14px] rounded-[16px] lg:rounded-full bg-[rgba(245,158,11,0.08)] border border-[rgba(245,158,11,0.2)] text-[#f59e0b]/80 text-[0.82rem] font-['Space_Mono',monospace] tracking-[0.05em] leading-[1.6]">
            ⚠ AgroGuard currently focuses on Tomato and Potato disease detection as part of its initial release. Support for additional crops will expand in future versions.
          </div>
        </div>

      </div>
    </section>
  );
}
