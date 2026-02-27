import React from 'react';

const filters = [
    'NORMAL', 'GLITCH', 'NEON', 'DREAMY', 'RETRO', 'NOIR', 'STRANGER'
];

export default function FilterPanel({ activeFilter, onFilterSelect }) {
    // Normalize STRANGER_THEME to STRANGER visually if needed
    return (
        <div className="flex flex-col items-center w-full mb-6">
            <span className="text-gray-400 text-xs tracking-[0.3em] mb-3 uppercase">Filter</span>
            <div className="flex flex-wrap gap-3 justify-center max-w-4xl px-4">
                {filters.map((filter) => {
                    const apiVariant = filter === 'STRANGER' ? 'STRANGER_THEME' : filter;
                    const isActive = activeFilter === apiVariant;

                    return (
                        <button
                            key={filter}
                            onClick={() => onFilterSelect(apiVariant)}
                            className={`
                px-5 py-2 rounded-lg text-sm font-sans tracking-[0.1em] transition-all duration-300
                ${isActive
                                    ? 'bg-transparent text-white border border-stranger-red box-glow-red scale-105 shadow-[0_0_15px_rgba(229,9,20,0.5)]'
                                    : 'bg-[#111] text-gray-500 border border-gray-800 hover:text-gray-300 hover:border-gray-600'}
              `}
                        >
                            {filter}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
