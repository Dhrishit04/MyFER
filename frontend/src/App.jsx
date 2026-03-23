import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ResultPage from './pages/ResultPage';

function App() {
  return (
    <div className="min-h-screen bg-dark-bg text-gray-200">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/result" element={<ResultPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
