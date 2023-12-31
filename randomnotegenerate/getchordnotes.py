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
note_name = 'C'
octave = 3
chord_type = 'maj'
result = get_chord_notes(note_name, octave, chord_type)
print(f"Chord Notes for {note_name}{octave} {chord_type}: {result}")
