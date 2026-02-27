import React from 'react';
import { motion } from 'framer-motion';
import { Download, Printer, Trash2 } from 'lucide-react';

export default function PhotoCard({ photo, onDelete, onPrint }) {
    const isAdmin = !!localStorage.getItem('MAGIC_ADMIN_KEY');

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="relative group w-full rounded-md overflow-hidden border border-gray-800 hover:border-stranger-red transition-all duration-500 bg-black"
        >
            <img
                src={photo.url}
                alt={photo.filename}
                className="w-full h-auto object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-300"
                loading="lazy"
            />

            {/* Overlay Actions */}
            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-center items-center gap-4">
                <a
                    href={photo.url}
                    download={photo.filename}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-2 bg-stranger-red/20 text-white px-4 py-2 rounded-md border border-stranger-red hover:bg-stranger-red/40 transition-colors cursor-pointer"
                >
                    <Download size={18} /> Download
                </a>

                <button
                    onClick={() => onPrint(photo.url)}
                    className="flex items-center gap-2 bg-gray-800/80 text-white px-4 py-2 rounded-md border border-gray-600 hover:bg-gray-700 transition-colors"
                >
                    <Printer size={18} /> Print
                </button>

                {isAdmin && (
                    <button
                        onClick={() => onDelete(photo.id)}
                        className="absolute top-2 right-2 text-red-500 hover:text-red-400 p-2 bg-black/50 rounded-full"
                        title="Admin Delete"
                    >
                        <Trash2 size={16} />
                    </button>
                )}
            </div>

            {/* Timestamp */}
            <div className="absolute bottom-0 left-0 w-full p-2 bg-gradient-to-t from-black to-transparent pointer-events-none">
                <p className="text-xs text-gray-400 font-mono text-center">
                    {new Date(photo.created_at).toLocaleString()}
                </p>
            </div>
        </motion.div>
    );
}
