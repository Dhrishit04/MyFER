import React, { useState } from 'react';
import { useLocation, useNavigate, Navigate } from 'react-router-dom';
import { ArrowLeft, Download } from 'lucide-react';
import ProcessingSteps from '../components/ProcessingSteps';
import EmotionResult from '../components/EmotionResult';
import SaliencyCard from '../components/SaliencyCard';
import ConfidenceChart from '../components/ConfidenceChart';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [showResults, setShowResults] = useState(false);

  // If accessed directly without state, redirect to home
  if (!location.state || !location.state.resultData) {
    return <Navigate to="/" replace />;
  }

  const { resultData } = location.state;

  if (!showResults) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <ProcessingSteps onComplete={() => setShowResults(true)} />
      </div>
    );
  }

  // Determine Intersection Badge color
  const intScore = resultData.intersection_score;
  let scoreBadgeColor = "text-gray-400";
  let dotColor = "bg-gray-500";
  if (intScore > 0.6) {
    scoreBadgeColor = "text-green-400";
    dotColor = "bg-green-500";
  } else if (intScore >= 0.3) {
    scoreBadgeColor = "text-yellow-400";
    dotColor = "bg-yellow-500";
  } else {
    scoreBadgeColor = "text-red-400";
    dotColor = "bg-red-500";
  }

  return (
    <div className="max-w-6xl mx-auto pt-10 px-6 pb-24">
      <header className="mb-8 flex items-center justify-between">
        <button 
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Analyze Another Image</span>
        </button>
        <button className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-dark-card border border-dark-border hover:bg-dark-border/50 transition-colors text-sm text-gray-300">
          <Download className="w-4 h-4" />
          <span>Download Report</span>
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (Prediction + Chart) */}
        <div className="lg:col-span-4 space-y-6">
          <EmotionResult 
            emotion={resultData.predicted_emotion} 
            confidence={resultData.confidence} 
          />
          <div className="glass-card p-6">
            <h3 className="text-sm font-semibold text-gray-300 mb-2 uppercase tracking-wide">Class Probabilities</h3>
            <ConfidenceChart scores={resultData.all_scores} />
          </div>
        </div>

        {/* Right Column (Explainability Cards) */}
        <div className="lg:col-span-8 flex flex-col space-y-6">
          <div className="flex items-center justify-between p-4 glass-card bg-dark-bg/50 neon-glow">
            <div>
              <h2 className="text-xl font-semibold text-white tracking-wide">Neural Explanations</h2>
              <p className="text-sm text-gray-400 mt-1">Saliency maps indicating which facial features drove the prediction.</p>
            </div>
            <div className="text-right">
              <p className="text-xs text-gray-500 uppercase tracking-widest mb-1">Intersection Score</p>
              <div className="flex items-center justify-end space-x-2">
                <span className={`w-3 h-3 rounded-full ${dotColor} shadow-[0_0_10px_currentColor]`} />
                <span className={`font-mono text-xl ${scoreBadgeColor}`}>{(intScore).toFixed(3)}</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <SaliencyCard
              title="Integrated Gradients"
              base64Image={resultData.ig_image_b64}
              description="Axiomatic attribution mapping the integral of gradients from a baseline image to the input."
            />
            <SaliencyCard
              title="LRP (Approx)"
              base64Image={resultData.lrp_image_b64}
              description="Layer-wise Relevance Propagation distributing prediction score backward to input pixels."
            />
            <SaliencyCard
              title="IG-LRP Intersection"
              base64Image={resultData.intersection_image_b64}
              description="The intersection of the top 20% most salient regions from both IG and LRP maps."
            />
            <SaliencyCard
              title="Feature Bounding Boxes"
              base64Image={resultData.boxed_image_b64}
              description="Automated bounding box extraction of the most active facial regions from the intersection map."
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
