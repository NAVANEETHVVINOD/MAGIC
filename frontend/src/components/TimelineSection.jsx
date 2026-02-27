import React from 'react';
import GalleryTimeline from './GalleryTimeline';

export default function TimelineSection({ photos, onDelete, onPrint, onDownload }) {

    return (
        <section className="relative w-full h-[500px] overflow-hidden bg-black flex justify-center mt-10 group">

            {/* Background gradient fade top and bottom to hide items scrolling out of view */}
            <div className="absolute top-0 left-0 w-full h-16 bg-gradient-to-b from-black to-transparent z-10 pointer-events-none" />
            <div className="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-black to-transparent z-10 pointer-events-none" />

            {/* The Scrollable Viewport */}
            <div className="w-full max-w-4xl h-full overflow-y-auto overflow-x-hidden relative scroll-smooth timeline-container scrollbar-hide py-16">

                {/* Glow Energy Line */}
                <div className="absolute left-1/2 top-0 bottom-0 w-[2px] bg-stranger-red opacity-60 box-glow-red -translate-x-1/2 rounded-full hidden md:block" />

                {/* Glowing moving dot */}
                <div className="absolute left-1/2 top-[10%] w-[6px] h-[30px] bg-white opacity-80 shadow-[0_0_10px_#fff,0_0_20px_#E50914] -translate-x-1/2 rounded-full hidden md:block animate-[pulse_2s_infinite]" />

                <GalleryTimeline
                    photos={photos}
                    onDelete={onDelete}
                    onPrint={onPrint}
                    onDownload={onDownload}
                />

            </div>

            <style dangerouslySetInnerHTML={{
                __html: `
        .scrollbar-hide::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
      `}} />
        </section>
    );
}
