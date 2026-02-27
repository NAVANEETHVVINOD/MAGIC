import React from 'react';

const filters = [
    'NORMAL', 'GLITCH', 'NEON', 'DREAMY', 'RETRO', 'NOIR', 'BW', 'STRANGER_THEME'
];

export default function FilterPanel({ activeFilter, onFilterSelect }) {
    return (
        <div className="flex flex-col items-center w-full my-6">
            <h3 className="font-horror text-stranger-red tracking-widest text-lg md:text-2xl mb-4 opacity-80 text-glow-red">VISUAL FILTER</h3>
            <div className="flex flex-wrap gap-3 justify-center max-w-4xl px-4">
                {filters.map((filter) => {
                    const isActive = activeFilter === filter;
                    return (
                        <button
                            key={filter}
                            onClick={() => onFilterSelect(filter)}
                            className={`
                px-4 py-2 rounded text-sm md:text-base font-horror tracking-wider transition-all duration-300
                ${isActive
                                    ? 'bg-stranger-red/20 text-white border border-stranger-red box-glow-red scale-105'
                                    : 'bg-black/40 text-gray-500 border border-gray-800 hover:text-gray-300 hover:border-gray-600'}
              `}
                        >
                            {filter.replace('_', ' ')}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
