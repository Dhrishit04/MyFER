import React, { useCallback, useState } from 'react';
import { UploadCloud, X, FileImage } from 'lucide-react';

const ImageUploader = ({ onImageSelect, selectedImage }) => {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const validateAndSetImage = (file) => {
    setError(null);
    if (!file) return;

    // Validate type
    if (file.type !== "image/jpeg" && file.type !== "image/png" && file.type !== "image/jpg") {
      setError("Only JPG and PNG files are supported.");
      return;
    }

    // Validate size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError("File size must be under 10MB.");
      return;
    }

    onImageSelect(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetImage(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      validateAndSetImage(e.target.files[0]);
    }
  };

  const handleClear = () => {
    onImageSelect(null);
    setError(null);
  };

  return (
    <div className="w-full">
      {!selectedImage ? (
        <label 
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-xl cursor-pointer transition-colors ${dragActive ? 'border-dark-accent bg-dark-accent/10' : 'border-dark-border bg-dark-card hover:bg-dark-border/50'}`}
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <UploadCloud className={`w-12 h-12 mb-4 ${dragActive ? 'text-dark-accent' : 'text-gray-400'}`} />
            <p className="mb-2 text-sm text-gray-300"><span className="font-semibold text-dark-accent">Click to upload</span> or drag and drop</p>
            <p className="text-xs text-gray-500">PNG, JPG up to 10MB</p>
          </div>
          <input type="file" className="hidden" accept=".jpg,.jpeg,.png" onChange={handleChange} />
        </label>
      ) : (
        <div className="glass-card p-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 rounded overflow-hidden bg-black/50 border border-dark-border flex items-center justify-center">
              <img src={URL.createObjectURL(selectedImage)} alt="Preview" className="w-full h-full object-cover" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-200 truncate max-w-[200px]">{selectedImage.name}</p>
              <p className="text-xs text-gray-500">{(selectedImage.size / (1024 * 1024)).toFixed(2)} MB</p>
            </div>
          </div>
          <button 
            type="button" 
            onClick={handleClear}
            className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-400/10 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      )}
      
      {error && (
        <p className="mt-2 text-sm text-red-400">{error}</p>
      )}
    </div>
  );
};

export default ImageUploader;
