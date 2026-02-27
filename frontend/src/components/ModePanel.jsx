import React from 'react';

const modes = ['SINGLE', 'BURST', 'GIF'];

export default function ModePanel({ activeMode, onModeSelect }) {
    return (
        <div className="flex flex-col items-center w-full mb-10">
            <span className="text-gray-400 text-xs tracking-[0.3em] mb-3 uppercase">Mode</span>
            <div className="flex flex-wrap gap-4 justify-center">
                {modes.map((mode) => {
                    const isActive = activeMode === mode;
                    return (
                        <button
                            key={mode}
                            onClick={() => onModeSelect(mode)}
                            className={`
                px-6 py-2 rounded-lg text-sm font-sans tracking-[0.1em] transition-all duration-300
                ${isActive
                                    ? 'bg-transparent text-white border border-stranger-red box-glow-red scale-105 shadow-[0_0_15px_rgba(229,9,20,0.5)]'
                                    : 'bg-[#111] text-gray-500 border border-gray-800 hover:text-gray-300 hover:border-gray-600'}
              `}
                        >
                            {mode}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
