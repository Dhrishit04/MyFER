import React from 'react';

const SaliencyCard = ({ title, base64Image, description, badge }) => {
  return (
    <div className="glass-card flex flex-col overflow-hidden group">
      <div className="p-4 border-b border-dark-border flex items-center justify-between">
        <h3 className="font-semibold text-gray-200">{title}</h3>
        {badge && (
          <span className="text-xs px-2 py-1 bg-dark-bg border border-dark-border rounded text-gray-300">
            {badge}
          </span>
        )}
      </div>
      
      <div className="relative w-full aspect-square bg-black overflow-hidden flex items-center justify-center">
        <img 
          src={`data:image/png;base64,${base64Image}`} 
          alt={title}
          className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-500"
        />
      </div>
      
      <div className="p-4 flex-grow bg-dark-bg/50">
        <p className="text-sm text-gray-400">{description}</p>
      </div>
    </div>
  );
};

export default SaliencyCard;
