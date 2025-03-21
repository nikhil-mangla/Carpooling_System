import { useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";

const Login: React.FC = () => {
  const [username, setUsername] = useState("admin"); // Pre-fill for testing
  const [password, setPassword] = useState("admin123"); // Pre-fill for testing
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const response = await fetch("https://carpooling-backend1.onrender.com/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        router.push("/home"); // Redirect to home page after login
      } else {
        setError(data.detail || "Login failed");
      }
    } catch {
      setError("An error occurred. Please try again.");
    }
  };

  return (
    <div className="relative flex min-h-screen flex-col bg-[#111418] overflow-x-hidden font-sans">
      <div className="layout-container flex h-full grow flex-col">
        <br />
        <div
          className="w-[500%] max-w-[1200px] bg-center bg-no-repeat bg-cover flex flex-col justify-end overflow-hidden bg-[#111418] @[480px]:rounded-xl min-h-[300px] rounded-tl-[50px] rounded-tr-[50px] rounded-bl-[50px] rounded-br-[50px] mx-auto"
          style={{
            backgroundImage: "url('/background.png')",
          }}
        ></div>
        <div className="px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col w-[512px] max-w-[512px] py-5 max-w-[960px] flex-1">
            <h3 className="text-white tracking-light text-2xl font-bold leading-tight px-4 text-center pb-2 pt-5">
              Sign in or create an account
            </h3>

            {/* Error Message */}
            {error && (
              <p className="text-red-500 text-sm text-center pb-3">{error}</p>
            )}

            {/* Username Field */}
            <div className="flex flex-col max-w-[480px] items-center text-center pb-2 pt-5 mx-auto">
              <label className="flex flex-col min-w-40 w-full items-center">
                <p className="text-white text-base font-medium leading-normal pb-2">Username</p>
                <input
                  type="text"
                  placeholder="admin"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="form-input w-full rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#293038] h-14 placeholder:text-[#9dabb8] p-8 text-base text-center placeholder:text-lg pl-9"
                />
              </label>
            </div>

            {/* Password Field */}
            <div className="flex flex-col max-w-[480px] items-center text-center py-3 mx-auto">
              <label className="flex flex-col min-w-40 w-full items-center">
                <p className="text-white text-base font-medium leading-normal pb-2">Password</p>
                <input
                  type="password"
                  placeholder="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="form-input w-full rounded-xl text-white focus:outline-0 focus:ring-0 border-none bg-[#293038] h-14 placeholder:text-[#9dabb8] p-8 text-base text-center placeholder:text-lg pl-9"
                />
              </label>
            </div>

            {/* Sign In Button */}
            <div className="flex justify-center py-3">
              <button
                onClick={handleLogin}
                className="flex min-w-[200px] max-w-[480px] cursor-pointer items-center justify-center rounded-xl h-10 px-4 bg-[#1b7ada] text-white text-sm font-bold hover:bg-[#166bb3] transition"
              >
                Sign in
              </button>
            </div>

            {/* Forgot Password Link */}
            <p className="text-[#9dabb8] text-sm font-normal pb-3 pt-1 text-center underline cursor-pointer">
              Forgot your password?
            </p>

            {/* Sign Up Link */}
            <p className="text-[#9dabb8] text-sm font-normal pb-3 pt-1 text-center">
              Don&apos;t have an account?  
              <Link href="/signup" className="text-[#1b7ada] underline cursor-pointer hover:text-[#166bb3] transition">
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;