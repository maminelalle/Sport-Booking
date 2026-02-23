import React from 'react';
import { Link } from 'react-router-dom';

const CourtCard = ({ court }) => {
  const imageUrl = court.main_image?.image || '/placeholder.jpg';

  return (
    <div className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow overflow-hidden">
      {/* Image */}
      <div className="relative h-48 bg-gray-200 overflow-hidden">
        <img src={imageUrl} alt={court.name} className="w-full h-full object-cover" />
      </div>

      {/* Contenu */}
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2 line-clamp-2">{court.name}</h3>

        {/* Lieu */}
        <p className="text-sm text-gray-600 mb-2">{court.site_name}</p>

        {/* Sport */}
        <div className="flex items-center justify-between mb-4">
          <span className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">
            {court.sport_type_name}
          </span>
          <span className="text-sm text-gray-500">{court.capacity} personnes</span>
        </div>

        {/* Prix */}
        <div className="flex justify-between items-center mb-4">
          <span className="text-2xl font-bold text-blue-600">{court.price_per_hour}€</span>
          <span className="text-sm text-gray-500">/heure</span>
        </div>

        {/* Bouton */}
        <Link
          to={`/courts/${court.id}`}
          className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md text-center transition-colors"
        >
          Voir les détails
        </Link>
      </div>
    </div>
  );
};

export default CourtCard;
