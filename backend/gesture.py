import mediapipe as mp

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )

    def process_frame(self, rgb_frame):
        """
        Processes an RGB frame and returns (results, gesture_name).
        Main gesture supported: "THUMBS_UP".
        """
        results = self.hands.process(rgb_frame)
        gesture = None

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                gesture = self._classify_gesture(handLms.landmark)
                break  # Only evaluate the first hand
                
        return results, gesture

    def _classify_gesture(self, landmarks):
        # Y-coordinates increase moving downwards.
        thumb_tip = landmarks[4].y
        thumb_ip = landmarks[3].y
        thumb_base = landmarks[2].y
        
        index_tip = landmarks[8].y
        index_pip = landmarks[6].y
        
        middle_tip = landmarks[12].y
        middle_pip = landmarks[10].y
        
        ring_tip = landmarks[16].y
        ring_pip = landmarks[14].y
        
        pinky_tip = landmarks[20].y
        pinky_pip = landmarks[18].y

        # Helper to check if a finger is extended (tip is higher than pip)
        is_index_ext = index_tip < index_pip
        is_middle_ext = middle_tip < middle_pip
        is_ring_ext = ring_tip < ring_pip
        is_pinky_ext = pinky_tip < pinky_pip

        # THUMBS UP Logic
        # All fingers except thumb are closed
        fingers_closed = (not is_index_ext) and (not is_middle_ext) and (not is_ring_ext) and (not is_pinky_ext)
        if fingers_closed:
            # Thumb tip must be significantly higher than its base
            if thumb_tip < thumb_base:
                return "THUMBS_UP"

        return None

    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
