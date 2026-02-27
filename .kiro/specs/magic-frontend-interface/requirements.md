# Requirements Document: MAGIC 5.0 Frontend Interface

## Introduction

The MAGIC 5.0 Frontend Interface is a cinematic photo booth web application with a Stranger Things-inspired aesthetic. The system provides a real-time photo capture interface with visual filters, capture modes, and an interactive timeline gallery. The interface features neon red accents on a pure black background, creating an immersive retro-futuristic experience for IEEE Hackathon 2026.

## Glossary

- **System**: The MAGIC 5.0 Frontend Interface web application
- **Camera_Display**: The visual component showing camera instructions (not actual browser camera)
- **Filter_Panel**: The horizontal control panel containing 7 filter options
- **Mode_Panel**: The horizontal control panel containing 3 capture mode options
- **Timeline_Gallery**: The scrollable vertical photo gallery with energy line visualization
- **Photo_Card**: Individual photo component in the timeline gallery
- **QR_Modal**: The popup dialog displaying QR code for photo download
- **Energy_Line**: The animated red vertical line with particle effects in the timeline
- **Backend_API**: The Flask backend service handling filter/mode settings
- **Supabase_Client**: The real-time database client for photo updates
- **Action_Card**: The overlay showing Download/Print buttons on photo click

## Requirements

### Requirement 1: Header and Branding

**User Story:** As a user, I want to see the MAGIC branding with IEEE Hackathon 2026 information, so that I understand the application context and event association.

#### Acceptance Criteria

1. THE System SHALL display "MAGIC" as the primary title with Stranger Things-style red neon glow effect
2. THE System SHALL display "IEEE Hackathon 2026" as a subtitle below the main title
3. THE System SHALL render the header text in white color on pure black background (#000000)
4. THE System SHALL apply a red glow filter effect to the title text using CSS drop-shadow

### Requirement 2: Camera Display Section

**User Story:** As a user, I want to see a large camera display area with instructions, so that I know how to trigger photo capture.

#### Acceptance Criteria

1. THE Camera_Display SHALL occupy 70vh of viewport height
2. THE Camera_Display SHALL maintain a 16:9 aspect ratio
3. THE Camera_Display SHALL display "👍 SHOW THUMBS UP TO CAPTURE" as instructional text
4. THE Camera_Display SHALL render a red neon border with subtle glow effect
5. THE Camera_Display SHALL apply a vignette overlay effect for cinematic appearance
6. THE Camera_Display SHALL animate the instructional text with a pulsing effect
7. THE Camera_Display SHALL NOT access the browser camera API

### Requirement 3: Filter Control Panel

**User Story:** As a user, I want to select different visual filters, so that I can customize the appearance of captured photos.

#### Acceptance Criteria

1. THE Filter_Panel SHALL display 7 filter options: NORMAL, GLITCH, NEON, DREAMY, RETRO, NOIR, STRANGER
2. WHEN a filter button is clicked, THE System SHALL send a POST request to /set_filter endpoint with the selected filter name
3. WHEN a filter is active, THE System SHALL highlight that button with red glow border and red text color
4. WHEN a user hovers over a filter button, THE System SHALL apply a subtle red pulse animation
5. THE Filter_Panel SHALL render buttons with matte dark background and white text by default
6. THE Filter_Panel SHALL arrange buttons horizontally in a single row

### Requirement 4: Mode Control Panel

**User Story:** As a user, I want to select different capture modes, so that I can control how photos are taken.

#### Acceptance Criteria

1. THE Mode_Panel SHALL display 3 mode options: SINGLE, BURST, GIF
2. WHEN a mode button is clicked, THE System SHALL send a POST request to /set_mode endpoint with the selected mode name
3. WHEN a mode is active, THE System SHALL highlight that button with red glow border and red text color
4. WHEN a user hovers over a mode button, THE System SHALL apply a subtle red pulse animation
5. THE Mode_Panel SHALL render buttons with matte dark background and white text by default
6. THE Mode_Panel SHALL arrange buttons horizontally in a single row

### Requirement 5: Timeline Gallery Display

**User Story:** As a user, I want to view captured photos in a scrollable timeline, so that I can browse through all captured images.

#### Acceptance Criteria

1. THE Timeline_Gallery SHALL display photos in a vertical scrolling container occupying 60vh of viewport height
2. THE Timeline_Gallery SHALL load a maximum of 6 photos initially
3. THE Timeline_Gallery SHALL render photos in grayscale by default
4. WHEN a user hovers over a Photo_Card, THE System SHALL transition the photo from grayscale to full color
5. THE Timeline_Gallery SHALL display an animated red vertical Energy_Line with particle effects
6. THE Timeline_Gallery SHALL use a controlled internal scroll container
7. THE main page SHALL remain fixed and not scroll
8. WHEN a user scrolls inside Timeline_Gallery, images SHALL move upward and fade into top boundary
9. WHEN new images arrive, THE System SHALL enter them from the top with downward slide animation
10. WHEN a user clicks a Photo_Card, THE System SHALL display an Action_Card overlay with Download and Print buttons
11. THE System SHALL disable body scroll using overflow: hidden on the root layout container

### Requirement 6: Real-time Photo Updates

**User Story:** As a user, I want to see new photos appear automatically in the timeline, so that I can view captures in real-time without refreshing.

#### Acceptance Criteria

1. WHEN a new photo is added to the database, THE System SHALL receive the update via Supabase postgres_changes subscription
2. WHEN a new photo is received, THE System SHALL prepend it to the Timeline_Gallery
3. WHEN a new photo appears, THE System SHALL animate its entrance with smooth transition effects
4. THE System SHALL maintain the 6-photo display limit in the Timeline_Gallery
5. WHEN the timeline exceeds 6 photos, THE System SHALL remove the oldest photo from view

### Requirement 7: QR Code Modal

**User Story:** As a user, I want to scan a QR code to download photos to my mobile device, so that I can easily save and share captured images.

#### Acceptance Criteria

1. WHEN a user clicks the Download button on an Action_Card, THE System SHALL display the QR_Modal
2. THE QR_Modal SHALL display a large QR code containing the photo download URL
3. THE QR_Modal SHALL display "Scan To Download" text above the QR code
4. THE QR_Modal SHALL render Download and Print action buttons
5. THE QR_Modal SHALL display a 10-second countdown timer for auto-close
6. WHEN the countdown reaches zero, THE System SHALL automatically close the QR_Modal
7. THE QR_Modal SHALL render with a centered position and blurred backdrop
8. THE QR_Modal SHALL render with a red neon border effect
9. THE QR_Modal SHALL NOT appear automatically without user interaction

### Requirement 8: Visual Theme and Styling

**User Story:** As a user, I want to experience a cohesive Stranger Things-inspired aesthetic, so that the interface feels immersive and thematic.

#### Acceptance Criteria

1. THE System SHALL use pure black (#000000) as the primary background color
2. THE System SHALL use Stranger Things neon red (#E10600 or #FF1E1E) for all accent colors and glows
3. THE System SHALL use white color for all text elements
4. THE System SHALL NOT use green colors anywhere in the interface
5. THE System SHALL apply cinematic vignette effects to appropriate sections
6. THE System SHALL use red glow effects (CSS drop-shadow) for interactive elements
7. THE System SHALL maintain consistent spacing and layout proportions

### Requirement 9: Performance and Optimization

**User Story:** As a user, I want the interface to run smoothly at 60fps, so that interactions feel responsive and animations are fluid.

#### Acceptance Criteria

1. THE System SHALL target 60 frames per second for all animations
2. THE System SHALL lazy load images in the Timeline_Gallery
3. THE System SHALL use React.memo optimization for Photo_Card components
4. THE System SHALL use Framer Motion for animations with duration between 200-400ms
5. THE System SHALL minimize re-renders of unchanged components

### Requirement 10: API Integration

**User Story:** As a developer, I want the frontend to communicate with the backend API, so that filter and mode selections are properly synchronized.

#### Acceptance Criteria

1. WHEN a filter is selected, THE System SHALL POST to /set_filter endpoint with JSON body containing {filter: "FILTER_NAME"}
2. WHEN a mode is selected, THE System SHALL POST to /set_mode endpoint with JSON body containing {mode: "MODE_NAME"}
3. THE System SHALL handle API request errors gracefully without crashing
4. THE System SHALL initialize Supabase_Client with proper configuration from environment variables
5. THE System SHALL read Backend_API base URL from environment variable VITE_BACKEND_URL

### Requirement 11: Component Architecture

**User Story:** As a developer, I want a clear component structure, so that the codebase is maintainable and follows React best practices.

#### Acceptance Criteria

1. THE System SHALL organize components into the following hierarchy: App → HeaderHero, CameraSection, TimelineSection, QRModal
2. THE CameraSection SHALL contain CameraView, FilterPanel, and ModePanel as child components
3. THE TimelineSection SHALL contain EnergyLine and GalleryTimeline as child components
4. THE GalleryTimeline SHALL contain multiple PhotoCard components
5. THE System SHALL separate reusable components into individual files
6. THE System SHALL use React hooks for state management (useState, useEffect)

### Requirement 12: Responsive Layout Constraints

**User Story:** As a user, I want the interface to maintain proper proportions, so that the design looks consistent across different screen sizes.

#### Acceptance Criteria

1. THE Camera_Display SHALL maintain 16:9 aspect ratio regardless of viewport width
2. THE Timeline_Gallery SHALL occupy 60vh of viewport height
3. THE Filter_Panel and Mode_Panel SHALL arrange buttons horizontally with proper spacing
4. THE QR_Modal SHALL center itself in the viewport
5. THE System SHALL prevent horizontal scrolling of the main page

### Requirement 13: Error Handling and System Feedback

**User Story:** As a user, I want the interface to remain stable even if backend or network fails, so that the system never appears broken.

#### Acceptance Criteria

1. IF the Backend_API is unreachable, THE System SHALL display a subtle red warning indicator
2. THE System SHALL NOT crash on API failure
3. IF Supabase subscription fails, THE System SHALL retry connection
4. IF image loading fails, THE Photo_Card SHALL display a fallback placeholder
5. THE System SHALL log errors to the browser console in development mode only

### Requirement 14: Frontend State Management

**User Story:** As a developer, I want predictable state control, so that UI behavior remains consistent.

#### Acceptance Criteria

1. THE System SHALL maintain activeFilter state
2. THE System SHALL maintain activeMode state
3. THE System SHALL maintain selectedPhoto state
4. THE System SHALL maintain isQRModalOpen state
5. THE System SHALL use local component state only (no Redux)
6. THE System SHALL avoid global mutable variables

### Requirement 15: Security and Access Control

**User Story:** As a developer, I want to ensure secure access to backend services, so that sensitive credentials are not exposed.

#### Acceptance Criteria

1. THE System SHALL NOT expose Supabase service_role key
2. THE System SHALL use only anon public key in frontend
3. THE QR download link SHALL point to public storage URL only
4. THE frontend SHALL NOT allow direct database mutation
5. THE frontend SHALL NOT allow deletion of photos

### Requirement 16: Animation Behavior

**User Story:** As a user, I want smooth and consistent animations, so that the interface feels polished and responsive.

#### Acceptance Criteria

1. THE Energy_Line SHALL animate continuously with particle effect
2. Photo hover transition SHALL complete within 300ms
3. QR modal open animation SHALL complete within 250ms
4. Timeline entrance animation SHALL use ease-in-out curve
5. Animations SHALL NOT cause layout shifts

### Requirement 17: Non-Functional Constraints

**User Story:** As a developer, I want to ensure the system meets performance and compatibility standards, so that it functions reliably in the event environment.

#### Acceptance Criteria

1. THE System SHALL load initial interface within 2 seconds on broadband connection
2. THE System SHALL support modern Chromium-based browsers (Chrome, Edge, Brave)
3. THE System SHALL be optimized for 1920x1080 primary display resolution
4. THE System SHALL function without touch input (mouse-only environment)
5. THE System SHALL maintain 60fps performance during continuous operation
