import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useParams } from 'react-router-dom';
import Navbar from './Navbar';
import Hero from './Hero';
import About from './About';
import Statistics from './Statistics';
import Footer from './Footer';
import SearchSection from './SearchSection';
import VictimDetailsPage from './VictimDetailsPage';

function VictimDetailsPage() {
  const { victimId } = useParams();
  const [victimDetails, setVictimDetails] = useState(null);

  useEffect(() => {
    // Fetch victim details from an API or data source
    fetch(`/api/victims/${victimId}`)
      .then(response => response.json())
      .then(data => setVictimDetails(data))
      .catch(error => console.error('Error fetching victim details:', error));
  }, [victimId]);

  if (!victimDetails) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{victimDetails.name}</h1>
      <p>{victimDetails.description}</p>
      {/* Render other victim details as needed */}
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" element={
            <>
              <Hero />
              <About />
              <SearchSection />
              <Statistics />
            </>
          } />
          <Route path="/victim/:victimId" element={<VictimDetailsPage />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}
