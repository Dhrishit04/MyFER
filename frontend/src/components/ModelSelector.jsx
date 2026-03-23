import React from 'react';
import { Cpu } from 'lucide-react';

const ModelSelector = ({ models, selectedModelId, onModelSelect, loading }) => {
  if (loading) {
    return (
      <div className="w-full grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {[1, 2].map(i => (
          <div key={i} className="animate-pulse glass-card h-24 rounded-xl"></div>
        ))}
      </div>
    );
  }

  if (!models || models.length === 0) {
    return (
      <div className="p-6 text-center text-gray-400 glass-card">
        No models currently available from the backend.
      </div>
    );
  }

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
      {models.map((model) => {
        const isSelected = selectedModelId === model.id;
        
        return (
          <div
            key={model.id}
            onClick={() => onModelSelect(model.id)}
            className={`cursor-pointer transition-all duration-200 rounded-xl p-5 border text-left flex flex-col items-start
              ${isSelected 
                ? 'bg-dark-accent/10 border-dark-accent shadow-[0_0_15px_rgba(0,209,255,0.15)] scale-[1.02]' 
                : 'bg-dark-card border-dark-border hover:bg-dark-border/40 hover:border-gray-500'}`}
          >
            <div className="flex items-center space-x-3 mb-2">
              <div className={`p-2 rounded-lg ${isSelected ? 'bg-dark-accent/20 text-dark-accent' : 'bg-gray-800 text-gray-400'}`}>
                <Cpu className="w-5 h-5" />
              </div>
              <h3 className={`font-medium ${isSelected ? 'text-dark-accent text-shadow-glow' : 'text-gray-200'}`}>
                {model.name}
              </h3>
            </div>
            <p className="text-sm text-gray-400 mt-1 line-clamp-2">{model.description}</p>
          </div>
        );
      })}
    </div>
  );
};

export default ModelSelector;
