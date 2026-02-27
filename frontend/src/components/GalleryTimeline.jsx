import React from 'react';
import { motion } from 'framer-motion';
import PhotoCard from './PhotoCard';

export default function GalleryTimeline({ photos, onDelete, onPrint }) {
    if (!photos || photos.length === 0) {
        return (
            <div className="w-full text-center py-20 text-gray-500 font-horror tracking-widest">
                THE VOID IS EMPTY
            </div>
        );
    }

    return (
        <div className="relative w-full max-w-5xl mx-auto py-12 px-4">
            {/* Center Line */}
            <div className="absolute left-1/2 top-0 bottom-0 w-1 bg-stranger-red/20 -translate-x-1/2 rounded-full hidden md:block" />

            <div className="space-y-12">
                {photos.map((photo, index) => {
                    const isLeft = index % 2 === 0;
                    return (
                        <div key={photo.id} className="relative w-full flex justify-center md:justify-between items-center px-0 md:px-8">

                            {/* Timeline Node */}
                            <div className="hidden md:block absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-stranger-red rounded-full box-glow-red z-10" />

                            {/* Photo Box */}
                            <motion.div
                                initial={{ opacity: 0, x: isLeft ? -50 : 50 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true, margin: "-100px" }}
                                transition={{ duration: 0.8, type: "spring" }}
                                className={`w-full md:w-[45%] ${isLeft ? 'md:mr-auto' : 'md:ml-auto'}`}
                            >
                                <div className="p-2 border border-stranger-red/30 rounded-lg bg-black box-glow-red">
                                    <PhotoCard
                                        photo={photo}
                                        onDelete={onDelete}
                                        onPrint={onPrint}
                                    />
                                </div>
                            </motion.div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
