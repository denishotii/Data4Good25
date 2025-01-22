import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Victim {
  id: string;
  firstName: string;
  lastName: string;
  birthDate?: string;
  birthPlace?: string;
  nationality?: string;
  religion?: string;
  father?: string;
  mother?: string;
  spouse?: string;
  locations?: Array<{
    name: string;
    lat: number;
    lng: number;
    date?: string;
  }>;
  alternativeBirthDate?: string;
  alternativeNationality1?: string;
  alternativeNationality2?: string;
  upper?: string;
  middle?: string;
  inferredNationality?: string;
  overallConfidenceOCR?: number;
  automaticValidation?: string;
  volunteersComment?: string;
}

export default function SearchSection() {
  const [searchQuery, setSearchQuery] = useState('');
  const [victims, setVictims] = useState<Victim[]>([]);
  const [filteredVictims, setFilteredVictims] = useState<Victim[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchVictims = async () => {
      // Simulated API call
      const data: Victim[] = [
        {
          id: '1',
          firstName: 'Mieczyslawa Marianna',
          lastName: 'KIERZKOWSKA',
          father: 'Wladyslaw',
          mother: 'Pelagie Wozniak',
          birthDate: '29/7/1926',
          birthPlace: 'Wiekowo',
          nationality: 'Polish',
          religion: 'Roman Catholic',
          locations: [
            { name: 'Wiekowo', lat: 52.4256018, lng: 17.8453561, date: '1926-07-29' },
            { name: 'Weser', lat: 52.555818, lng: 8.977783, date: '1942-11' },
            { name: 'Berlin', lat: 52.520006, lng: 13.404954, date: '1944-03' },
            { name: 'Gniezno', lat: 52.534925, lng: 17.582657, date: '1944-06' }
          ],
          overallConfidenceOCR: 94,
        },
        {
          id: '631083',
          firstName: 'Rezso',
          lastName: 'BACK',
          father: '',
          mother: '',
          spouse: 'Magda geb. Klein',
          birthDate: '1905',
          birthPlace: 'Budapest',
          nationality: 'Formerly Hungarian',
          religion: 'Jewish',
          locations: [
            { name: 'Budapest', lat: 47.497912, lng: 19.040235, date: '1905' },
            { name: 'Roechnitz', lat: 47.497912, lng: 19.040235, date: '' }
          ],
          overallConfidenceOCR: 96,
          automaticValidation: 'Matched',
          volunteersComment: ''
        }
      ];
      setVictims(data);
    };

    fetchVictims();
  }, []);

  useEffect(() => {
    console.log("All victims:", victims); // Log all victims
    setFilteredVictims(victims);
  }, [victims]);

  useEffect(() => {
    if (!searchQuery.trim()) {
      setFilteredVictims(victims);
    } else {
      setFilteredVictims(
        victims.filter(victim =>
          `${victim.firstName} ${victim.lastName}`.toLowerCase().includes(searchQuery.toLowerCase())
        )
      );
    }
  }, [searchQuery, victims]);

  const handleVictimClick = (victim: Victim) => {
    console.log("🔍 Clicked victim:", victim);
    navigate(`/victim/${victim.id}`);
  };

  return (
    <div id="search" className="bg-gray-50 py-16">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-indigo-600 font-semibold uppercase">Search Records</h2>
          <p className="text-3xl font-extrabold text-gray-900">Find Information About Victims</p>
        </div>

        <div className="mt-8 max-w-3xl mx-auto">
          <div className="relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              className="focus:ring-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md h-12"
              placeholder="Search by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        <div className="mt-8 max-w-3xl mx-auto bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {filteredVictims.length > 0 ? (
              filteredVictims.map((victim) => (
                <li key={victim.id} onClick={() => handleVictimClick(victim)} className="cursor-pointer">
                  <div className="px-4 py-4 hover:bg-gray-50">
                    <p className="text-sm font-medium text-indigo-600 truncate">
                      {victim.firstName} {victim.lastName}
                    </p>
                    <p className="text-sm text-gray-500">Born: {victim.birthDate} • {victim.birthPlace}</p>
                  </div>
                </li>
              ))
            ) : (
              <li className="px-4 py-4 text-center text-gray-500">No victims found</li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}
