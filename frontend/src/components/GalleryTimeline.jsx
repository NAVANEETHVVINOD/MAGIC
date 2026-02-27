import React from 'react';
import PhotoCard from './PhotoCard';

export default function GalleryTimeline({ photos, onDelete, onPrint, onDownload }) {
    if (!photos || photos.length === 0) {
        return (
            <div className="w-full text-center py-20 text-gray-600 font-sans tracking-[0.2em] uppercase">
                Waiting for captures...
            </div>
        );
    }

    // Pre-filter/limit images (e.g., initial load handles up to 6 smoothly due to lazy loads)
    const displayPhotos = photos.slice(0, 10);

    return (
        <div className="w-full px-4 pb-32">
            <div className="space-y-6">
                {displayPhotos.map((photo, index) => {
                    const isRight = index % 2 === 0;
                    return (
                        <PhotoCard
                            key={photo.id}
                            photo={photo}
                            isRight={isRight}
                            onDelete={onDelete}
                            onPrint={onPrint}
                            onDownload={onDownload}
                        />
                    );
                })}
                {photos.length > 10 && (
                    <div className="text-center text-gray-600 text-xs font-mono tracking-widest mt-10">
                        LOAD MORE
                    </div>
                )}
            </div>
        </div>
    );
}
