import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { QRCodeSVG } from 'qrcode.react';
import { X, Download, Printer } from 'lucide-react';

export default function QRModal({ photoUrl, onClose, onPrint }) {
    const [timeLeft, setTimeLeft] = React.useState(10);

    React.useEffect(() => {
        if (!photoUrl) return;
        const timer = setInterval(() => {
            setTimeLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(timer);
                    onClose(); // Auto close at 0
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
        return () => clearInterval(timer);
    }, [photoUrl, onClose]);

    // Reset timer on new open
    React.useEffect(() => {
        if (photoUrl) setTimeLeft(10);
    }, [photoUrl]);

    if (!photoUrl) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4"
                onClick={onClose}
            >
                <motion.div
                    initial={{ scale: 0.9, y: 30 }}
                    animate={{ scale: 1, y: 0 }}
                    exit={{ scale: 0.9, y: 30 }}
                    className="relative bg-[#0a0a0a] border-2 border-stranger-red shadow-[0_0_30px_rgba(229,9,20,0.5)] rounded-2xl p-10 max-w-sm w-full flex flex-col items-center"
                    onClick={(e) => e.stopPropagation()}
                >
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
                    >
                        <X size={24} />
                    </button>

                    <div className="bg-white p-4 rounded-xl mb-6 flex-shrink-0">
                        <QRCodeSVG value={photoUrl} size={180} />
                    </div>

                    <h2 className="font-sans text-xl tracking-[0.1em] text-white mb-2 text-center uppercase">
                        Scan To Download
                    </h2>

                    <div className="flex gap-4 w-full mt-4 mb-6">
                        <a
                            href={photoUrl}
                            download
                            target="_blank"
                            rel="noreferrer"
                            className="flex-1 text-center bg-stranger-red/20 border border-stranger-red hover:bg-stranger-red/40 text-white py-2 rounded-lg font-sans text-sm tracking-wider transition-colors flex items-center justify-center gap-2"
                        >
                            <Download size={16} /> Download
                        </a>
                        <button
                            onClick={() => onPrint(photoUrl)}
                            className="flex-1 bg-gray-900 border border-gray-700 hover:border-gray-500 text-gray-300 hover:text-white py-2 rounded-lg font-sans text-sm tracking-wider transition-colors flex items-center justify-center gap-2"
                        >
                            <Printer size={16} /> Print
                        </button>
                    </div>

                    <div className="flex flex-col items-center mt-2">
                        <svg width="40" height="40" viewBox="0 0 40 40">
                            <circle cx="20" cy="20" r="16" fill="none" stroke="#333" strokeWidth="3" />
                            <circle cx="20" cy="20" r="16" fill="none" stroke="#E50914" strokeWidth="3"
                                strokeDasharray="100"
                                strokeDashoffset={100 - (timeLeft / 10) * 100}
                                strokeLinecap="round"
                                transform="rotate(-90 20 20)"
                                style={{ transition: 'stroke-dashoffset 1s linear' }}
                            />
                        </svg>
                        <p className="font-mono text-gray-500 text-xs mt-2">
                            Auto close {timeLeft}s
                        </p>
                    </div>

                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
}
