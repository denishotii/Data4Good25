import React from 'react';
import Modal from 'react-modal';
import { X } from 'lucide-react';

interface VictimDetailsProps {
  isOpen: boolean;
  onClose: () => void;
  victim: any;
}

Modal.setAppElement('#root'); // Make sure to set the app element for accessibility

export default function VictimDetails({ isOpen, onClose, victim }: VictimDetailsProps) {
  console.log("🔍 Rendering VictimDetails:", { isOpen, victim }); // Debugging log

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      contentLabel="Victim Details"
      className="bg-white rounded-lg shadow-xl w-full max-w-3xl p-4"
      overlayClassName="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4"
    >
      <div className="flex justify-between items-center border-b pb-4">
        <h2 className="text-xl font-bold">{victim.firstName} {victim.lastName}</h2>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-500">
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
    </Modal>
  );
}
