#!/usr/bin/env python3
"""
Random Music Generator (Baseline Model)
Simple rule-based random music generation for baseline comparison.
All outputs are simulated for demonstration purposes.
"""

import random
import json
import time
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Note:
    """Simple note representation"""
    pitch: int  # MIDI pitch (48-84 = C3 to C6)
    start: float  # Start time in seconds
    duration: float  # Duration in seconds
    velocity: int  # Note velocity (60-100)


class RandomMusicGenerator:
    """Baseline model: random music generator"""

    def __init__(self, seed: int = 42):
        """Initialize random generator with seed"""
        random.seed(seed)
        self.seed = seed

    def generate_segment(self, duration_sec: float = 10.0,
                         genre: str = "pop") -> List[Note]:
        """
        Generate a random music segment

        Args:
            duration_sec: Length of music segment
            genre: Target genre (not actually used in baseline)

        Returns:
            List of Note objects
        """
        # Simulate generation time
        time.sleep(0.01)  # 10ms for demonstration

        notes = []
        current_time = 0.0

        # Generate random notes until duration is reached
        while current_time < duration_sec:
            # Random note parameters
            pitch = random.randint(48, 84)  # C3 to C6
            duration = random.choice([0.25, 0.5, 1.0])
            velocity = random.randint(60, 100)

            # Ensure note doesn't exceed segment duration
            if current_time + duration > duration_sec:
                duration = duration_sec - current_time

            note = Note(
                pitch=pitch,
                start=current_time,
                duration=duration,
                velocity=velocity
            )
            notes.append(note)

            # Move to next note start time
            current_time += duration

        return notes

    def save_to_jsonl(self, notes: List[Note], filename: str):
        """Save generated notes to JSONL file"""
        with open(filename, 'w') as f:
            for note in notes:
                note_dict = {
                    "pitch": note.pitch,
                    "start": note.start,
                    "duration": note.duration,
                    "velocity": note.velocity
                }
                f.write(json.dumps(note_dict) + '\n')

    def simulate_performance(self) -> Dict:
        """Simulate baseline model performance metrics"""
        return {
            "generation_speed_ms": 10.0,  # 10ms per segment
            "structure_score": 0.3,  # Low score (random)
            "style_consistency": 0.2,  # Very low (random)
            "note_diversity": 0.7,  # High (random notes)
            "rhythm_stability": 0.3,  # Low (random rhythm)
            "melodic_coherence": 0.2  # Very low (random)
        }


def main():
    """Demonstrate baseline model usage"""
    print("Random Music Generator (Baseline)")
    print("=" * 50)

    # Initialize generator
    generator = RandomMusicGenerator(seed=42)

    # Generate a sample segment
    print("Generating 10-second pop music segment...")
    notes = generator.generate_segment(duration_sec=10.0, genre="pop")

    print(f"Generated {len(notes)} notes")
    print("Sample notes:")
    for i, note in enumerate(notes[:3]):
        print(f"  Note {i + 1}: pitch={note.pitch}, start={note.start:.2f}s, "
              f"duration={note.duration:.2f}s")

    # Show simulated performance
    print("\nSimulated Performance Metrics:")
    metrics = generator.simulate_performance()
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    # Save to file for demonstration
    generator.save_to_jsonl(notes, "baseline_output.jsonl")
    print(f"\nSaved to: baseline_output.jsonl")


if __name__ == "__main__":
    main()