import random
import pygame
import time
import numpy
from pydub import AudioSegment
from pydub.playback import play
import time  # Don't forget to import the time module


def generate_random_notes(num_notes):
    # Define the possible musical notes
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Generate a list of random notes and octaves
    random_notes = [(random.choice(notes), random.randint(2, 3)) for _ in range(num_notes)]

    return random_notes

def play_music_notes(notes, duration, waveform_type):
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
    
    if waveform_type == 'sine':
        freq_array_function = freq_array_sine_envelope
    elif waveform_type == 'triangle':
        freq_array_function = freq_array_triangle_envelope
    elif waveform_type == 'sawtooth':
        freq_array_function = freq_array_sawtooth_envelope
    elif waveform_type == 'square':
        freq_array_function = freq_array_square_envelope
    elif waveform_type == 'sine-square':
        freq_array_function = freq_array_sine_square_envelope
    else:
        print(f"Invalid waveform type: {waveform_type}")
        return

    # Initialize pygame mixer
    pygame.mixer.init()

    # Set the note duration (in milliseconds)
    note_duration = duration  # You can adjust this value

    # Generate Pygame sound objects for each note
    sounds = []
    for note, octave in notes:
        frequency = note_frequencies.get(note, octave) * (2 ** (octave - 4))
        if frequency == 0:
            print(f"Invalid note: {note}")
            return

        sound_array = freq_array_function(frequency, note_duration)
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

def freq_array_square_envelope(frequency, length_ms):
    sample_rate = 44100  # Adjust as needed
    length = int(sample_rate * length_ms / 1000)
    t = numpy.linspace(0, length_ms / 1000, length, endpoint=False)

    # Generate a square waveform
    waveform = numpy.sign(numpy.sin(2 * numpy.pi * frequency * t))

    # Apply an envelope to smooth the sound
    envelope = numpy.linspace(0, 1, int(0.1 * sample_rate))  # 10% of the sound for attack
    envelope = numpy.concatenate([envelope, numpy.ones(length - 2 * len(envelope)), envelope[::-1]])
    waveform *= envelope

    # Normalize the waveform to be between -1 and 1
    waveform /= numpy.max(numpy.abs(waveform))

    return (waveform * 32767).astype(numpy.int16)

def freq_array_sine_square_envelope(frequency, length_ms):
    sample_rate = 44100  # Adjust as needed
    length = int(sample_rate * length_ms / 1000)
    t = numpy.linspace(0, length_ms / 1000, length, endpoint=False)

    # Generate a sine-square waveform
    waveform = 0.5 * (numpy.sin(2 * numpy.pi * frequency * t) + numpy.sign(numpy.sin(2 * numpy.pi * frequency * t)))

    # Apply an envelope to smooth the sound
    envelope = numpy.linspace(0, 1, int(0.1 * sample_rate))  # 10% of the sound for attack
    envelope = numpy.concatenate([envelope, numpy.ones(length - 2 * len(envelope)), envelope[::-1]])
    waveform *= envelope

    # Normalize the waveform to be between -1 and 1
    waveform /= numpy.max(numpy.abs(waveform))

    return (waveform * 32767).astype(numpy.int16)

def freq_array_triangle_envelope(frequency, length_ms):
    sample_rate = 44100  # Adjust as needed
    length = int(sample_rate * length_ms / 1000)
    t = numpy.linspace(0, length_ms / 1000, length, endpoint=False)
    
    # Generate a triangle waveform
    waveform = numpy.abs(2 * (t * frequency - numpy.floor(0.5 + t * frequency)))

    # Apply an envelope to smooth the sound
    envelope = numpy.linspace(0, 1, int(0.1 * sample_rate))  # 10% of the sound for attack
    envelope = numpy.concatenate([envelope, numpy.ones(length - 2 * len(envelope)), envelope[::-1]])
    waveform *= envelope

    # Normalize the waveform to be between -1 and 1
    waveform /= numpy.max(numpy.abs(waveform))

    return (waveform * 32767).astype(numpy.int16)

def freq_array_sawtooth_envelope(frequency, length_ms):
    sample_rate = 44100  # Adjust as needed
    length = int(sample_rate * length_ms / 1000)
    t = numpy.linspace(0, length_ms / 1000, length, endpoint=False)
    
    # Generate a sawtooth waveform
    waveform = 2 * (t * frequency - numpy.floor(0.5 + t * frequency))

    # Apply an envelope to smooth the sound
    envelope = numpy.linspace(0, 1, int(0.1 * sample_rate))  # 10% of the sound for attack
    envelope = numpy.concatenate([envelope, numpy.ones(length - 2 * len(envelope)), envelope[::-1]])
    waveform *= envelope

    # Normalize the waveform to be between -1 and 1
    waveform /= numpy.max(numpy.abs(waveform))

    return (waveform * 32767).astype(numpy.int16)

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

# Example usage
for i in range(0,1):
    #define a tempo
    bpm=85
    num_notes = 1
    random_notes = generate_random_notes(num_notes)
    minninechord = get_chord_notes(random_notes[0][0], random_notes[0][1], 'dom9')
    print(f"Random Music Notes: {random_notes}")
    play_music_notes(minninechord,10000,'square')
    play_music_notes([minninechord[0]],300,'square')
    play_music_notes([minninechord[1]],300,'square')
    play_music_notes([minninechord[2]],300,'square')
    play_music_notes([minninechord[3]],300,'square')
