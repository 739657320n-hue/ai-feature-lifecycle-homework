#!/usr/bin/env python3
"""
Simplified Transformer Music Generator (Simulated)
Mock implementation for demonstration purposes only.
No actual training or inference happens.
"""

import random
import json
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class ModelConfig:
    """Mock transformer configuration"""
    num_layers: int = 2
    hidden_size: int = 128
    num_heads: int = 4
    vocab_size: int = 128  # MIDI pitches
    max_seq_length: int = 100
    dropout: float = 0.1


class SimulatedTransformer:
    """Mock transformer model for music generation"""

    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize with mock configuration"""
        self.config = config or ModelConfig()
        self.is_trained = False
        self.training_losses = []

        # Simulated model parameters
        self.params_count = 50000  # ~50K parameters
        print(f"Initialized simulated transformer with {self.params_count:,} parameters")

    def simulate_training(self, num_epochs: int = 10) -> Dict:
        """
        Simulate training process

        Args:
            num_epochs: Number of training epochs

        Returns:
            Training statistics
        """
        print(f"Simulating training for {num_epochs} epochs...")

        # Generate fake training losses
        self.training_losses = []
        for epoch in range(num_epochs):
            # Simulate decreasing loss
            loss = 2.0 * (0.9 ** epoch) + random.uniform(0, 0.1)
            self.training_losses.append(loss)

            # Simulate epoch time
            time.sleep(0.1)
            print(f"  Epoch {epoch + 1}/{num_epochs}: loss = {loss:.4f}")

        self.is_trained = True

        return {
            "final_loss": self.training_losses[-1],
            "num_epochs": num_epochs,
            "training_time_sec": num_epochs * 0.1
        }

    def generate_music(self, prompt: str = "", duration_sec: float = 10.0,
                       genre: str = "pop") -> List[Dict]:
        """
        Simulate music generation

        Args:
            prompt: Text prompt (not used in mock)
            duration_sec: Duration of generated music
            genre: Target genre for generation

        Returns:
            List of note dictionaries
        """
        if not self.is_trained:
            print("Warning: Model not trained, using random generation")

        # Simulate generation time (faster than baseline)
        time.sleep(0.005)  # 5ms

        # Generate somewhat structured notes based on genre
        notes = []
        current_time = 0.0

        # Genre-specific patterns (simulated)
        if genre == "pop":
            # Pop: simple chord progressions
            chords = [[60, 64, 67], [62, 65, 69], [59, 62, 67], [60, 64, 67]]
            note_duration = 1.0
        elif genre == "classical":
            # Classical: arpeggios
            chords = [[60, 64, 67], [62, 65, 69]]
            note_duration = 0.25
        elif genre == "jazz":
            # Jazz: seventh chords
            chords = [[60, 64, 67, 70], [62, 65, 69, 72]]
            note_duration = 0.5
        else:  # rock
            # Rock: power chords
            chords = [[60, 67], [62, 69]]
            note_duration = 0.5

        chord_index = 0
        while current_time < duration_sec:
            # Get current chord
            chord = chords[chord_index % len(chords)]

            # Generate notes from chord
            for pitch in chord:
                if current_time + note_duration > duration_sec:
                    note_duration = duration_sec - current_time

                note = {
                    "pitch": pitch + random.randint(-1, 1),  # Small variation
                    "start": current_time,
                    "duration": note_duration,
                    "velocity": random.randint(70, 90)
                }
                notes.append(note)

            current_time += note_duration
            chord_index += 1

        return notes

    def simulate_performance(self) -> Dict:
        """Simulate model performance metrics"""
        if not self.is_trained:
            return {
                "generation_speed_ms": 10.0,
                "structure_score": 0.3,
                "style_consistency": 0.2
            }

        # Simulated better performance after training
        return {
            "generation_speed_ms": 5.0,  # 5ms per segment (faster)
            "structure_score": 0.75,  # Better structure
            "style_consistency": 0.65,  # Better style match
            "note_diversity": 0.6,  # Moderate diversity
            "rhythm_stability": 0.7,  # Good rhythm
            "melodic_coherence": 0.75  # Good melody
        }

    def save_checkpoint(self, path: str):
        """Save mock model checkpoint"""
        checkpoint = {
            "config": self.config.__dict__,
            "is_trained": self.is_trained,
            "training_losses": self.training_losses,
            "params_count": self.params_count
        }

        with open(path, 'w') as f:
            json.dump(checkpoint, f, indent=2)

        print(f"Saved mock checkpoint to {path}")

    def load_checkpoint(self, path: str):
        """Load mock model checkpoint"""
        print(f"Loading mock checkpoint from {path}")
        # In real implementation, would load weights
        self.is_trained = True
        print("Checkpoint loaded (simulated)")


def main():
    """Demonstrate simulated transformer model"""
    print("Simulated Transformer Music Generator")
    print("=" * 50)

    # Initialize model
    config = ModelConfig(num_layers=2, hidden_size=128, num_heads=4)
    model = SimulatedTransformer(config)

    # Simulate training
    print("\n1. Training Simulation:")
    training_stats = model.simulate_training(num_epochs=5)
    print(f"Training complete. Final loss: {training_stats['final_loss']:.4f}")

    # Generate music
    print("\n2. Generation Simulation:")
    notes = model.generate_music(duration_sec=8.0, genre="pop")
    print(f"Generated {len(notes)} notes")

    # Show sample notes
    print("Sample notes:")
    for i, note in enumerate(notes[:3]):
        print(f"  Note {i + 1}: pitch={note['pitch']}, "
              f"start={note['start']:.2f}s, duration={note['duration']:.2f}s")

    # Show performance metrics
    print("\n3. Performance Metrics:")
    metrics = model.simulate_performance()
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    # Save checkpoint
    model.save_checkpoint("transformer_checkpoint.json")


if __name__ == "__main__":
    main()