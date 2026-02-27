import React, { useState, useEffect } from 'react';
import { supabase } from './lib/supabase';
import HeaderHero from './components/HeaderHero';
import CameraSection from './components/CameraSection';
import TimelineSection from './components/TimelineSection';
import QRModal from './components/QRModal';

const API_BASE = 'http://localhost:5000';

function App() {
  const [photos, setPhotos] = useState([]);
  const [activeMode, setActiveMode] = useState('SINGLE');
  const [activeFilter, setActiveFilter] = useState('STRANGER_THEME');
  const [qrUrl, setQrUrl] = useState(null);

  // Fetch initial gallery (no duplicate popup logic anymore on mount)
  useEffect(() => {
    const fetchPhotos = async () => {
      const { data, error } = await supabase
        .from('photos')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(600);

      if (!error && data) {
        setPhotos(data);
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
          setPhotos(prev => {
            // Check if it already exists to avoid dupes purely in state
            if (prev.find(p => p.id === newPhoto.id)) return prev;
            return [newPhoto, ...prev].slice(0, 600);
          });
        } else if (payload.eventType === 'DELETE') {
          setPhotos(prev => prev.filter(p => p.id !== payload.old.id));
        }
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

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
      console.log('Print job queued');
    } catch (err) {
      console.error("Print request failed", err);
    }
  };

  // UI trigger for Download -> opens QR modal
  const handleDownloadClick = (imageUrl) => {
    setQrUrl(imageUrl);
  };

  const handleDelete = async (id) => {
    const adminKey = localStorage.getItem('MAGIC_ADMIN_KEY');
    if (!adminKey) {
      alert("Unauthorized: Set MAGIC_ADMIN_KEY in local storage");
      return;
    }
    const { error } = await supabase.from('photos').delete().eq('id', id);
    if (error) {
      console.error("Delete failed", error);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans overflow-x-hidden selection:bg-stranger-red selection:text-white pb-10">

      {/* 1. Hero */}
      <HeaderHero />

      {/* 2 & 3. Camera View & Controls */}
      <CameraSection
        activeFilter={activeFilter}
        activeMode={activeMode}
        onFilterSelect={handleFilterSelect}
        onModeSelect={handleModeSelect}
      />

      {/* 4. Timeline */}
      <TimelineSection
        photos={photos}
        onDelete={handleDelete}
        onPrint={handlePrint}
        onDownload={handleDownloadClick}
      />

      {/* Manual Action QR Modal */}
      <QRModal
        photoUrl={qrUrl}
        onClose={() => setQrUrl(null)}
        onPrint={handlePrint}
      />
    </div>
  );
}

export default App;
