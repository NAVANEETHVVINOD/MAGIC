# Design Document: MAGIC 5.0 Frontend Interface

## Overview

The MAGIC 5.0 Frontend Interface is a React-based single-page application that provides a cinematic photo booth experience with Stranger Things-inspired aesthetics. The application features a non-functional camera display (instructional placeholder), interactive filter and mode controls, a real-time photo timeline with animated effects, and a QR code modal for photo downloads.

The design emphasizes visual consistency with pure black backgrounds, neon red accents, and smooth animations targeting 60fps performance. The interface uses Supabase for real-time photo updates and communicates with a Flask backend for filter/mode configuration.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Application                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    App Component                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ HeaderHero   │  │ CameraSection│  │ Timeline   │  │  │
│  │  │              │  │              │  │ Section    │  │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │  │
│  │                    ┌──────────────┐                   │  │
│  │                    │  QRModal     │                   │  │
│  │                    └──────────────┘                   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Supabase       │  │  Backend API    │  │  Browser APIs   │
│  Realtime       │  │  /set_filter    │  │  (localStorage) │
│  postgres_      │  │  /set_mode      │  │                 │
│  changes        │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Technology Stack

- **React 19.2.0**: UI framework with hooks for state management
- **Vite 7.3.1**: Build tool and development server
- **TailwindCSS 3.4.19**: Utility-first CSS framework for styling
- **Framer Motion 12.34.3**: Animation library for smooth transitions
- **Supabase JS Client 2.98.0**: Real-time database subscriptions
- **qrcode.react 4.2.0**: QR code generation for download links

### Component Hierarchy

```
App
├── HeaderHero
├── CameraSection
│   ├── CameraView
│   ├── FilterPanel
│   │   └── FilterButton (×7)
│   └── ModePanel
│       └── ModeButton (×3)
├── TimelineSection
│   ├── EnergyLine
│   └── GalleryTimeline
│       └── PhotoCard (×6 max)
│           └── ActionCard (conditional)
└── QRModal (conditional)
```

## Components and Interfaces

### 1. App Component

**Responsibility**: Root component managing global state and layout structure.

**State**:
```javascript
{
  activeFilter: string,        // Current filter: "NORMAL" | "GLITCH" | "NEON" | "DREAMY" | "RETRO" | "NOIR" | "STRANGER"
  activeMode: string,           // Current mode: "SINGLE" | "BURST" | "GIF"
  photos: Array<Photo>,         // Array of photo objects from Supabase
  selectedPhoto: Photo | null,  // Currently selected photo for QR modal
  isQRModalOpen: boolean,       // QR modal visibility state
  isBackendError: boolean       // Backend connection status
}
```

**Layout Structure**:
```jsx
<div className="min-h-screen flex flex-col overflow-hidden">
  <HeaderHero />           {/* auto height */}
  <CameraSection />        {/* flex-none */}
  <TimelineSection />      {/* flex-1 */}
  <QRModal />
</div>
```

**Lifecycle**:
- Initialize Supabase client on mount
- Subscribe to postgres_changes for new photos
- Fetch initial 6 photos from database
- Apply `overflow: hidden` to body element
- Start backend health check polling (every 5 seconds)

**Backend Health Check**:
```javascript
useEffect(() => {
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/health`);
      setIsBackendError(!res.ok);
    } catch {
      setIsBackendError(true);
    }
  }, 5000);
  
  return () => clearInterval(interval);
}, []);
```

**Memory Safety Note**: All intervals and subscriptions must be cleaned up on component unmount to prevent duplicate connections during hot reload or navigation.

**Props**: None (root component)

### 2. HeaderHero Component

**Responsibility**: Display MAGIC branding with Stranger Things aesthetic.

**Props**: None

**Styling**:
- Title: "MAGIC" with red neon glow (`drop-shadow(0 0 20px #E10600)`)
- Subtitle: "IEEE Hackathon 2026" in white
- Font: Large display font with letter-spacing
- Animation: Optional subtle flicker effect

### 3. CameraSection Component

**Responsibility**: Container for camera display and control panels.

**Props**: 
```javascript
{
  activeFilter: string,
  activeMode: string,
  onFilterChange: (filter: string) => void,
  onModeChange: (mode: string) => void
}
```

**Layout**: Vertical stack with camera view on top, controls below

### 4. CameraView Component

**Responsibility**: Display instructional placeholder (not actual camera).

**Props**: None

**Styling**:
- Height: 70vh
- Aspect ratio: 16:9 (using `aspect-[16/9]`)
- Border: Red neon glow (`shadow-[0_0_20px_#E10600]`)
- Background: Dark gradient with vignette overlay
- Content: "👍 SHOW THUMBS UP TO CAPTURE" with pulsing animation

**Animation**:
```javascript
// Framer Motion variants
const pulseVariants = {
  initial: { opacity: 0.6, scale: 1 },
  animate: { 
    opacity: [0.6, 1, 0.6],
    scale: [1, 1.05, 1],
    transition: { duration: 2, repeat: Infinity, ease: "easeInOut" }
  }
}
```

### 5. FilterPanel Component

**Responsibility**: Render filter selection buttons.

**Props**:
```javascript
{
  activeFilter: string,
  onFilterChange: (filter: string) => void
}
```

**Filters**: `["NORMAL", "GLITCH", "NEON", "DREAMY", "RETRO", "NOIR", "STRANGER"]`

**Behavior**:
- On click: POST to `${VITE_BACKEND_URL}/set_filter` with `{filter: filterName}`
- Update local state immediately (optimistic update)
- Handle errors gracefully (log to console, show error indicator)

### 6. ModePanel Component

**Responsibility**: Render capture mode selection buttons.

**Props**:
```javascript
{
  activeMode: string,
  onModeChange: (mode: string) => void
}
```

**Modes**: `["SINGLE", "BURST", "GIF"]`

**Behavior**:
- On click: POST to `${VITE_BACKEND_URL}/set_mode` with `{mode: modeName}`
- Update local state immediately (optimistic update)
- Handle errors gracefully

### 7. FilterButton / ModeButton Components

**Responsibility**: Reusable button component for filters and modes.

**Props**:
```javascript
{
  label: string,
  isActive: boolean,
  onClick: () => void
}
```

**Styling**:
- Default: Dark background (`bg-zinc-900`), white text, matte finish
- Active: Red border glow, red text (`text-[#E10600]`)
- Hover: Subtle red pulse animation (scale 1.02, glow intensity increase)

**Animation**:
```javascript
// Framer Motion
<motion.button
  whileHover={{ scale: 1.02, boxShadow: "0 0 15px #E10600" }}
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.2 }}
/>
```

### 8. TimelineSection Component

**Responsibility**: Container for energy line and photo gallery.

**Props**:
```javascript
{
  photos: Array<Photo>,
  onPhotoClick: (photo: Photo) => void
}
```

**Layout**: Relative positioning to allow absolute-positioned energy line overlay

### 9. EnergyLine Component

**Responsibility**: Animated vertical red line with particle effects.

**Props**: None

**Implementation**:
- SVG or Canvas-based animation
- Vertical line with animated particles moving upward
- Continuous loop animation
- Red glow effect (`filter: drop-shadow(0 0 10px #E10600)`)

**Animation Strategy**:
```javascript
// Using Framer Motion with SVG
const particleVariants = {
  animate: {
    y: [0, -100],
    opacity: [0, 1, 0],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: "linear",
      staggerChildren: 0.3
    }
  }
}
```

### 10. GalleryTimeline Component

**Responsibility**: Scrollable container for photo cards.

**Props**:
```javascript
{
  photos: Array<Photo>,
  onPhotoClick: (photo: Photo) => void
}
```

**Styling**:
- Height: 60vh
- Overflow: `overflow-y-auto`, `overflow-x-hidden`
- Custom scrollbar: Red thumb on dark track
- Grid layout: Single column with gap
- Fade mask: Apply `timeline-fade-mask` class for top boundary fade

**Implementation**:
```jsx
<div className="timeline-scroll timeline-fade-mask overflow-y-auto h-[60vh]">
  {/* Photo cards */}
</div>
```

**Scroll Behavior**:
- Internal scroll only (body has `overflow: hidden`)
- Smooth scrolling enabled
- Photos fade at top boundary using gradient mask

### 11. PhotoCard Component

**Responsibility**: Individual photo display with hover effects.

**Props**:
```javascript
{
  photo: Photo,
  onClick: (photo: Photo) => void
}
```

**State**:
```javascript
{
  isHovered: boolean,
  isLoading: boolean,
  hasError: boolean
}
```

**Styling**:
- Default: Grayscale filter (`filter: grayscale(100%)`)
- Hover: Full color (`filter: grayscale(0%)`), red border glow
- Transition: 300ms ease-in-out
- Aspect ratio: Maintain original photo proportions
- Border: Subtle red glow on hover

**Animation**:
```javascript
// Entrance animation when new photo arrives
const entranceVariants = {
  initial: { opacity: 0, y: -50 },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.4, ease: "easeOut" }
  }
}
```

**Error Handling**:
- If image fails to load, display fallback placeholder
- Placeholder: Dark rectangle with red border and error icon

### 12. ActionCard Component

**Responsibility**: Overlay showing Download/Print buttons on photo click.

**Props**:
```javascript
{
  photo: Photo,
  onDownload: (photo: Photo) => void,
  onPrint: (photo: Photo) => void,
  onClose: () => void
}
```

**Styling**:
- Absolute positioning over photo
- Semi-transparent dark background (`bg-black/80`)
- Red border glow
- Centered buttons with icons

**Behavior**:
- Download: Open QR modal with photo URL
- Print: Send POST request to backend /print endpoint with photo URL (no browser print dialog)
- Close: Click outside or ESC key

### 13. QRModal Component

**Responsibility**: Display QR code for mobile photo download.

**Props**:
```javascript
{
  photo: Photo,
  isOpen: boolean,
  onClose: () => void
}
```

**State**:
```javascript
{
  countdown: number  // 10-second countdown
}
```

**Styling**:
- Fixed positioning, centered viewport
- Backdrop: Blurred dark overlay (`backdrop-blur-md bg-black/70`)
- Modal: Red neon border, dark background
- QR code: Large size (256x256px)
- Countdown: Red text, prominent display

**Lifecycle**:
- On open: Start 10-second countdown
- On countdown zero: Auto-close modal
- On manual close: Clear countdown timer

**Timer Implementation with Cleanup**:
```javascript
useEffect(() => {
  if (!isOpen) return;
  
  setCountdown(10); // Reset countdown
  
  const timer = setInterval(() => {
    setCountdown(prev => {
      if (prev <= 1) {
        onClose();
        return 0;
      }
      return prev - 1;
    });
  }, 1000);
  
  return () => clearInterval(timer); // Cleanup on unmount or close
}, [isOpen, onClose]);
```

**Animation**:
```javascript
// Framer Motion
const modalVariants = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { 
    opacity: 1, 
    scale: 1,
    transition: { duration: 0.25, ease: "easeOut" }
  },
  exit: { 
    opacity: 0, 
    scale: 0.8,
    transition: { duration: 0.2 }
  }
}
```

## Data Models

### Photo Object

```typescript
interface Photo {
  id: string;        // UUID from Supabase
  filename: string;  // Original filename
  url: string;       // Public URL to photo in Supabase storage
  created_at: string; // ISO timestamp
}
```

**Note**: This schema matches the current backend implementation. The backend stores filter and mode settings globally, not per-photo.

### Supabase Table Schema

```sql
-- photos table (current backend schema)
CREATE TABLE photos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  filename TEXT NOT NULL,
  url TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for efficient querying
CREATE INDEX idx_photos_created_at ON photos(created_at DESC);
```

**Note**: Filter and mode settings are stored globally in the backend, not per-photo in the database.

### API Request/Response Models

**POST /set_filter**
```typescript
// Request
{
  filter: "NORMAL" | "GLITCH" | "NEON" | "DREAMY" | "RETRO" | "NOIR" | "STRANGER"
}

// Response
{
  success: boolean,
  message: string
}
```

**POST /set_mode**
```typescript
// Request
{
  mode: "SINGLE" | "BURST" | "GIF"
}

// Response
{
  success: boolean,
  message: string
}
```

### Environment Variables

```bash
# .env file
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_BACKEND_URL=http://localhost:5000
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Camera Display Aspect Ratio Invariance

*For any* viewport width, the Camera Display component should maintain a 16:9 aspect ratio.

**Validates: Requirements 2.2, 12.1**

### Property 2: No Browser Camera API Access

*For any* user session, the system should never request camera permissions or access the browser camera API.

**Validates: Requirements 2.7**

### Property 3: Control Button API Communication

*For any* filter or mode button click, the system should send a POST request to the appropriate endpoint (/set_filter or /set_mode) with the correct JSON payload containing the selected option name.

**Validates: Requirements 3.2, 4.2, 10.1, 10.2**

### Property 4: Active Control Button Highlighting

*For any* active filter or mode, the corresponding button should display red glow border and red text color (#E10600).

**Validates: Requirements 3.3, 4.3**

### Property 5: Control Button Hover Animation

*For any* filter or mode button, hovering should trigger a subtle red pulse animation effect.

**Validates: Requirements 3.4, 4.4**

### Property 6: Control Button Default Styling

*For any* inactive filter or mode button, the button should render with matte dark background and white text.

**Validates: Requirements 3.5, 4.5**

### Property 7: Photo Card Grayscale Default

*For any* photo in the timeline gallery, the photo should render with grayscale filter by default when not hovered.

**Validates: Requirements 5.3**

### Property 8: Photo Card Hover Color Transition

*For any* photo card, when hovered, the grayscale filter should transition to full color within 300ms using ease-in-out timing.

**Validates: Requirements 5.4, 16.2**

### Property 9: Timeline Photo Limit

*For any* state of the timeline gallery, the displayed photos should not exceed 6 items.

**Validates: Requirements 5.2, 5.5**

### Property 10: Timeline Scroll Isolation

*For any* scroll action within the timeline gallery, the main page body should remain fixed and not scroll.

**Validates: Requirements 5.7, 5.11**

### Property 11: QR Modal Trigger Exclusivity

*For any* user session, the QR modal should only appear when the user explicitly clicks the Download button on an Action Card, never automatically.

**Validates: Requirements 7.1, 7.9**

### Property 12: QR Modal Auto-Close Timer

*For any* opened QR modal, the modal should automatically close after exactly 10 seconds unless manually closed earlier.

**Validates: Requirements 7.5, 7.6**

### Property 13: Realtime Photo Subscription

*For any* new photo inserted into the Supabase photos table, the frontend should receive the update via postgres_changes subscription and prepend it to the timeline.

**Validates: Requirements 6.1, 6.2**

### Property 14: Color Palette Consistency

*For any* UI element in the system, only black (#000000), white (#FFFFFF), and Stranger Things red (#E10600 or #FF1E1E) colors should be used. No green colors should appear anywhere.

**Validates: Requirements 8.1, 8.2, 8.3, 8.4**

### Property 15: Animation Frame Rate Target

*For any* animation in the system, the target frame rate should be 60fps with animation durations between 200-400ms.

**Validates: Requirements 9.1, 9.4, 16.2**

### Property 16: Photo Data Model Alignment

*For any* photo object received from Supabase, it should contain the following fields: id (string), filename (string), url (string), created_at (string).

**Validates: Requirements 6.1, 14.1**

## Z-Index Layering Strategy

To prevent stacking context issues, the following z-index hierarchy is enforced:

```css
/* Base layout */
.base-layout { z-index: 0; }

/* Energy line background */
.energy-line { z-index: 10; }

/* Photo cards */
.photo-card { z-index: 20; }

/* Action card overlay */
.action-card { z-index: 30; }

/* QR modal backdrop */
.qr-modal-backdrop { z-index: 40; }

/* QR modal content */
.qr-modal-content { z-index: 50; }
```

## Supabase Integration

### Client Initialization

```javascript
// src/lib/supabase.js
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

### Realtime Subscription Setup

```javascript
// In App.jsx
useEffect(() => {
  const channel = supabase
    .channel('photos-channel')
    .on('postgres_changes', {
      event: 'INSERT',
      schema: 'public',
      table: 'photos'
    }, (payload) => {
      const newPhoto = payload.new;
      setPhotos(prev => {
        // Prevent duplicates
        if (prev.find(p => p.id === newPhoto.id)) return prev;
        // Prepend and limit to 6
        return [newPhoto, ...prev].slice(0, 6);
      });
    })
    .subscribe();

  // Cleanup on unmount - Supabase client handles auto-reconnection internally
  return () => {
    supabase.removeChannel(channel);
  };
}, []);
```

**Note**: Supabase JS client auto-reconnects internally on connection loss. The frontend does not need to manually poll or implement reconnection logic.

### Initial Photo Fetch

```javascript
// Fetch latest 6 photos on mount
useEffect(() => {
  const fetchPhotos = async () => {
    const { data, error } = await supabase
      .from('photos')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(6);

    if (!error && data) {
      setPhotos(data);
    }
  };
  fetchPhotos();
}, []);
```

## Backend API Integration

### Filter Selection

```javascript
const handleFilterChange = async (filter) => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/set_filter`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filter })
    });
    
    if (response.ok) {
      setActiveFilter(filter);
    } else {
      console.error('Filter change failed');
      setIsBackendError(true);
    }
  } catch (error) {
    console.error('Backend unreachable:', error);
    setIsBackendError(true);
  }
};
```

### Mode Selection

```javascript
const handleModeChange = async (mode) => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/set_mode`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode })
    });
    
    if (response.ok) {
      setActiveMode(mode);
    } else {
      console.error('Mode change failed');
      setIsBackendError(true);
    }
  } catch (error) {
    console.error('Backend unreachable:', error);
    setIsBackendError(true);
  }
};
```

### Print Trigger

```javascript
const handlePrint = async (photoUrl) => {
  try {
    await fetch(`${import.meta.env.VITE_BACKEND_URL}/print`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ imageUrl: photoUrl })
    });
    console.log('Print job queued');
  } catch (error) {
    console.error('Print request failed:', error);
  }
};
```

## Styling Implementation

### TailwindCSS Configuration

```javascript
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        'stranger-red': '#E10600',
        'stranger-red-bright': '#FF1E1E'
      },
      boxShadow: {
        'red-glow': '0 0 20px #E10600',
        'red-glow-strong': '0 0 30px #E10600'
      },
      dropShadow: {
        'red-neon': '0 0 20px #E10600'
      }
    }
  },
  plugins: []
};
```

### Global Styles

```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-black text-white overflow-hidden;
    font-family: 'Inter', system-ui, sans-serif;
  }
}

/* Custom scrollbar for timeline */
.timeline-scroll::-webkit-scrollbar {
  width: 8px;
}

.timeline-scroll::-webkit-scrollbar-track {
  background: #1a1a1a;
}

.timeline-scroll::-webkit-scrollbar-thumb {
  background: #E10600;
  border-radius: 4px;
}

.timeline-scroll::-webkit-scrollbar-thumb:hover {
  background: #FF1E1E;
}

/* Fade mask for timeline top boundary */
.timeline-fade-mask {
  mask-image: linear-gradient(
    to top,
    rgba(0,0,0,1) 80%,
    rgba(0,0,0,0)
  );
  -webkit-mask-image: linear-gradient(
    to top,
    rgba(0,0,0,1) 80%,
    rgba(0,0,0,0)
  );
}
```

## Performance Optimizations

### React.memo for Photo Cards

```javascript
// PhotoCard.jsx
import React, { memo } from 'react';

const PhotoCard = memo(({ photo, onClick }) => {
  // Component implementation
}, (prevProps, nextProps) => {
  // Only re-render if photo.id changes
  return prevProps.photo.id === nextProps.photo.id;
});

export default PhotoCard;
```

### Lazy Loading Images

```javascript
// PhotoCard.jsx
const [isLoaded, setIsLoaded] = useState(false);

<img
  src={photo.url}
  alt={photo.filename}
  loading="lazy"
  onLoad={() => setIsLoaded(true)}
  className={`transition-opacity duration-300 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
/>
```

### Debounced Scroll Handling

```javascript
import { useCallback } from 'react';
import { debounce } from 'lodash';

const handleScroll = useCallback(
  debounce((e) => {
    // Scroll logic
  }, 100),
  []
);
```

## Testing Strategy

### Unit Tests

- Component rendering tests for all major components
- State management tests for App component
- API integration mocking tests
- Animation behavior tests

### Property-Based Tests

Property-based tests will be implemented using `fast-check` library to validate the correctness properties defined above.

Example test structure:

```javascript
import fc from 'fast-check';

describe('Property 9: Timeline Photo Limit', () => {
  it('should never display more than 6 photos', () => {
    fc.assert(
      fc.property(
        fc.array(fc.record({ id: fc.uuid(), url: fc.webUrl() }), { minLength: 0, maxLength: 100 }),
        (photos) => {
          const { container } = render(<GalleryTimeline photos={photos} />);
          const displayedPhotos = container.querySelectorAll('.photo-card');
          return displayedPhotos.length <= 6;
        }
      )
    );
  });
});
```

## Deployment Considerations

### Build Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'supabase-vendor': ['@supabase/supabase-js']
        }
      }
    }
  },
  server: {
    port: 5173,
    host: true
  }
});
```

### Environment Variables

Production environment variables should be set in `.env.production`:

```bash
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-production-anon-key
VITE_BACKEND_URL=http://localhost:5000
```

## Security Considerations

1. **Supabase RLS Policies**: Ensure Row Level Security is enabled on the photos table
2. **CORS Configuration**: Backend should only allow requests from the frontend domain
3. **API Key Protection**: Never expose service_role key in frontend code
4. **Input Validation**: Validate all user inputs before sending to backend
5. **XSS Prevention**: React's JSX automatically escapes content, but be cautious with dangerouslySetInnerHTML

## Accessibility Considerations

1. **Keyboard Navigation**: All interactive elements should be keyboard accessible
2. **ARIA Labels**: Add appropriate aria-labels to buttons and interactive elements
3. **Focus Indicators**: Ensure visible focus indicators for keyboard navigation
4. **Alt Text**: All images should have descriptive alt text
5. **Color Contrast**: Ensure sufficient contrast between text and background

## Browser Compatibility

Target browsers:
- Chrome 90+
- Edge 90+
- Firefox 88+
- Safari 14+

Required polyfills: None (modern browsers only)

## Failure Mode Handling

The system is designed to gracefully handle various failure scenarios without crashing or appearing broken.

### Failure Mode: Supabase Offline

**Symptoms**:
- No new photos appear in timeline
- Realtime subscription disconnected

**System Behavior**:
- Timeline freezes at current state
- Existing photos remain visible and interactive
- No crash occurs
- Backend controls (filter/mode) remain operational
- Supabase client auto-reconnects internally (no manual polling needed)

**User Experience**:
- Subtle red indicator appears (optional)
- System continues to function with cached data
- Photos captured during downtime appear when connection restored

### Failure Mode: Backend API Unreachable

**Symptoms**:
- Filter/mode changes fail to sync
- Print requests fail

**System Behavior**:
- `isBackendError` state set to true
- Health check polling continues (5-second interval)
- UI remains responsive
- Local state updates optimistically

**User Experience**:
- Subtle red warning indicator in corner
- Filter/mode buttons still clickable (local state updates)
- System auto-recovers when backend returns

### Failure Mode: Image Loading Failure

**Symptoms**:
- Photo URL returns 404 or network error

**System Behavior**:
- PhotoCard displays fallback placeholder
- Dark rectangle with red border
- Error icon or "Image unavailable" text
- No crash or blank space

**User Experience**:
- Clear visual indication of missing image
- Timeline layout remains stable
- Other photos load normally

### Failure Mode: QR Code Generation Failure

**Symptoms**:
- Invalid photo URL
- QR library error

**System Behavior**:
- Modal displays error message
- "Unable to generate QR code" text
- Download button still available (direct link)
- Modal can be closed normally

**User Experience**:
- Clear error message
- Alternative download method provided
- No system crash

## Event Mode Behavior

When the backend runs with `--event-mode` flag, the frontend should align with production event constraints:

### Event Mode Characteristics

**Filter and Mode Locking**:
- Filter list remains unlocked (user can change)
- Mode list remains unlocked (user can change)
- Changes sync to backend immediately
- No admin-only restrictions on frontend

**Debug and Logging**:
- Console logs disabled in production build
- Error logging only in development mode
- No verbose output to browser console

**Auto-Retry Behavior**:
- Supabase subscription auto-reconnects on disconnect
- Backend health check polls every 5 seconds
- Failed uploads handled by backend retry queue (not frontend concern)

**Performance Constraints**:
- 6-photo limit strictly enforced
- Lazy loading enabled for all images
- 60fps animation target maintained
- Memory usage kept minimal

**Kiosk Mode Optimizations**:
- Body scroll disabled (`overflow: hidden`)
- No right-click context menu (optional)
- No text selection outside QR modal
- Fullscreen-friendly layout

### Event Mode Testing Checklist

Before event deployment, verify:
- [ ] Backend health check recovers from temporary outage
- [ ] Supabase subscription reconnects after network blip
- [ ] Timeline never exceeds 6 photos
- [ ] QR modal never appears automatically
- [ ] Print jobs queue correctly
- [ ] System runs stable for 8+ hours continuous operation
- [ ] Memory usage remains constant (no leaks)
- [ ] Animations maintain 60fps under load

## Conclusion

This design document provides a comprehensive blueprint for implementing the MAGIC 5.0 Frontend Interface. The architecture emphasizes performance, visual consistency, and real-time interactivity while maintaining a cinematic Stranger Things-inspired aesthetic. All components are designed to work together seamlessly, with clear separation of concerns and well-defined interfaces.