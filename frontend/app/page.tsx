"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";

const features = [
  { title: "AI Networking", desc: "Connect with like-minded participants easily." },
  { title: "Smart Schedule", desc: "Plan your sessions and workshops efficiently." },
  { title: "Interactive Floor Plan", desc: "Explore venues and booths visually." },
];

const testimonials = [
  { name: "Ali Khan", role: "Participant", msg: "Amazing experience! Learned a lot." },
  { name: "Sara Ahmed", role: "Organizer", msg: "The platform made event management seamless." },
];

const faqs = [
  { q: "Who can participate?", a: "All MCS students and faculty are welcome to join." },
  { q: "Is registration free?", a: "Yes, early registration is free for the first 100 participants." },
  { q: "Can I attend workshops online?", a: "Yes, selected sessions are streamed virtually." },
];

export default function LandingPage() {
  const router = useRouter();
  const [showTopBtn, setShowTopBtn] = useState(false);
  const [modalType, setModalType] = useState<"signin" | "signup" | "otp" | null>(null);
  const [userType, setUserType] = useState<"attendee" | "organizer">("attendee");
  const [formData, setFormData] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [otp, setOtp] = useState("");
const [currentIndex, setCurrentIndex] = useState(0);
const imageWidth = 300; // width of each image
const gap = 16; // gap between images (tailwind `gap-4` = 16px)
const visibleCount = 2; // show 2 images at a time

  useEffect(() => {
    const handleScroll = () => setShowTopBtn(window.scrollY > 300);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => window.scrollTo({ top: 0, behavior: "smooth" });

  const openSignIn = () => setModalType("signin");
  const openSignUp = () => setModalType("signup");
  const closeModal = () => setModalType(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignIn = () => {
    const { username, password } = formData;
    if (username === "mcsAdmin" && password === "mcsAdmin") router.push("/admin/dashboard");
    else if (username === "Ali" && password === "ali") router.push("/organizer/dashboard");
    else if (username === "Akrash" && password === "Akrash") router.push("/attendee");
    else if (username === "staff" && password === "staff") router.push("/staff");
    else setModalType("signin");
  };

  const handleSignUp = () => setModalType("otp");

  const handleOtpSubmit = () => {
    setModalType(null);
    router.push("/attendee");
  };

  return (
    <div className="font-sans text-gray-800 relative">
      <header className="fixed top-0 left-0 w-full z-50 bg-mcs-red text-mcs-light shadow-md">
        <div className="container mx-auto flex justify-between items-center p-6">
          <div className="flex items-center gap-4">
            <Image src="/nust-logo.png" alt="NUST Logo" width={50} height={50} />
            <Image src="/mcs-logo.png" alt="MCS Logo" width={50} height={50} />
            <h1 className="text-2xl font-bold ml-4">MCS Olympiad</h1>
          </div>
          <div className="space-x-4">
            <button onClick={openSignIn} className="px-4 py-2 bg-mcs-yellow text-mcs-red font-semibold rounded hover:bg-yellow-400">Sign In</button>
            <button onClick={openSignUp} className="px-4 py-2 border border-mcs-yellow text-mcs-yellow rounded hover:bg-mcs-yellow hover:text-mcs-red">Sign Up</button>
          </div>
        </div>
      </header>

      {modalType && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-mcs-light rounded-lg p-8 w-96 relative">
            <button onClick={closeModal} className="absolute top-3 right-3 text-gray-dark font-bold">X</button>

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
      )}

      <main className="pt-32">
        <section className="text-center py-24 bg-gradient-to-r from-mcs-red to-nust-blue text-mcs-light">
          <h2 className="text-5xl md:text-6xl font-bold mb-4">Welcome to MCS Olympiad</h2>
          <p className="max-w-2xl mx-auto text-lg md:text-xl mb-8">Participate in the most exciting coding and innovation competitions at MCS NUST.</p>
          <section className="py-12 px-4 text-center">
  <h3 className="text-4xl font-bold mb-8 text-white">Event Gallery</h3>
  <div className="relative max-w-6xl mx-auto">
    {/* Images container */}
    <div className="flex overflow-hidden">
      <div
        className="flex transition-transform duration-300"
        style={{ transform: `translateX(-${currentIndex * (imageWidth + gap)}px)` }}
      >
        {[...Array(10)].map((_, idx) => (
          <Image
            key={idx}
            src={`/mcs-event${idx + 1}.jpg`}
            alt={`MCS Event ${idx + 1}`}
            width={300}
            height={180}
            className="flex-shrink-0 rounded shadow-lg"
          />
        ))}
      </div>
    </div>

    {/* Left/Right Buttons */}
    <button
      onClick={() => setCurrentIndex((prev) => Math.max(prev - 2, 0))}
      className="absolute top-1/2 -left-6 transform -translate-y-1/2 bg-mcs-red text-mcs-light p-2 rounded-full shadow hover:bg-red-700"
    >
      ‹
    </button>
    <button
      onClick={() =>
        setCurrentIndex((prev) => Math.min(prev + 2, 10 - visibleCount))
      }
      className="absolute top-1/2 -right-6 transform -translate-y-1/2 bg-mcs-red text-mcs-light p-2 rounded-full shadow hover:bg-red-700"
    >
      ›
    </button>
  </div>
</section>

        </section>

        <section id="about" className="py-24 px-4 text-center bg-gray-light">
          <h3 className="text-4xl font-bold mb-6 text-gray-dark">About MCS Olympiad</h3>
          <p className="max-w-3xl mx-auto text-lg text-gray-dark">MCS Olympiad is the premier event for students to showcase their skills in coding, AI, and innovation. Participants compete, network, and learn through workshops and interactive sessions. Join us for an unforgettable experience!</p>
        </section>

        <section className="py-24 px-4 text-center">
          <h3 className="text-4xl font-bold mb-12 text-gray-dark">Features</h3>
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {features.map((f, idx) => (
              <div key={idx} className="p-6 bg-mcs-light rounded shadow-lg hover:shadow-xl transition transform hover:-translate-y-1">
                <h4 className="text-2xl font-semibold mb-3 text-mcs-red">{f.title}</h4>
                <p className="text-gray-dark">{f.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="py-24 px-4 bg-gray-light text-center">
          <h3 className="text-4xl font-bold mb-12 text-gray-dark">Testimonials</h3>
          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {testimonials.map((t, idx) => (
              <div key={idx} className="p-6 bg-white rounded shadow-lg">
                <p className="italic mb-4 text-gray-dark">"{t.msg}"</p>
                <p className="font-bold text-mcs-red">{t.name}</p>
                <p className="text-gray-dark">{t.role}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="faq" className="py-24 px-4 text-center max-w-4xl mx-auto">
          <h3 className="text-4xl font-bold mb-12 text-gray-dark">FAQ</h3>
          <div className="space-y-4 text-left">
            {faqs.map((f, idx) => (
              <details key={idx} className="p-6 bg-white rounded shadow cursor-pointer">
                <summary className="font-semibold text-gray-dark">{f.q}</summary>
                <p className="mt-3 text-gray-dark">{f.a}</p>
              </details>
            ))}
          </div>
        </section>

        <section id="contact" className="py-24 px-4 bg-gray-light text-center">
          <h3 className="text-4xl font-bold mb-6 text-gray-dark">Contact Us</h3>
          <p className="mb-6 text-gray-dark">For inquiries, reach us at: <a href="mailto:olympiardmcs@nust.edu.pk" className="text-mcs-red font-semibold">olympiardmcs@nust.edu.pk</a></p>
          <form className="max-w-md mx-auto grid gap-4">
            <input type="text" placeholder="Name" className="p-3 rounded border border-gray-dark focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <input type="email" placeholder="Email" className="p-3 rounded border border-gray-dark focus:outline-none focus:ring-2 focus:ring-mcs-red" />
            <textarea placeholder="Message" className="p-3 rounded border border-gray-dark focus:outline-none focus:ring-2 focus:ring-mcs-red"></textarea>
            <button className="px-8 py-3 bg-mcs-red text-mcs-light rounded font-semibold hover:bg-red-700">Send</button>
          </form>
        </section>
      </main>

      <footer className="bg-nust-blue text-mcs-light py-8 text-center">
        <p>&copy; 2026 MCS Olympiad, NUST. All rights reserved.</p>
        <div className="flex justify-center gap-6 mt-3">
          <a href="#about" className="hover:underline">About</a>
          <a href="#faq" className="hover:underline">FAQ</a>
          <a href="#contact" className="hover:underline">Contact</a>
        </div>
      </footer>

      {showTopBtn && (
        <button onClick={scrollToTop} className="fixed bottom-6 right-6 bg-mcs-red text-mcs-light p-3 rounded-full shadow-lg hover:bg-red-700 transition">↑</button>
      )}
    </div>
  );
}
