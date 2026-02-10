// components/AuthModal.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

type AuthModalProps = {
  type: "signin" | "signup" | "otp";
  onClose: () => void;
};

export default function AuthModal({ type, onClose }: AuthModalProps) {
  const router = useRouter();
  const [modalType, setModalType] = useState(type);
  const [userType, setUserType] = useState<"attendee" | "organizer">("attendee");
  const [formData, setFormData] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [otp, setOtp] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignIn = () => {
    const { username, password } = formData;
    if (username === "mcsAdmin" && password === "mcsAdmin") router.push("/admin");
    else if (username === "Ali" && password === "ali") router.push("/organizer");
    else if (username === "Akrash" && password === "Akrash") router.push("/attendee");
    else if (username === "staff" && password === "staff") router.push("/staff");
    else setModalType("signin"); // retry
  };

  const handleSignUp = () => setModalType("otp");

  const handleOtpSubmit = () => {
    setModalType(null);
    router.push("/attendee"); // new signup defaults to attendee
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-mcs-light rounded-lg p-8 w-96 relative">
        <button onClick={onClose} className="absolute top-3 right-3 text-gray-dark font-bold">X</button>

        {modalType === "signin" && (
          <>
            <h2 className="text-2xl font-bold mb-4 text-mcs-red text-center">Sign In</h2>
            <input name="username" placeholder="Username" value={formData.username} onChange={handleChange} className="w-full p-3 rounded border mb-3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} className="w-full p-3 rounded border mb-3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <button onClick={handleSignIn} className="w-full bg-mcs-red text-mcs-light p-3 rounded font-semibold hover:bg-red-700">Sign In</button>
          </>
        )}

        {modalType === "signup" && (
          <>
            <h2 className="text-2xl font-bold mb-4 text-mcs-red text-center">Sign Up</h2>
            <input name="username" placeholder="Username" value={formData.username} onChange={handleChange} className="w-full p-3 rounded border mb-3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <input name="email" placeholder="Email" value={formData.email} onChange={handleChange} className="w-full p-3 rounded border mb-3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} className="w-full p-3 rounded border mb-3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <input type="password" name="confirmPassword" placeholder="Confirm Password" value={formData.confirmPassword} onChange={handleChange} className="w-full p-3 rounded border mb-3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />

            <div className="mb-3">
              <label className="mr-3">
                <input type="radio" name="role" value="attendee" checked={userType==="attendee"} onChange={()=>setUserType("attendee")} className="mr-1" /> Attendee
              </label>
              <label>
                <input type="radio" name="role" value="organizer" checked={userType==="organizer"} onChange={()=>setUserType("organizer")} className="mr-1" /> Organizer
              </label>
            </div>

            <button onClick={handleSignUp} className="w-full bg-mcs-red text-mcs-light p-3 rounded font-semibold hover:bg-red-700">Sign Up</button>
          </>
        )}

        {modalType === "otp" && (
          <>
            <h2 className="text-2xl font-bold mb-4 text-mcs-red text-center">Enter OTP</h2>
            <p className="mb-3 text-gray-dark text-center">We sent a mock OTP to {formData.email}</p>
            <input type="text" placeholder="Enter OTP" value={otp} onChange={(e)=>setOtp(e.target.value)} className="w-full p-3 rounded border mb-3 focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <button onClick={handleOtpSubmit} className="w-full bg-mcs-red text-mcs-light p-3 rounded font-semibold hover:bg-red-700">Verify OTP</button>
          </>
        )}
      </div>
    </div>
  );
}
