import pygame
import time

def metronome(bpm, duration):
    pygame.init()
    pygame.mixer.init()

    # Load metronome sound file (replace 'bassdrum0.wav' with the path to your sound file)
    sound = pygame.mixer.Sound('bassdrum0.wav')

    # Calculate the time delay between each beat based on the BPM
    beat_duration = 60 / bpm

    beat_counter = 0  # Initialize beat counter

    try:
        while True:
            # Increment the beat counter
            beat_counter += 1

            # Play the metronome sound
            sound.play()

            # Print the beat counter
            print(f'Beat {beat_counter}')

            # Wait for the specified duration before the next beat
            time.sleep(beat_duration)

            # Check for the Esc key press to terminate the program
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    raise KeyboardInterrupt  # Raise KeyboardInterrupt to exit the loop

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C or Esc) to stop the metronome
        pygame.mixer.quit()
        pygame.quit()

if __name__ == "__main__":
    # Set the BPM (beats per minute) and duration (in seconds)
    bpm = 120
    duration = 300  # Set the total duration in seconds (e.g., 300 seconds = 5 minutes)

    # Call the metronome function
    metronome(bpm, duration)
 