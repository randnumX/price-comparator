// App.js
import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomeComponent from './components/HomeComponent';
import Footer from './components/Footer';
import './App.css';

function App() {
  const [searchType, setSearchType] = useState('shopping');

  const handleSearchTypeChange = (newType) => {
    setSearchType(newType);
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Header searchType={searchType} onSearchTypeChange={handleSearchTypeChange} />
        <div className="content">
          <Routes>
            <Route path="/" element={<HomeComponent searchType={searchType} />} />
            <Route path="*" element={<div>404 Not Found</div>} />
          </Routes>
        </div>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;