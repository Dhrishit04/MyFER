import React, { useEffect, useState } from 'react';
import { CheckCircle2, Circle } from 'lucide-react';

const STEPS = [
  "Image received",
  "Running model inference...",
  "Computing Integrated Gradients...",
  "Computing LRP...",
  "Computing Saliency Intersection...",
  "Generating visualizations..."
];

const ProcessingSteps = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (currentStep < STEPS.length) {
      const timer = setTimeout(() => {
        setCurrentStep(s => s + 1);
      }, 400); // 400ms per step
      return () => clearTimeout(timer);
    } else {
      const timer = setTimeout(() => {
        onComplete();
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [currentStep, onComplete]);

  return (
    <div className="max-w-md mx-auto mt-20 p-8 glass-card">
      <h2 className="text-xl font-semibold mb-6 flex items-center">
        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-dark-accent" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Analyzing Image...
      </h2>
      <div className="space-y-4">
        {STEPS.map((step, index) => {
          const isCompleted = index < currentStep;
          const isActive = index === currentStep;
          const isPending = index > currentStep;
          
          return (
            <div 
              key={index} 
              className={`flex items-center space-x-3 transition-opacity duration-300 ${
                isPending ? 'opacity-30' : 'opacity-100'
              }`}
            >
              {isCompleted ? (
                <CheckCircle2 className="w-5 h-5 text-green-400" />
              ) : isActive ? (
                <Circle className="w-5 h-5 text-dark-accent animate-pulse" />
              ) : (
                <Circle className="w-5 h-5 text-gray-600" />
              )}
              <span className={`text-sm ${isActive ? 'text-gray-100 font-medium' : 'text-gray-400'}`}>
                {step}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProcessingSteps;
