import React from 'react';
import { motion } from 'framer-motion';

export default function HeaderHero() {
    return (
        <div className="relative w-full h-[40vh] md:h-[50vh] flex flex-col items-center justify-center overflow-hidden border-b-2 border-stranger-red box-glow-red bg-black">
            {/* Background GIF */}
            <div
                className="absolute inset-0 bg-cover bg-center opacity-30 mix-blend-screen"
                style={{ backgroundImage: "url('/s3.gif')" }}
            />

            {/* Gradients & Vignetting */}
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-stranger-dark opacity-90" />
            <div className="absolute inset-0 bg-stranger-red opacity-10 mix-blend-multiply" />

            {/* Hero Content */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                className="relative z-10 flex flex-col items-center text-center"
            >
                <h1 className="font-creep text-7xl md:text-9xl text-stranger-red text-glow-red animate-flicker tracking-widest leading-none m-0 p-0">
                    MAGIC
                </h1>
                <h2 className="font-horror text-xl md:text-3xl text-white mt-4 tracking-widest opacity-80 uppercase text-glow-red">
                    IEEE Hackathon 2026
                </h2>
            </motion.div>

            {/* Scanner Element */}
            <div className="absolute top-0 left-0 w-full h-[2px] bg-white opacity-20 shadow-[0_0_10px_#E50914] animate-[scan_4s_linear_infinite]" />
            <style dangerouslySetInnerHTML={{
                __html: `
        @keyframes scan {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(50vh); }
        }
      `}} />
        </div>
    );
}
