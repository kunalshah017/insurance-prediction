// SlideNavbar.js
import React, { useState } from "react";


const SlideNavbar = () => {
  const [isSignUp, setIsSignUp] = useState(false);

  return (
    <div className="main">
      <input
        type="checkbox"
        id="chk"
        aria-hidden="true"
        checked={isSignUp}
        onChange={() => setIsSignUp(!isSignUp)}
      />
      <div className="signup">
        <form>
          <label htmlFor="chk" aria-hidden="true" onClick={() => setIsSignUp(true)}>
            Sign up
          </label>
          <input type="text" name="txt" placeholder="User name" required />
          <input type="email" name="email" placeholder="Email" required />
          <input type="password" name="pswd" placeholder="Password" required />
          <button>Sign up</button>
        </form>
      </div>
      <div className="login">
        <form>
          <label htmlFor="chk" aria-hidden="true" onClick={() => setIsSignUp(false)}>
            Login
          </label>
          <input type="email" name="email" placeholder="Email" required />
          <input type="password" name="pswd" placeholder="Password" />
          <button>Login</button>
        </form>
      </div>
    </div>
  );
};

export default SlideNavbar;
