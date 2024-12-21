import React, { useState } from "react";
import 'tailwindcss/tailwind.css';

const Login = () => {
  const [isSignUp, setIsSignUp] = useState(false);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-[#0f0c29] via-[#302b63] to-[#24243e]">
      <div className="relative w-[350px] h-[500px] bg-cover bg-center rounded-lg shadow-lg overflow-hidden" style={{ backgroundImage: 'url("1.jpg")' }}>
        {/* Sign-Up Form */}
        <div
          className={`absolute inset-0 bg-gray-200 rounded-[20px] transform transition-transform duration-1000 ease-in-out ${
            isSignUp ? "translate-y-0" : "-translate-y-full"
          }`}
        >
          <form className="flex flex-col items-center justify-center h-full px-6">
            <label
              className="absolute bottom-4 left-1/2 transform -translate-x-1/2 text-[#573b8a] font-bold text-[2.3em] cursor-pointer"
              onClick={() => setIsSignUp(false)}
            >
              Sign Up
            </label>
            <input
              type="text"
              placeholder="User name"
              className="w-[60%] h-[40px] bg-gray-300 rounded-md px-4 mb-4 outline-none"
              required
            />
            <input
              type="email"
              placeholder="Email"
              className="w-[60%] h-[40px] bg-gray-300 rounded-md px-4 mb-4 outline-none"
              required
            />
            <input
              type="password"
              placeholder="Password"
              className="w-[60%] h-[40px] bg-gray-300 rounded-md px-4 mb-6 outline-none"
              required
            />
            <button
              type="submit"
              className="w-[60%] h-[40px] bg-[#573b8a] text-white font-bold rounded-md transition duration-200 hover:bg-[#6d44b8]"
            >
              Sign Up
            </button>
          </form>
        </div>

        {/* Login Form */}
        <div
          className={`absolute inset-0 bg-transparent transform transition-transform duration-1000 ease-in-out ${
            isSignUp ? "translate-y-full" : "translate-y-0"
          }`}
        >
          <form className="flex flex-col items-center justify-center h-full px-6">
            <label
              className="absolute top-4 left-1/2 transform -translate-x-1/2 text-white font-bold text-[2.3em] cursor-pointer"
              onClick={() => setIsSignUp(true)}
            >
              Login
            </label>
            <input
              type="email"
              placeholder="Email"
              className="w-[60%] h-[40px] bg-gray-300 rounded-md px-4 mb-4 outline-none"
              required
            />
            <input
              type="password"
              placeholder="Password"
              className="w-[60%] h-[40px] bg-gray-300 rounded-md px-4 mb-6 outline-none"
              required
            />
            <button
              type="submit"
              className="w-[60%] h-[40px] bg-[#573b8a] text-white font-bold rounded-md transition duration-200 hover:bg-[#6d44b8]"
            >
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
