import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { HelmetProvider } from 'react-helmet-async';


import Home from "./pages/home"
import Login from "./pages/login";

function App() {
  return (
    <HelmetProvider>
      <Router>
        <div className="App " >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/customer/login" element={<Login />} />
          </Routes>
        </div>
      </Router>
    </HelmetProvider>
  );
}

export default App;
