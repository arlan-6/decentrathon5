import { useEffect, useState } from "react";
import { Button } from "./components/ui/button";
import { isLoggedIn, logoutCandidate } from "./lib/auth";
import { Link } from "react-router";

function App() {
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);

  useEffect(() => {
    setIsUserLoggedIn(isLoggedIn());
  }, [isLoggedIn,setIsUserLoggedIn]);
  

  const logout = () => {
    logoutCandidate();
    setIsUserLoggedIn(false);
  }

  return (
    <main className="min-h-screen px-6 py-8">
      {!isUserLoggedIn ? (
        <div className="flex gap-3">
          <Link to="/login">
            <Button>Login</Button>
          </Link>
          <Link to="/register">
            <Button variant="outline">Register</Button>
          </Link>
        </div>
      ) : (
        <div className="">
          <h1 className="text-2xl font-bold">Welcome to Decentrathon!</h1>
          <Button onClick={() => logout()}>Logout</Button>
        </div>
      )}
    </main>
  );
}

export default App;
