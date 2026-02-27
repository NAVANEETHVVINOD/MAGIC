import React from 'react';
import CameraView from './CameraView';
import FilterPanel from './FilterPanel';
import ModePanel from './ModePanel';

export default function CameraSection({ activeFilter, activeMode, onFilterSelect, onModeSelect }) {
    return (
        <section className="relative w-full flex flex-col items-center bg-black/95">
            <div className="container mx-auto px-4 max-w-7xl">
                <CameraView />
                <FilterPanel
                    activeFilter={activeFilter}
                    onFilterSelect={onFilterSelect}
                />
                <ModePanel
                    activeMode={activeMode}
                    onModeSelect={onModeSelect}
                />
            </div>

            {/* Bottom fade into Timeline */}
            <div className="absolute bottom-0 w-full h-32 bg-gradient-to-t from-black to-transparent pointer-events-none" />
        </section>
    );
}
