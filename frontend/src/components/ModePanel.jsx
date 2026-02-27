import React from 'react';

const modes = ['SINGLE', 'BURST', 'GIF'];

export default function ModePanel({ activeMode, onModeSelect }) {
    return (
        <div className="flex flex-col items-center w-full my-6">
            <h3 className="font-horror text-stranger-red tracking-widest text-lg md:text-2xl mb-4 opacity-80 text-glow-red">CAPTURE MODE</h3>
            <div className="flex flex-wrap gap-4 justify-center">
                {modes.map((mode) => (
                    <button
                        key={mode}
                        onClick={() => onModeSelect(mode)}
                        className={`
              px-6 py-2 rounded font-horror tracking-wider md:text-xl transition-all duration-300
              ${activeMode === mode
                                ? 'bg-green-900/40 text-green-400 border border-green-500 box-glow-green scale-105'
                                : 'bg-black/40 text-gray-400 border border-gray-800 hover:border-gray-500 hover:text-white'}
            `}
                    >
                        {mode}
                    </button>
                ))}
            </div>
        </div>
    );
}
