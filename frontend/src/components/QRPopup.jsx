import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { QRCodeSVG } from 'qrcode.react';
import { X } from 'lucide-react';

export default function QRPopup({ photoUrl, onClose }) {
    if (!photoUrl) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4"
                onClick={onClose}
            >
                <motion.div
                    initial={{ scale: 0.8, y: 50 }}
                    animate={{ scale: 1, y: 0 }}
                    exit={{ scale: 0.8, y: 50 }}
                    className="relative bg-stranger-dark border-2 border-stranger-red box-glow-red rounded-xl p-8 max-w-sm w-full flex flex-col items-center"
                    onClick={(e) => e.stopPropagation()}
                >
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 text-gray-400 hover:text-white"
                    >
                        <X size={24} />
                    </button>

                    <h2 className="font-horror text-2xl text-stranger-red text-glow-red mb-6 text-center">
                        YOUR CAPTURE IS READY
                    </h2>

                    <div className="bg-white p-4 rounded-lg mb-6 shadow-[0_0_15px_rgba(255,255,255,0.2)]">
                        <QRCodeSVG value={photoUrl} size={200} />
                    </div>

                    <p className="font-mono text-gray-400 text-sm text-center">
                        Scan to download your photo
                    </p>
                    <p className="font-horror tracking-widest text-stranger-red text-xs mt-4 opacity-50 uppercase">
                        Welcome to the upside down
                    </p>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
}
