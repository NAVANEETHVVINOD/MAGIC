import React from 'react';
import { motion } from 'framer-motion';
import { ThumbsUp } from 'lucide-react';

export default function CameraView() {
    return (
        <div className="w-full max-w-[900px] aspect-video relative rounded-lg overflow-hidden border border-stranger-red box-glow-red bg-black/50 mx-auto my-8 flex flex-col items-center justify-center">

            {/* Mock Camera Container */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none opacity-80">
                <motion.div
                    animate={{ scale: [1, 1.1, 1], opacity: [0.7, 1, 0.7] }}
                    transition={{ duration: 2, repeat: Infinity }}
                >
                    <ThumbsUp size={64} className="text-green-500 box-glow-green rounded-full p-4 mb-4" />
                </motion.div>
                <h3 className="text-2xl md:text-4xl font-horror text-green-500 text-glow-green text-center">
                    Show Thumbs Up To Capture
                </h3>
                <p className="text-gray-400 mt-4 text-sm tracking-widest uppercase font-horror">
                    [ Live Feed Active on Camera Unit ]
                </p>
            </div>

            {/* Decorative corners */}
            <div className="absolute top-4 left-4 w-8 h-8 border-t-2 border-l-2 border-stranger-red opacity-50" />
            <div className="absolute top-4 right-4 w-8 h-8 border-t-2 border-r-2 border-stranger-red opacity-50" />
            <div className="absolute bottom-4 left-4 w-8 h-8 border-b-2 border-l-2 border-stranger-red opacity-50" />
            <div className="absolute bottom-4 right-4 w-8 h-8 border-b-2 border-r-2 border-stranger-red opacity-50" />

            {/* REC Indicator */}
            <div className="absolute top-6 right-8 flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-600 animate-pulse box-glow-red" />
                <span className="font-mono text-stranger-red tracking-widest font-bold">REC</span>
            </div>
        </div>
    );
}
