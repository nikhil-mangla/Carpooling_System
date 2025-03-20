"use client";

import { useState } from "react";
import { TextField, Button, Typography, AppBar, Toolbar, Container, Box } from "@mui/material";
import axios from "axios";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const router = useRouter();

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Handle form submission
  const handleSignup = async () => {
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/register/`, formData);
      router.push("/login");
    } catch (error) {
      console.error("Signup error:", error);
    }
  };

  return (
    <Box sx={{ flexGrow: 1, backgroundColor: "#111418", minHeight: "100vh" }}>
      {/* Navbar */}
      <AppBar position="static" sx={{ backgroundColor: "#1c2126", padding: 1 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: "bold", color: "#fff" }}>
            RideShare
          </Typography>
        </Toolbar>
      </AppBar>

   
      <Container maxWidth="sm" sx={{ mt: 5, backgroundColor: "#1c2126", p: 4, borderRadius: 4 }}>
        <Typography variant="h5" align="center" color="white" fontWeight="bold" gutterBottom>
          Create an Account
        </Typography>

        <TextField
          label="Username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          fullWidth
          margin="normal"
          variant="outlined"
          InputProps={{ style: { color: "white" } }}
          InputLabelProps={{ style: { color: "#9dabb8" } }}
        />

        <TextField
          label="Email"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          fullWidth
          margin="normal"
          variant="outlined"
          InputProps={{ style: { color: "white" } }}
          InputLabelProps={{ style: { color: "#9dabb8" } }}
        />

        <TextField
          label="Password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          fullWidth
          margin="normal"
          variant="outlined"
          InputProps={{ style: { color: "white" } }}
          InputLabelProps={{ style: { color: "#9dabb8" } }}
        />

        <Button variant="contained" fullWidth sx={{ mt: 2, backgroundColor: "#1b7ada" }} onClick={handleSignup}>
          Sign Up
        </Button>

        <Typography variant="body2" align="center" sx={{ color: "#9dabb8", mt: 2 }}>
          Already have an account?
          <Link href="/login" className="text-[#1b7ada] underline cursor-pointer hover:text-[#166bb3] transition">
                Log in
           </Link>
        </Typography>
      </Container>
    </Box>
  );
}