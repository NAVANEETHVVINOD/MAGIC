import React, { useState, useEffect } from 'react';
import { supabase } from './lib/supabase';
import HeaderHero from './components/HeaderHero';
import CameraView from './components/CameraView';
import ModePanel from './components/ModePanel';
import FilterPanel from './components/FilterPanel';
import GalleryTimeline from './components/GalleryTimeline';
import QRPopup from './components/QRPopup';

const API_BASE = 'http://localhost:5000';

function App() {
  const [photos, setPhotos] = useState([]);
  const [activeMode, setActiveMode] = useState('SINGLE');
  const [activeFilter, setActiveFilter] = useState('STRANGER_THEME');
  const [qrUrl, setQrUrl] = useState(null);
  const [lastSeenId, setLastSeenId] = useState(null);

  // Fetch initial gallery
  useEffect(() => {
    const fetchPhotos = async () => {
      const { data, error } = await supabase
        .from('photos')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(600);

      if (!error && data) {
        setPhotos(data);
        if (data.length > 0) {
          setLastSeenId(data[0].id);
        }
      }
    };
    fetchPhotos();
  }, []);

  // Realtime subscription
  useEffect(() => {
    const channel = supabase
      .channel('public:photos')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'photos' }, (payload) => {
        if (payload.eventType === 'INSERT') {
          const newPhoto = payload.new;
          setPhotos(prev => [newPhoto, ...prev].slice(0, 600));

          if (newPhoto.id !== lastSeenId) {
            setQrUrl(newPhoto.url);
            setLastSeenId(newPhoto.id);
          }
        } else if (payload.eventType === 'DELETE') {
          setPhotos(prev => prev.filter(p => p.id !== payload.old.id));
        }
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [lastSeenId]);

  // Sync mode with backend
  const handleModeSelect = async (mode) => {
    try {
      const res = await fetch(`${API_BASE}/set_mode`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode })
      });
      if (res.ok) {
        setActiveMode(mode);
      }
    } catch (err) {
      console.error("Failed to set mode", err);
    }
  };

  // Sync filter with backend
  const handleFilterSelect = async (filter) => {
    try {
      const res = await fetch(`${API_BASE}/set_filter`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filter })
      });
      if (res.ok) {
        setActiveFilter(filter);
      }
    } catch (err) {
      console.error("Failed to set filter", err);
    }
  };

  // Remote Print via Flask
  const handlePrint = async (imageUrl) => {
    try {
      await fetch(`${API_BASE}/print`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ imageUrl })
      });
      alert('Print job queued');
    } catch (err) {
      console.error("Print request failed", err);
    }
  };

  const handleDelete = async (id) => {
    const adminKey = localStorage.getItem('MAGIC_ADMIN_KEY');
    if (!adminKey) {
      alert("Unauthorized: Set MAGIC_ADMIN_KEY in local storage");
      return;
    }

    // In a real app we'd verify the key on backend RLS. For now, directly delete using SDK.
    const { error } = await supabase.from('photos').delete().eq('id', id);
    if (error) {
      console.error("Delete failed", error);
    }
  };

  return (
    <div className="min-h-screen pb-20">
      <HeaderHero />

      <div className="container mx-auto px-4">
        <CameraView />
        <ModePanel activeMode={activeMode} onModeSelect={handleModeSelect} />
        <FilterPanel activeFilter={activeFilter} onFilterSelect={handleFilterSelect} />

        <div className="mt-20 border-t border-stranger-red/30 pt-10">
          <h2 className="text-center font-horror text-3xl md:text-5xl text-stranger-red text-glow-red tracking-widest mb-10">
            THE ARCHIVES
          </h2>
          <GalleryTimeline
            photos={photos}
            onDelete={handleDelete}
            onPrint={handlePrint}
          />
        </div>
      </div>

      <QRPopup
        photoUrl={qrUrl}
        onClose={() => setQrUrl(null)}
      />
    </div>
  );
}

export default App;
