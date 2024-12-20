import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SlideNavbar from "./SlideNavbar";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/slide-navbar" element={<SlideNavbar />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
