import React from 'react';
import { Download, Printer, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function PhotoCard({ photo, isRight, onDelete, onPrint, onDownload }) {
    const isAdmin = !!localStorage.getItem('MAGIC_ADMIN_KEY');

    // Custom hook for hover state or inline state for floating quick actions
    const [isHovered, setIsHovered] = React.useState(false);

    return (
        <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: false, margin: "-100px" }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className={`relative flex items-center w-full my-12 ${isRight ? 'justify-start' : 'justify-end'}`}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <div className={`
        relative w-full max-w-[280px] md:max-w-[400px] border border-stranger-red/30 rounded-xl bg-black
        transition-all duration-500 overflow-visible
        ${isHovered ? 'scale-105 border-stranger-red box-glow-red z-20' : 'grayscale-[50%] opacity-80 z-10'}
      `}>

                {/* The Image */}
                <div className="overflow-hidden rounded-t-xl">
                    <img
                        src={photo.url}
                        alt={photo.filename}
                        className="w-full h-auto object-cover transition-transform duration-700"
                        loading="lazy"
                    />
                </div>

                {/* Footer info inside card */}
                <div className="flex items-center justify-between p-3 bg-[#0a0a0a] rounded-b-xl border-t border-gray-800">
                    <p className="text-[10px] text-gray-500 font-mono">
                        {new Date(photo.created_at).toLocaleString()}
                    </p>
                    {isAdmin && (
                        <button
                            onClick={(e) => { e.stopPropagation(); onDelete(photo.id); }}
                            className="text-red-900 hover:text-red-500 transition-colors"
                        >
                            <Trash2 size={16} />
                        </button>
                    )}
                </div>

                {/* Floating Action Menu (Shows near photo on hover) */}
                <AnimatePresence>
                    {isHovered && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, x: isRight ? 20 : -20 }}
                            animate={{ opacity: 1, scale: 1, x: isRight ? 40 : -40 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            transition={{ duration: 0.2 }}
                            className={`absolute top-1/2 -translate-y-1/2 flex flex-col gap-2 
                ${isRight ? 'right-[-80px] md:right-[-120px]' : 'left-[-80px] md:left-[-120px]'}
              `}
                        >
                            <button
                                onClick={() => onDownload(photo.url)}
                                className="bg-black/90 border border-stranger-red text-white text-xs md:text-sm px-4 py-2 rounded shadow-lg shadow-stranger-red/20 hover:bg-stranger-red/20 transition-colors backdrop-blur flex items-center justify-center gap-2 font-sans tracking-wide"
                            >
                                Download
                            </button>
                            <button
                                onClick={() => onPrint(photo.url)}
                                className="bg-[#111]/90 border border-gray-600 text-gray-300 text-xs md:text-sm px-4 py-2 rounded shadow-lg hover:border-gray-400 hover:text-white transition-colors backdrop-blur flex items-center justify-center gap-2 font-sans tracking-wide"
                            >
                                Print
                            </button>
                        </motion.div>
                    )}
                </AnimatePresence>

            </div>
        </motion.div>
    );
}
