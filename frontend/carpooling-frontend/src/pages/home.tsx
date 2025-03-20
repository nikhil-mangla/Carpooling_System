"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Menu, X,  Coins, Users, MapPin, } from "lucide-react"; 

export default function RideShare() {
  const [from, setFrom] = useState("");
  const [date, setDate] = useState("");
  const [to, setTo] = useState("");

  const [seats, setSeats] = useState<number | "">("");
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="flex flex-col min-h-screen bg-[#111418] text-white">
      
    
      <nav className="flex justify-between items-center px-6 py-4 bg-[#1c2126] shadow-md fixed top-0 left-0 right-0 z-50">
       
        <h1 className="text-2xl font-bold text-white">ShareRide</h1>

        {/* Right - Desktop Menu */}
        <div className="hidden md:flex gap-6">
          <Link href="/home" className="hover:text-gray-300">Home</Link>
          <Link href="/messages" className="hover:text-gray-300">Messages</Link>
          <Link href="/profile" className="hover:text-gray-300">Profile</Link>
        </div>

        {/* Mobile Menu Button */}
        <button className="md:hidden" onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </nav>

     
      {menuOpen && (
        <div className="md:hidden flex flex-col items-center bg-[#111827] py-4">
          <Link href="/" className="py-2 hover:text-gray-300">Home</Link>
          <Link href="/messages" className="py-2 hover:text-gray-300">Messages</Link>
          <Link href="/profile" className="py-2 hover:text-gray-300">Profile</Link>
        </div>
      )}

      {/* Main Content */}
      <div className="flex justify-center grow p-5">
        <div className="flex flex-col grow">
          <div>
          <br />
          <br />
          <br />
          </div>
         
          <div className="flex flex-col items-center justify-center self-stretch">
          <div className="relative w-1/2 h-[480px] rounded-xl overflow-hidden mx-auto" style={{ width: '80%', height: '420px' }} >
          
            <Image 
                src="/ridesharing.png"
                alt="Ridesharing Image"
                layout="fill"
                objectFit="cover"
                priority
            />

            
            <div className="absolute inset-0 flex justify-center items-center bg-black/40">
                <span className="text-white text-4xl font-extrabold text-center px-6">
                Ridesharing for groups. The more, the merrier.
                </span>
            </div>
            </div>
           
          </div>

          
          <div className="flex flex-wrap items-end gap-4 px-4 py-3 justify-center">
            <div className="w-[216px] flex flex-col mr-4">
              <span className="font-medium text-base text-white pb-2 text-center">Leaving From</span>
              <div className="relative">
     
               <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    placeholder="Enter location"
                    value={from}
                    onChange={(e) => setFrom(e.target.value)}
                    className="h-8 w-full bg-[#293038] p-6 pl-10 rounded-xl text-white outline-none text-center"
                  />
                </div>
            </div>

            <div className="w-[216px] flex flex-col">
              <span className="font-medium text-base text-white pb-2 text-center">Going To</span>

              <div className="relative">
              <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input 
                type="text" 
                placeholder="Enter destination"  style={{ textAlign: 'center' }}
                value={to}
                onChange={(e) => setTo(e.target.value)}
                className="h-8 bg-[#293038] p-6 rounded-xl text-white outline-none"
              />
              </div>
            </div>

            <div className="w-[216px] flex flex-col">
              <span className="font-medium text-base text-white pb-2 text-center">Date</span>

              <input 
                type="date" 
                placeholder="Today"  style={{ textAlign: 'center' }}
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="h-8 bg-[#293038] p-6 rounded-xl text-white outline-none"
              />
            </div>

            <div className="w-[216px] flex flex-col">
              <span className="font-medium text-base text-white pb-2 text-center">Seats</span>
              
              <input 
                type="number" 
                placeholder="1 passenger"  style={{ textAlign: 'center' }}
                min="1" 
                max="7" 
                value={seats}
                onChange={(e) => setSeats(e.target.value ? Number(e.target.value) : "")}
                className="h-8 bg-[#293038] p-6 rounded-xl text-white outline-none"
              />
            </div>

          </div>

          <div className="w-full flex justify-center py-3">
            <button className="flex justify-center items-center h-10 bg-[#1c7ad9] px-4 rounded-xl text-white font-bold text-[14px]">
              Search
            </button>
          </div>
          <div className="flex flex-col md:flex-row items-center justify-center gap-10 mt-6 px-4 text-center">
    
      
            <div className="flex flex-col items-center max-w-sm text-white">
              <Coins className="w-10 h-10 text-gray-400 mb-3" /> 
              <h3 className="font-bold text-lg text-gray-100 text-center">
                Your pick of rides at low prices
              </h3>
              <p className="text-gray-400 mt-1 text-left">
                No matter where you’re going, by bus or carpool, find the perfect ride 
                from our wide range of destinations and routes at low prices.
              </p>
            </div>


            <div className="flex flex-col items-center max-w-sm text-white">
              <Users className="w-10 h-10 text-gray-400 mb-3" />
              <h3 className="font-bold text-lg text-gray-100 text-center">
                Trust who you travel with
              </h3>
              <p className="text-gray-400 mt-1 text-left">
                We take the time to get to know each of our members and bus partners. 
                We check reviews, profiles, and IDs, so you know who you&apos;re traveling 
                with and can book your ride at ease on our secure platform.
              </p>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}