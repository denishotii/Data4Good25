import React, { useState } from 'react';
import { Search, Info, Map, Database, Heart } from 'lucide-react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import SearchSection from './components/SearchSection';
import Statistics from './components/Statistics';
import Footer from './components/Footer';

function App() {
  const [searchOpen, setSearchOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <Hero />
      <About />
      <Statistics />
      <SearchSection isOpen={searchOpen} setIsOpen={setSearchOpen} />
      <Footer />
    </div>
  );
}

export default App;