import React from 'react';
import { Microscope, Sprout, Clock, Send } from 'lucide-react';

export interface FeatureHighlight {
  id: string;
  title: string;
  icon: React.ReactNode;
}

const features: FeatureHighlight[] = [
  {
    id: 'disease-guidance',
    title: 'Disease Guidance',
    icon: <Microscope className="w-6 h-6 text-[#22c55e]" />
  },
  {
    id: 'crop-care-recommendations',
    title: 'Crop Care Recommendations',
    icon: <Sprout className="w-6 h-6 text-[#22c55e]" />
  },
  {
    id: 'future-ai-support',
    title: 'Future AI Support',
    icon: <Clock className="w-6 h-6 text-[#22c55e]" />
  }
];

export interface ChatMessage {
  id: string;
  sender: 'assistant' | 'user';
  text: string;
}

const exampleConversation: ChatMessage[] = [
  {
    id: 'msg-1',
    sender: 'user',
    text: 'My tomato leaves have dark circular spots.'
  },
  {
    id: 'msg-2',
    sender: 'assistant',
    text: 'These symptoms may indicate Early Blight. Upload an image to receive AI-powered analysis.'
  },
  {
    id: 'msg-3',
    sender: 'user',
    text: 'Can I treat this disease?'
  },
  {
    id: 'msg-4',
    sender: 'assistant',
    text: 'Treatment recommendations are generated after disease detection results are available.'
  }
];

export default function AIAssistantPreviewSection() {
  return (
    <section className="relative w-full py-[80px] lg:py-[120px] px-[8%] z-10" id="assistant-preview">
      <div className="container mx-auto max-w-[1400px]">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-[40px] lg:gap-[60px] items-center">

          {/* Left Column: Content */}
          <div className="flex flex-col max-w-2xl">
            {/* Eyebrow */}
            <div className="inline-flex items-center gap-2 font-mono text-[0.7rem] tracking-[0.15em] uppercase text-[#22c55e] px-4 py-2 rounded-full border border-[#22c55e]/25 bg-[#22c55e]/[0.06] mb-6 w-fit">
              <span className="w-1.5 h-1.5 bg-[#22c55e] rounded-full animate-blink"></span>
              Coming Soon
            </div>

            {/* Header */}
            <h2 className="text-[clamp(2.2rem,8vw,4rem)] font-[800] tracking-tight text-white mb-6 font-['Syne',sans-serif] leading-[1.05]">
              Meet AgroGuard<br />
              <span className="text-transparent bg-clip-text bg-[linear-gradient(90deg,#22C55E,#86EFAC)]">AI Assistant</span>
            </h2>

            <p className="text-[1.05rem] lg:text-[1.15rem] text-[#cbd5e1] leading-[1.8] lg:leading-[1.9] mb-[32px] lg:mb-[48px]">
              Explore a preview of AgroGuard&apos;s upcoming AI assistant, designed to provide disease guidance, crop care recommendations, and conversational agricultural support through future Gemini integration.
            </p>

            {/* Features List */}
            <div className="flex flex-col gap-4">
              {features.map((feature) => (
                <div
                  key={feature.id}
                  className="flex items-center gap-4 lg:gap-5 p-[16px_20px] lg:p-[20px_24px] bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.07)] rounded-[16px] transition-transform duration-300 hover:-translate-y-1"
                >
                  <div className="w-[48px] h-[48px] rounded-full bg-[rgba(34,197,94,0.1)] border border-[rgba(34,197,94,0.2)] flex items-center justify-center shrink-0">
                    {feature.icon}
                  </div>
                  <h3 className="text-white text-[1.1rem] font-[700] font-['Syne',sans-serif]">
                    {feature.title}
                  </h3>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Chat Preview UI */}
          <div className="w-full flex flex-col items-center lg:items-end">
            <div className="w-full max-w-[440px] h-[450px] sm:h-[500px] lg:h-[540px] bg-[rgba(255,255,255,0.08)] backdrop-blur-[24px] border border-[rgba(255,255,255,0.12)] rounded-[28px] shadow-[0_10px_40px_rgba(0,0,0,0.25)] flex flex-col overflow-hidden relative">

              {/* Chat Header */}
              <div className="p-[18px_22px] bg-[linear-gradient(135deg,rgba(22,101,52,0.8),rgba(34,197,94,0.3))] border-b border-[rgba(255,255,255,0.08)] flex items-center gap-[12px] shrink-0">
                <div className="w-[36px] h-[36px] rounded-full bg-[linear-gradient(135deg,#166534,#22C55E)] flex items-center justify-center text-[1rem] border-2 border-[rgba(255,255,255,0.2)]">
                  🤖
                </div>
                <div className="flex-1">
                  <div className="font-['Syne',sans-serif] font-[700] text-[0.95rem] text-white">AgroGuard AI</div>
                  <div className="text-[0.72rem] text-white/60 flex items-center gap-[5px]">
                    <span className="w-1.5 h-1.5 bg-yellow-400 rounded-full inline-block"></span>
                    Coming Soon • Gemini Integration Planned
                  </div>
                </div>
              </div>

              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto p-[20px] flex flex-col gap-[16px] scrollbar-hide">
                {exampleConversation.map((msg) => (
                  <div
                    key={msg.id}
                    className={`max-w-[85%] p-[14px_18px] text-[0.9rem] leading-[1.6] text-white ${msg.sender === 'user'
                      ? 'bg-[linear-gradient(135deg,rgba(22,101,52,0.7),rgba(34,197,94,0.3))] border border-[rgba(34,197,94,0.2)] rounded-[18px_18px_4px_18px] self-end'
                      : 'bg-[rgba(255,255,255,0.06)] border border-[rgba(255,255,255,0.07)] rounded-[4px_18px_18px_18px] self-start'
                      }`}
                  >
                    {msg.text}
                  </div>
                ))}
              </div>

              {/* Chat Input Area (Disabled placeholder) */}
              <div className="p-[16px] border-t border-[rgba(255,255,255,0.06)] flex items-center gap-[12px] shrink-0 bg-black/20">
                <div className="flex-1 bg-[rgba(255,255,255,0.06)] border border-[rgba(255,255,255,0.08)] rounded-[14px] p-[12px_16px] text-[0.88rem] text-white/30 cursor-not-allowed select-none">
                  Ask about diseases, treatments...
                </div>
                <div className="w-[44px] h-[44px] rounded-[12px] bg-[linear-gradient(135deg,#166534,#22C55E)] flex items-center justify-center text-white opacity-80 cursor-not-allowed shrink-0">
                  <Send className="w-5 h-5 ml-0.5" />
                </div>
              </div>

            </div>

            {/* Informational Disclaimer */}
            <p className="text-xs text-white/40 text-center mt-4 max-w-sm mx-auto lg:mx-0 lg:ml-auto leading-relaxed">
              Gemini-powered AI assistance is planned for a future release and is currently under development.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}
