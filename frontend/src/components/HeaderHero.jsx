import React from 'react';
import { motion } from 'framer-motion';

export default function HeaderHero() {
    return (
        <div className="relative w-full h-[180px] flex flex-col items-center justify-center overflow-hidden border-b border-stranger-red/30 bg-black">
            {/* Background GIF */}
            <div
                className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-40 mix-blend-screen"
                style={{ backgroundImage: "url('/s3.gif')", backgroundPosition: "center 20%" }}
            />

            {/* Dark Overlay */}
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[#0a0a0a] opacity-90" />
            <div className="absolute inset-0 bg-stranger-red opacity-[0.15] mix-blend-multiply" />

            {/* Hero Content */}
            <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                className="relative z-10 flex flex-col items-center text-center mt-4"
            >
                <h1 className="font-creep text-5xl md:text-7xl text-stranger-red text-glow-red animate-flicker tracking-widest leading-none m-0 p-0">
                    MAGIC
                </h1>
                <h2 className="font-sans text-sm md:text-md text-white mt-2 tracking-[0.2em] opacity-80 uppercase font-medium">
                    IEEE Hackathon 2026
                </h2>
            </motion.div>
        </div>
    );
}
