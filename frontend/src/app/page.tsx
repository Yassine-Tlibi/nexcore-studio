'use client';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import Marquee from '../components/Marquee';
import Services from '../components/Services';
import Stats from '../components/Stats';
import Showcase from '../components/Showcase';
import Methodology from '../components/Methodology';
import Contact from '../components/Contact';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <Hero />
      <Marquee />
      <Services />
      <Stats />
      <Showcase />
      <Methodology />
      <Contact />
      <Footer />
    </main>
  );
}
