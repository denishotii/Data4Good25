import React from 'react';
import { Database } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Database className="h-8 w-8 text-indigo-600" />
            <span className="ml-2 text-xl font-semibold">Arolsen Archives Explorer</span>
          </div>
          <div className="flex items-center space-x-4">
            <a href="#about" className="text-gray-700 hover:text-indigo-600">About</a>
            <a href="#search" className="text-gray-700 hover:text-indigo-600">Search</a>
            <a href="#statistics" className="text-gray-700 hover:text-indigo-600">Statistics</a>
          </div>
        </div>
      </div>
    </nav>
  );
}