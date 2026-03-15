'use client';

export default function Process() {
  const steps = [
    { title: 'Discover', desc: 'Understanding your goals and setting the strategic foundation.' },
    { title: 'Design', desc: 'Crafting premium visuals and intuitive user experiences.' },
    { title: 'Develop', desc: 'Writing clean, scalable, and high-performance code.' },
    { title: 'Launch', desc: 'Rigorous testing and deploying to production.' }
  ];

  return (
    <section id="process" className="py-32 px-6 max-w-4xl mx-auto">
      <h2 className="font-syne text-4xl font-bold text-center mb-24">How We Work</h2>
      <div className="relative border-l border-white/10 pl-10 md:pl-20 ml-4 md:ml-10 space-y-20">
        {steps.map((step, i) => (
          <div key={i} className="relative">
            <div className="absolute -left-[45px] md:-left-[85px] top-1 w-4 h-4 rounded-full bg-accent" />
            <h3 className="font-syne text-2xl font-bold text-white mb-3">0{i+1}. {step.title}</h3>
            <p className="text-secondary leading-relaxed bg-white/5 p-6 rounded-2xl">{step.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
