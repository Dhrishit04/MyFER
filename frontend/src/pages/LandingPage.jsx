import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity } from 'lucide-react';
import { getModels, predictEmotion } from '../api/ferApi';
import ImageUploader from '../components/ImageUploader';
import ModelSelector from '../components/ModelSelector';

const LandingPage = () => {
  const navigate = useNavigate();
  const [models, setModels] = useState([]);
  const [loadingModels, setLoadingModels] = useState(true);
  
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedModelId, setSelectedModelId] = useState(null);
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await getModels();
        setModels(data);
        if (data && data.length > 0) {
          setSelectedModelId(data[0].id); // Auto-select first
        }
      } catch (err) {
        console.error("Failed to load models:", err);
      } finally {
        setLoadingModels(false);
      }
    };
    fetchModels();
  }, []);

  const handleAnalyze = async () => {
    if (!selectedImage || !selectedModelId) return;
    
    setIsAnalyzing(true);
    setError(null);
    try {
      const result = await predictEmotion(selectedImage, selectedModelId);
      // Navigate to ResultPage with data in state
      navigate('/result', { state: { resultData: result } });
    } catch (err) {
      console.error(err);
      setError("Analysis failed. Please check backend connection and try again.");
      setIsAnalyzing(false);
    }
  };

  const isReady = selectedImage !== null && selectedModelId !== null;

  return (
    <div className="max-w-4xl mx-auto pt-16 px-6 pb-24">
      <header className="mb-12 flex items-center space-x-3">
        <Activity className="w-8 h-8 text-dark-accent" />
        <h1 className="text-2xl font-semibold tracking-wide text-white">FER<span className="text-gray-500 font-light">Studio</span></h1>
      </header>

      <main className="space-y-12">
        <section>
          <h2 className="text-lg font-medium text-gray-300 mb-4 tracking-wide uppercase text-sm">1. Select Input</h2>
          <ImageUploader onImageSelect={setSelectedImage} selectedImage={selectedImage} />
        </section>

        <section>
          <h2 className="text-lg font-medium text-gray-300 mb-4 tracking-wide uppercase text-sm">2. Select Model</h2>
          <ModelSelector 
            models={models} 
            selectedModelId={selectedModelId} 
            onModelSelect={setSelectedModelId} 
            loading={loadingModels} 
          />
        </section>

        <section className="pt-6 border-t border-dark-border text-right flex items-center justify-between">
          <div className="text-red-400 text-sm">{error}</div>
          <button
            onClick={handleAnalyze}
            disabled={!isReady || isAnalyzing}
            className={`px-8 py-3 rounded-xl font-medium tracking-wide transition-all shadow-lg ${
              isReady && !isAnalyzing
                ? 'bg-dark-accent text-dark-bg hover:brightness-110 shadow-[0_0_20px_rgba(0,209,255,0.3)]'
                : 'bg-dark-border text-gray-500 cursor-not-allowed'
            }`}
          >
            {isAnalyzing ? (
              <span className="flex items-center space-x-2">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : 'Analyze Face'}
          </button>
        </section>
      </main>
    </div>
  );
};

export default LandingPage;
