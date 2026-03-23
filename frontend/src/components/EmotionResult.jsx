import React from 'react';

const emotionColors = {
  Happy: 'bg-green-500/20 text-green-400 border-green-500/30',
  Sad: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  Angry: 'bg-red-500/20 text-red-400 border-red-500/30',
  Fear: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  Disgust: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  Surprise: 'bg-pink-500/20 text-pink-400 border-pink-500/30',
  Neutral: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
};

const EmotionResult = ({ emotion, confidence }) => {
  const colorClass = emotionColors[emotion] || emotionColors.Neutral;
  
  return (
    <div className="w-full flex flex-col items-center justify-center p-8 glass-card relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-dark-accent/10 rounded-full blur-3xl -mr-10 -mt-10" />
      <div className="absolute bottom-0 left-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -ml-10 -mb-10" />
      
      <p className="text-gray-400 uppercase tracking-widest text-xs mb-3 font-medium">Predominant Emotion</p>
      <div className={`px-6 py-2 rounded-full border ${colorClass} font-bold tracking-widest uppercase mb-4 text-3xl shadow-lg`}>
        {emotion}
      </div>
      <div className="flex items-end space-x-1">
        <span className="text-5xl font-light text-white">{(confidence * 100).toFixed(1)}</span>
        <span className="text-xl text-gray-400 mb-1">%</span>
      </div>
      <p className="text-gray-500 mt-2 text-sm">Confidence Score</p>
    </div>
  );
};

export default EmotionResult;
