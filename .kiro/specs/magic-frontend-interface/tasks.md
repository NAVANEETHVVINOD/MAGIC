# Implementation Tasks: MAGIC 5.0 Frontend Interface

## Overview
This task list implements the exact design from the reference screenshot (web design.png) with Stranger Things-inspired aesthetics, featuring a large camera display, filter/mode controls, and a cinematic photo timeline.

## Task List

### Phase 1: Foundation and Configuration

- [ ] 1. Update Data Model Alignment
  - [ ] 1.1 Update Photo interface to match backend schema (id, filename, url, created_at)
  - [ ] 1.2 Remove unused fields (image_url, filter_applied, mode_used, thumbnail_url) from frontend
  - [ ] 1.3 Update all components to use correct field names (url instead of image_url)

- [ ] 2. Fix Supabase Integration
  - [ ] 2.1 Update initial photo fetch to limit 6 photos (currently fetching 600)
  - [ ] 2.2 Add subscription cleanup in useEffect return
  - [ ] 2.3 Ensure realtime subscription only prepends to max 6 photos
  - [ ] 2.4 Add duplicate prevention logic in subscription handler
  - [ ] 2.5 Note: Supabase client auto-reconnects internally (no manual polling needed)

- [ ] 3. Configure TailwindCSS Theme
  - [ ] 3.1 Add Stranger Things red colors to tailwind.config.js (stranger-red: #E10600, stranger-red-bright: #FF1E1E)
  - [ ] 3.2 Add custom box-shadow utilities (red-glow, red-glow-strong)
  - [ ] 3.3 Add custom drop-shadow utilities (red-neon)
  - [ ] 3.4 Configure custom scrollbar styles for timeline

- [ ] 4. Setup Global Styles and Layout
  - [ ] 4.1 Add overflow-hidden to body element in index.css
  - [ ] 4.2 Add custom scrollbar styles for .timeline-scroll class
  - [ ] 4.3 Add timeline fade mask CSS (.timeline-fade-mask)
  - [ ] 4.4 Configure font family (Inter or system-ui)
  - [ ] 4.5 Create root layout container with flex-col and overflow-hidden
  - [ ] 4.6 Set HeaderHero to auto height, CameraSection to flex-none, TimelineSection to flex-1

- [ ] 5. Implement Backend Health Check
  - [ ] 5.1 Add backend health check polling (every 5 seconds)
  - [ ] 5.2 Update isBackendError state based on health check
  - [ ] 5.3 Add cleanup for health check interval on unmount
  - [ ] 5.4 Display subtle red warning indicator when backend is unreachable
  - [ ] 5.5 Auto-recover when backend returns online

### Phase 2: Header and Branding

- [ ] 6. Implement HeaderHero Component
  - [ ] 6.1 Create large "MAGIC" title with red neon glow effect
  - [ ] 6.2 Add "IEEE Hackathon 2026" subtitle
  - [ ] 6.3 Apply Stranger Things-style text styling with letter-spacing
  - [ ] 6.4 Add optional subtle flicker animation to title
  - [ ] 6.5 Ensure proper spacing and centering

### Phase 3: Camera Section (Exact Design Match)

- [ ] 7. Redesign CameraView Component
  - [ ] 7. Redesign CameraView Component
  - [ ] 7.1 Set height to 70vh with 16:9 aspect ratio
  - [ ] 7.2 Add red neon border with glow effect (shadow-[0_0_20px_#E10600])
  - [ ] 7.3 Apply dark gradient background with vignette overlay
  - [ ] 7.4 Center "👍 SHOW THUMBS UP TO CAPTURE" text
  - [ ] 7.5 Implement pulsing animation for instructional text (Framer Motion)
  - [ ] 7.6 Remove any browser camera access code

- [ ] 8. Redesign FilterPanel Component
  - [ ] 8.1 Arrange 7 filter buttons horizontally: NORMAL, GLITCH, NEON, DREAMY, RETRO, NOIR, STRANGER
  - [ ] 8.2 Style buttons with matte dark background (bg-zinc-900) and white text
  - [ ] 8.3 Implement active state with red border glow and red text
  - [ ] 8.4 Add hover animation with scale and glow intensity increase
  - [ ] 8.5 Ensure proper spacing between buttons
  - [ ] 8.6 Fix API integration to send correct filter names

- [ ] 9. Redesign ModePanel Component
  - [ ] 9.1 Arrange 3 mode buttons horizontally: SINGLE, BURST, GIF
  - [ ] 9.2 Style buttons with matte dark background and white text
  - [ ] 9.3 Implement active state with red border glow and red text
  - [ ] 9.4 Add hover animation with scale and glow intensity increase
  - [ ] 9.5 Ensure proper spacing between buttons
  - [ ] 9.6 Fix API integration to send correct mode names

- [ ] 10. Create Reusable Button Component
  - [ ] 10.1 Create FilterButton/ModeButton component with props (label, isActive, onClick)
  - [ ] 10.2 Implement Framer Motion hover effects (whileHover, whileTap)
  - [ ] 10.3 Add transition duration of 200ms
  - [ ] 10.4 Ensure consistent styling across all buttons

### Phase 4: Timeline Section (Critical - Exact Design Match)

- [ ] 11. Redesign TimelineSection Layout
  - [ ] 11.1 Set container height to 60vh
  - [ ] 11.2 Implement relative positioning for energy line overlay
  - [ ] 11.3 Remove page scroll (body overflow-hidden)
  - [ ] 11.4 Create controlled internal scroll container
  - [ ] 11.5 Add fade mask at top boundary

- [ ] 12. Implement EnergyLine Component
  - [ ] 12.1 Create vertical red line with SVG or Canvas
  - [ ] 12.2 Add animated particles moving upward
  - [ ] 12.3 Implement continuous loop animation
  - [ ] 12.4 Apply red glow effect (drop-shadow)
  - [ ] 12.5 Position absolutely in center of timeline
  - [ ] 12.6 Set z-index to 10

- [ ] 13. Redesign GalleryTimeline Component
  - [ ] 13.1 Limit display to maximum 6 photos
  - [ ] 13.2 Implement overflow-y-auto with custom scrollbar
  - [ ] 13.3 Apply timeline-fade-mask class for top boundary fade
  - [ ] 13.4 Remove "LOAD MORE" text (not in design)
  - [ ] 13.5 Implement single column grid layout with proper gap
  - [ ] 13.6 Add smooth scrolling behavior
  - [ ] 13.7 Use className="timeline-scroll timeline-fade-mask overflow-y-auto h-[60vh]"

- [ ] 14. Redesign PhotoCard Component
  - [ ] 14.1 Apply grayscale filter by default (filter: grayscale(100%))
  - [ ] 14.2 Implement hover transition to full color (300ms ease-in-out)
  - [ ] 14.3 Add red border glow on hover
  - [ ] 14.4 Implement entrance animation with Framer Motion (opacity 0→1, y: -50→0)
  - [ ] 14.5 Add lazy loading for images
  - [ ] 14.6 Implement error handling with fallback placeholder
  - [ ] 14.7 Add React.memo optimization
  - [ ] 14.8 Set z-index to 20

- [ ] 15. Create ActionCard Component
  - [ ] 15.1 Create overlay component with Download and Print buttons
  - [ ] 15.2 Position absolutely over photo when clicked
  - [ ] 15.3 Apply semi-transparent dark background (bg-black/80)
  - [ ] 15.4 Add red border glow
  - [ ] 15.5 Center buttons with proper spacing
  - [ ] 15.6 Implement close on click outside or ESC key
  - [ ] 15.7 Set z-index to 30
  - [ ] 15.8 Add fade-in animation
  - [ ] 15.9 Ensure Print button calls backend /print endpoint (NOT browser print dialog)

### Phase 5: QR Modal (Exact Design Match)

- [ ] 16. Redesign QRModal Component
  - [ ] 16.1 Implement fixed positioning with centered viewport
  - [ ] 16.2 Add blurred backdrop overlay (backdrop-blur-md bg-black/70)
  - [ ] 16.3 Style modal with red neon border and dark background
  - [ ] 16.4 Display large QR code (256x256px)
  - [ ] 16.5 Add "Scan To Download" text above QR code
  - [ ] 16.6 Implement 10-second countdown timer with proper cleanup
  - [ ] 16.7 Add auto-close functionality when countdown reaches zero
  - [ ] 16.8 Implement manual close button
  - [ ] 16.9 Add Framer Motion entrance/exit animations (scale 0.8→1)
  - [ ] 16.10 Set z-index to 40 (backdrop) and 50 (content)
  - [ ] 16.11 Ensure modal only opens on Download button click (never automatically)
  - [ ] 16.12 Add interval cleanup to prevent multiple timers on rapid open/close

- [ ] 17. Fix QR Modal Trigger Logic
  - [ ] 17.1 Remove any automatic QR popup logic from App.jsx
  - [ ] 17.2 Ensure QR modal only opens when user clicks Download on ActionCard
  - [ ] 17.3 Pass correct photo URL to QR modal
  - [ ] 17.4 Implement proper state management for modal visibility

### Phase 6: Print Integration

- [ ] 18. Implement Print Functionality
  - [ ] 18.1 Update Print button to call backend /print endpoint (not browser print)
  - [ ] 18.2 Send correct imageUrl in POST request body
  - [ ] 18.3 Add error handling for print requests
  - [ ] 18.4 Show success/error feedback to user
  - [ ] 18.5 Ensure print works from both ActionCard and QRModal

### Phase 7: Animations and Polish

- [ ] 19. Implement Framer Motion Animations
  - [ ] 19.1 Add camera view pulse animation (2s infinite loop)
  - [ ] 19.2 Add button hover animations (scale 1.02, glow increase)
  - [ ] 19.3 Add photo entrance animations (opacity, y-position)
  - [ ] 19.4 Add QR modal scale animation (0.8→1 in 250ms)
  - [ ] 19.5 Add energy line particle animations
  - [ ] 19.6 Ensure all animations target 60fps

- [ ] 20. Implement Glow Hierarchy
  - [ ] 20.1 Apply strongest glow to MAGIC title
  - [ ] 20.2 Apply medium glow to camera border
  - [ ] 20.3 Apply light glow to active buttons
  - [ ] 20.4 Apply subtle glow to timeline energy line
  - [ ] 20.5 Ensure consistent glow intensity across components

- [ ] 21. Color Palette Enforcement
  - [ ] 21.1 Audit all components for color usage
  - [ ] 21.2 Replace any non-black/white/red colors
  - [ ] 21.3 Remove all green colors from codebase
  - [ ] 21.4 Ensure consistent red shade usage (#E10600 or #FF1E1E)

### Phase 8: Performance Optimization

- [ ] 22. Implement Performance Optimizations
  - [ ] 22.1 Add React.memo to PhotoCard component
  - [ ] 22.2 Implement lazy loading for all images
  - [ ] 22.3 Add debounced scroll handling
  - [ ] 22.4 Optimize re-render logic in App component
  - [ ] 22.5 Ensure 60fps performance during animations

- [ ] 23. Memory Management
  - [ ] 23.1 Ensure photo array never exceeds 6 items in state
  - [ ] 23.2 Clean up Supabase subscription on unmount
  - [ ] 23.3 Clear countdown timers on modal close
  - [ ] 23.4 Remove unused event listeners
  - [ ] 23.5 Clean up health check interval on unmount
  - [ ] 23.6 Verify all intervals and subscriptions are cleaned up to prevent duplicate connections during hot reload

### Phase 9: Error Handling and Resilience

- [ ] 24. Implement Error Handling
  - [ ] 24.1 Add backend connection error indicator
  - [ ] 24.2 Handle API request failures gracefully
  - [ ] 24.3 Implement Supabase subscription retry logic
  - [ ] 24.4 Add image loading error fallbacks
  - [ ] 24.5 Log errors to console in development mode only

- [ ] 25. Add User Feedback
  - [ ] 25.1 Show subtle loading states for API requests
  - [ ] 25.2 Add success feedback for print jobs
  - [ ] 25.3 Display error messages for failed operations
  - [ ] 25.4 Ensure feedback doesn't break immersive aesthetic

### Phase 10: Testing and Validation

- [ ] 26. Manual Testing Checklist
  - [ ] 26.1 Test camera display aspect ratio on different screen sizes
  - [ ] 26.2 Test filter selection and backend sync
  - [ ] 26.3 Test mode selection and backend sync
  - [ ] 26.4 Test photo timeline scroll behavior
  - [ ] 26.5 Test photo hover effects
  - [ ] 26.6 Test ActionCard appearance on photo click
  - [ ] 26.7 Test QR modal trigger (only on Download click)
  - [ ] 26.8 Test QR modal auto-close after 10 seconds
  - [ ] 26.9 Test print functionality
  - [ ] 26.10 Test realtime photo updates
  - [ ] 26.11 Test backend health check recovery
  - [ ] 26.12 Test Supabase reconnection after network blip

- [ ] 27. Property-Based Testing
  - [ ] 27.1 Write property test for timeline photo limit (max 6)
  - [ ] 27.2 Write property test for color palette consistency
  - [ ] 27.3 Write property test for QR modal trigger exclusivity
  - [ ] 27.4 Write property test for scroll isolation
  - [ ] 27.5 Write property test for animation frame rate

- [ ] 28. Cross-Browser Testing
  - [ ] 28.1 Test on Chrome 90+
  - [ ] 28.2 Test on Edge 90+
  - [ ] 28.3 Test on Firefox 88+
  - [ ] 28.4 Test on Safari 14+

- [ ] 29. Event Mode Testing
  - [ ] 29.1 Test 8+ hours continuous operation
  - [ ] 29.2 Test memory usage remains constant (no leaks)
  - [ ] 29.3 Test system recovery from backend temporary outage
  - [ ] 29.4 Test system recovery from Supabase temporary outage
  - [ ] 29.5 Test timeline never exceeds 6 photos under load

### Phase 11: Final Polish and Deployment

- [ ] 30. Final Visual Audit
  - [ ] 30.1 Compare implementation to web design.png screenshot
  - [ ] 30.2 Verify all spacing matches design
  - [ ] 30.3 Verify all colors match design
  - [ ] 30.4 Verify all animations match design
  - [ ] 30.5 Verify glow effects match design

- [ ] 31. Accessibility Improvements
  - [ ] 31.1 Add keyboard navigation support
  - [ ] 31.2 Add ARIA labels to interactive elements
  - [ ] 31.3 Ensure visible focus indicators
  - [ ] 31.4 Add alt text to all images
  - [ ] 31.5 Verify color contrast ratios

- [ ] 32. Production Build Configuration
  - [ ] 32.1 Configure vite.config.js for production
  - [ ] 32.2 Set up environment variables for production
  - [ ] 32.3 Test production build locally
  - [ ] 32.4 Optimize bundle size
  - [ ] 32.5 Verify sourcemaps are disabled in production

## Priority Order

**Critical Path (Must Complete First):**
1. Tasks 1-5: Foundation, Configuration, and Health Check
2. Tasks 6-10: Header and Camera Section Redesign
3. Tasks 11-15: Timeline Section Redesign
4. Tasks 16-17: QR Modal Redesign

**High Priority:**
5. Tasks 18-21: Print Integration and Animations
6. Tasks 22-23: Performance Optimization and Memory Management

**Medium Priority:**
7. Tasks 24-25: Error Handling and User Feedback
8. Tasks 26-29: Testing (Manual, Property-Based, Cross-Browser, Event Mode)

**Final Polish:**
9. Tasks 30-32: Visual Audit, Accessibility, and Deployment

## Notes

- All tasks should reference the web design.png screenshot for exact visual specifications
- Maintain Stranger Things aesthetic throughout (black background, red neon accents)
- Target 60fps for all animations
- Ensure mobile responsiveness is not a priority (event installation on 1920x1080 display)
- Test frequently against the backend to ensure API integration works correctly
- Pay special attention to cleanup logic (timers, subscriptions, intervals) to prevent memory leaks
- Backend health check is critical for event mode reliability
- Timeline must never exceed 6 photos under any circumstances
