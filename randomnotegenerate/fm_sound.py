import random
import pygame
import time
import numpy as np

def play_fm_synth_chord(chord, duration_ms, modulator_frequency=20.0, modulation_index=50.0, sample_rate=44100):
    pygame.mixer.init(frequency=sample_rate)

    # Get the base note (frequency) of the chord
    base_note = note_to_frequency(chord[0][0], chord[0][1])

    # Generate the carrier waveform for the base note
    carrier_waveform = fm_synth_carrier(base_note, duration_ms, sample_rate)

    # Generate the modulator waveform
    modulator_waveform = fm_synth_modulator(modulator_frequency, modulation_index, duration_ms, sample_rate)

    # Apply FM synthesis by modulating the carrier with the modulator
    fm_synth_waveform = carrier_waveform * (1.0 + modulator_waveform)

    # Normalize the waveform to be between -1 and 1
    fm_synth_waveform /= np.max(np.abs(fm_synth_waveform))

    # Create a stereo sound array by duplicating the mono waveform for both channels
    sound_array_stereo = np.column_stack((fm_synth_waveform, fm_synth_waveform))

    # Create a Pygame sound object and play it
    sound = pygame.sndarray.make_sound((sound_array_stereo * 32767).astype(np.int16))
    sound.play()
    
    # Allow the sound to play for the specified duration
    time.sleep(duration_ms / 1000.0)

def note_to_frequency(note, octave):
    # Dictionary mapping notes to corresponding frequencies
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
    return note_frequencies.get(note, octave) * (2 ** (octave - 4))

def get_chord_notes(note, octave, chord_type):
    # Define the possible musical notes
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Map note names to indices
    note_index = notes.index(note)

    # Calculate the starting note's index in the chromatic scale
    start_index = note_index + (octave - 1) * len(notes)

    # Define intervals for each chord type
    chord_intervals = {
        'maj': [0, 4, 7],
        'minor': [0, 3, 7],
        'aug': [0, 4, 8],
        'dim': [0, 3, 6],
        'halfdim': [0, 3, 6, 10],
        'maj7': [0, 4, 7, 11],
        'min7': [0, 3, 7, 10],
        'dom7': [0, 4, 7, 10],
        'majmin7': [0, 4, 7, 10],
        'maj6': [0, 4, 7, 9],
        'min6': [0, 3, 7, 9],
        'maj9': [0, 4, 7, 11, 14],
        'min9': [0, 3, 7, 10, 14],
        'dom9': [0, 4, 7, 10, 14],
        'dom13': [0, 4, 7, 10, 14, 21],
        '7b9': [0, 4, 7, 10, 13]
    }

    # Calculate the notes in the chord
    chord_notes = [(notes[(start_index + interval) % len(notes)], octave + (start_index + interval) // len(notes))
                   for interval in chord_intervals.get(chord_type, [])]

    return chord_notes

def fm_synth_carrier(frequency, duration_ms, sample_rate=44100):
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), endpoint=False)
    return np.sin(2 * np.pi * frequency * t)

def fm_synth_modulator(mod_freq, mod_index, duration_ms, sample_rate=44100):
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), endpoint=False)
    return np.sin(2 * np.pi * mod_freq * t) * mod_index

def play_fm_synth_carrier(frequency, duration_ms, sample_rate=44100):
    pygame.mixer.init(frequency=sample_rate)
    sound_array_mono = fm_synth_carrier(frequency, duration_ms, sample_rate)
    
    # Duplicate the mono waveform for both channels (stereo)
    sound_array_stereo = np.column_stack((sound_array_mono, sound_array_mono))
    
    sound = pygame.sndarray.make_sound((sound_array_stereo * 32767).astype(np.int16))
    sound.play()
    time.sleep(duration_ms / 1000.0)

def play_fm_synth_modulator(mod_freq, mod_index, duration_ms, sample_rate=44100):
    pygame.mixer.init(frequency=sample_rate)
    sound_array_mono = fm_synth_modulator(mod_freq, mod_index, duration_ms, sample_rate)
    
    # Duplicate the mono waveform for both channels (stereo)
    sound_array_stereo = np.column_stack((sound_array_mono, sound_array_mono))
    
    sound = pygame.sndarray.make_sound((sound_array_stereo * 32767).astype(np.int16))
    sound.play()
    time.sleep(duration_ms / 1000.0)

# Example usage
num_notes = 1
random_notes = [(random.choice(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']), random.randint(2, 3))
                for _ in range(num_notes)]



minninechord = get_chord_notes(random_notes[0][0], random_notes[0][1], 'dom9')
print(f"Random Music Notes: {random_notes}")
play_fm_synth_chord(random_notes, 500)
play_fm_synth_chord(minninechord, 500)
