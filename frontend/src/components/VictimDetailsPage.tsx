import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { X } from 'lucide-react';

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

export default function VictimDetailsPage() {
  const { victimId } = useParams<{ victimId: string }>();
  const [victims, setVictims] = useState<Victim[]>([]);
  const [victim, setVictim] = useState<Victim | undefined>(undefined);

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
    const foundVictim = victims.find(v => v.id === victimId);
    setVictim(foundVictim);
  }, [victims, victimId]);

  if (!victim) {
    return <div>Victim not found</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center border-b pb-4">
        <h2 className="text-xl font-bold">{victim.firstName} {victim.lastName}</h2>
        <button onClick={() => window.history.back()} className="text-gray-400 hover:text-gray-500">
          <X className="h-6 w-6" />
        </button>
      </div>
      <div className="pt-4">
        <p><strong>Birth Date:</strong> {victim.birthDate}</p>
        <p><strong>Birth Place:</strong> {victim.birthPlace}</p>
        <p><strong>Nationality:</strong> {victim.nationality}</p>
        <p><strong>Religion:</strong> {victim.religion}</p>
        {/* Add more fields as needed */}
      </div>
      <div className="pt-4">
        <h3 className="text-lg font-bold">Locations</h3>
        <div id="map" style={{ height: '400px', width: '100%' }}>
          {/* Add map implementation here */}
        </div>
      </div>
    </div>
  );
}
