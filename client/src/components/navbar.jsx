import React, { useCallback } from 'react';
import 'tailwindcss/tailwind.css';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';

const Navbar = () => {

  const navigate = useNavigate();

  const scrollToSection = useCallback((elementId) => {
    document.getElementById(elementId)?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  return (
    <nav className="fixed top-0 w-full border-b bg-gray-50 shadow-md z-20">
      <div className="max-w-[95%] md:max-w-[85%] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0 flex justify-center items-center gap-5">
            {/* <img src={logo} alt="logo" className="w-12 h-12 md:w-16 mb:h-16 mb-2" /> */}
            <p className="text-xl font-extrabold cursor-pointer flex flex-col">
              <span className="text-sm mb:text-md bg-gradient-to-r from-indigo-600 via-purple-500 to-pink-500 bg-clip-text text-transparent animate-gradient">
                SBI Life Insurance Advisor
              </span>
              <span className="text-xs md:text-sm bg-gradient-to-r from-indigo-600 via-purple-500 to-pink-500 bg-clip-text text-transparent animate-gradient">Team One Piece</span>
            </p>
          </div>

          {/* Navigation Menu */}
          <div className="hidden md:flex space-x-8 items-center">
            <a
              // href="#home"
              onClick={() => navigate('/')}
              className="relative text-gray-700 font-medium hover:text-indigo-600 transition-colors duration-300 group"
            >
              Home
              <span className="absolute left-0 bottom-0 w-0 h-0.5 bg-indigo-600 transition-all duration-300 group-hover:w-full"></span>
            </a>
            <a
              onClick={() => scrollToSection('policies')}
              className="relative text-gray-700 font-medium hover:text-indigo-600 transition-colors duration-300 group"
            >
              Policy Plans
              <span className="absolute left-0 bottom-0 w-0 h-0.5 bg-indigo-600 transition-all duration-300 group-hover:w-full"></span>
            </a>
            <a
              onClick={() => scrollToSection('team')}
              className="relative text-gray-700 font-medium hover:text-purple-600 transition-colors duration-300 group"
            >
              Team
              <span className="absolute left-0 bottom-0 w-0 h-0.5 bg-purple-600 transition-all duration-300 group-hover:w-full"></span>
            </a>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-4">
            <button
              className="hidden md:inline-flex bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-2 rounded-lg font-medium shadow-lg transition-transform duration-300 hover:scale-105"
              onClick={() => navigate('/customer/login')}
            >
              Customer
            </button>
            <button
              className="hidden md:inline-flex bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-2 rounded-lg font-medium shadow-lg transition-transform duration-300 hover:scale-105"
              onClick={() => navigate('/rm/login')}
            >
              Relation Ship Managers
            </button>
            <button className="md:hidden focus:outline-none text-gray-700">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                strokeWidth={2}
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
