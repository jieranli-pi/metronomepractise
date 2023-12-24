import pygame
import time

def get_interval(note, interval):
    # Define a dictionary to map note names to their corresponding index in the chromatic scale
    note_index = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
                  'E': 4, 'Fb': 4, 'E#': 5, 'F': 5, 'F#': 6, 'Gb': 6,
                  'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}

    # Define a dictionary to map intervals to their semitone values
    interval_semitones = {'m2': 1, 'M2': 2, 'm3': 3, 'M3': 4, 'P4': 5, 'A4': 6, 'd5': 6, 'P5': 7, 'A5': 8,
                          'm6': 8, 'M6': 9, 'm7': 10, 'M7': 11}

    # Ensure the provided note and interval are valid
    if note not in note_index or interval not in interval_semitones:
        raise ValueError("Invalid note or interval")

    # Calculate the new note index after applying the interval
    new_index = (note_index[note] + interval_semitones[interval]) % 12

    # Find the note name corresponding to the new index
    result_note = [k for k, v in note_index.items() if v == new_index][0]

    return result_note

def onesixtwofive(note):
    one=note;
    six=get_interval(note, 'M6')
    two=get_interval(note, 'M2')
    five=get_interval(note, 'P5')
    
    return one, six, two, five
    
def metronome(bpm, duration):
    pygame.init()
    pygame.mixer.init()

    # Load metronome sound file (replace 'bassdrum0.wav' with the path to your sound file)
    sound = pygame.mixer.Sound('bassdrum0.wav')

    # Calculate the time delay between each beat based on the BPM
    beat_duration = 60 / bpm

    beat_counter = 0  # Initialize beat counter

    # Initialize Pygame font for text rendering
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 36)

    # Set up the Pygame window
    window_size = (400, 200)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Metronome')
    
    #starting note
    note="C"

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

            # Increment the beat counter
            beat_counter += 1

            # Play the metronome sound
            sound.play()

            # Determine the remainder when dividing beat_counter by 4
            ffremainder = beat_counter % 4 + 1
                        
            # Determine the remainder when dividing beat_counter by 3
            tfremainder = beat_counter % 3 + 1
            
            # Create chord progression
            one, six, two, five=onesixtwofive(note)
            
            # Create a string for the beat counter and graph
            line1_surface = font.render(f'4/4: {ffremainder} 4/3: {tfremainder}', True, (255, 255, 255))
            line2_surface = font.render(f'{one} {six} {two} {five}', True, (255, 255, 255))
            # Clear the screen
            screen.fill((0, 0, 0))

            # Blit the text surfaces onto the screen at different positions
            screen.blit(line1_surface, (10, 10))
            screen.blit(line2_surface, (10, 60))

            # Update the display
            pygame.display.flip()

            # Wait for the specified duration before the next beat
            time.sleep(beat_duration)

    except KeyboardInterrupt:
        # Handle keyboard interrupt (close the Pygame window)
        pygame.mixer.quit()
        pygame.quit()

if __name__ == "__main__":
    # Set the BPM (beats per minute) and duration (in seconds)
    bpm = 120
    duration = 300  # Set the total duration in seconds (e.g., 300 seconds = 5 minutes)

    # Call the metronome function
    metronome(bpm, duration)
