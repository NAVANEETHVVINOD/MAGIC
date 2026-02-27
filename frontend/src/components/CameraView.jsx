import React from 'react';
import { motion } from 'framer-motion';
import { ThumbsUp } from 'lucide-react';

export default function CameraView() {
    return (
        <div className="w-full flex justify-center py-6">
            <div className="relative w-full max-w-[1200px] h-[70vh] aspect-video rounded-3xl overflow-hidden border border-stranger-red/50 box-glow-red bg-black/80 flex flex-col items-center justify-center shadow-[0_0_50px_rgba(229,9,20,0.15)]">

                {/* Subtle Vignette Gradient */}
                <div className="absolute inset-0 rounded-3xl pointer-events-none" style={{ background: 'radial-gradient(circle, transparent 60%, rgba(0,0,0,0.8) 100%)' }} />

                {/* Mock Camera Instruction */}
                <div className="absolute inset-0 flex flex-row items-center justify-center pointer-events-none">
                    <motion.div
                        animate={{ opacity: [0.6, 1, 0.6] }}
                        transition={{ duration: 2.5, repeat: Infinity }}
                        className="flex items-center gap-4 bg-black/40 px-8 py-4 rounded-xl border border-stranger-red/20 backdrop-blur-sm"
                    >
                        <ThumbsUp size={32} className="text-stranger-red" />
                        <span className="text-xl md:text-2xl font-sans tracking-[0.15em] text-white uppercase text-glow-red">
                            Show thumbs up to capture
                        </span>
                    </motion.div>
                </div>

            </div>
        </div>
    );
}
