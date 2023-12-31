import random
import pygame
import time
import numpy

def generate_random_notes(num_notes):
    # Define the possible musical notes
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Generate a list of random notes and octaves
    random_notes = [(random.choice(notes), random.randint(3, 5)) for _ in range(num_notes)]

    return random_notes

def play_music_notes(notes):
    # Dictionary mapping notes to corresponding frequencies (adjust as needed)
    note_frequencies = {
        'C': 261.63,
        'C#': 277.18,
        'D': 293.66,
        'D#': 311.13,
        'E': 329.63,
        'F': 349.23,
        'F#': 369.99,
        'G': 392.00,
        'G#': 415.30,
        'A': 440.00,
        'A#': 466.16,
        'B': 493.88
    }

    # Initialize pygame mixer
    pygame.mixer.init()

    # Set the note duration (in milliseconds)
    note_duration = 500  # You can adjust this value

    # Generate Pygame sound objects for each note
    sounds = []
    for note, octave in notes:
        frequency = note_frequencies.get(note, octave) * (2 ** (octave - 4))
        if frequency == 0:
            print(f"Invalid note: {note}")
            return

        sound_array = freq_array_sine_envelope(frequency, note_duration)
        sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=pygame.sndarray.array(sound_array)))
        sounds.append(sound)

    # Play all sounds simultaneously
    for sound in sounds:
        sound.play()

    # Allow the sounds to play for the specified duration
    time.sleep(note_duration / 1000.0)

def freq_array_sine_envelope(frequency, length_ms):
    sample_rate = 44100  # Adjust as needed
    length = int(sample_rate * length_ms / 1000)
    t = numpy.linspace(0, length_ms / 1000, length, endpoint=False)
    waveform = numpy.sin(2 * numpy.pi * frequency * t)

    # Apply a simple envelope to smooth the sound
    envelope = numpy.linspace(0, 1, int(0.1 * sample_rate))  # 10% of the sound for attack
    envelope = numpy.concatenate([envelope, numpy.ones(length - 2 * len(envelope)), envelope[::-1]])
    waveform *= envelope

    # Normalize the waveform to be between -1 and 1
    waveform /= numpy.max(numpy.abs(waveform))

    return (waveform * 32767).astype(numpy.int16)

# Example usage
for i in range(1,50):
    num_notes = 2
    random_notes = generate_random_notes(num_notes)
    print(f"Random Music Notes: {random_notes}")
    play_music_notes(random_notes)
