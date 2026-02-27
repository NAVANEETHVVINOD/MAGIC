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
                <h1
                    className="font-creep text-6xl md:text-8xl tracking-widest leading-none m-0 p-0"
                    style={{
                        WebkitTextStroke: '2px #E50914',
                        color: 'transparent',
                        filter: 'drop-shadow(0 0 15px rgba(229,9,20,0.8))'
                    }}
                >
                    MAGIC
                </h1>
                <h2 className="font-sans text-sm md:text-md text-white mt-4 tracking-[0.2em] opacity-90 uppercase font-medium">
                    IEEE Hackathon 2026
                </h2>
            </motion.div>
        </div>
    );
}
