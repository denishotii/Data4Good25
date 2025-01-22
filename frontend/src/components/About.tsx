import React from 'react';
import { Info, Database, Heart } from 'lucide-react';

export default function About() {
  return (
    <div id="about" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <h2 className="text-base text-indigo-600 font-semibold tracking-wide uppercase">About</h2>
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            The Arolsen Archives
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            The world's most comprehensive archive on victims and survivors of Nazi persecution.
          </p>
        </div>

        <div className="mt-10">
          <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
            <div className="relative">
              <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                <Database className="h-6 w-6" />
              </div>
              <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Comprehensive Records</p>
              <p className="mt-2 ml-16 text-base text-gray-500">
                Over 30 million documents from concentration camps, forced labour records, and files on displaced persons.
              </p>
            </div>

            <div className="relative">
              <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                <Info className="h-6 w-6" />
              </div>
              <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Digital Initiative</p>
              <p className="mt-2 ml-16 text-base text-gray-500">
                #EveryNameCounts project works to preserve and expand access to these vital historical records.
              </p>
            </div>

            <div className="relative">
              <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                <Heart className="h-6 w-6" />
              </div>
              <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Memorial</p>
              <p className="mt-2 ml-16 text-base text-gray-500">
                Honoring the memory of victims while contributing to education and historical justice.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}