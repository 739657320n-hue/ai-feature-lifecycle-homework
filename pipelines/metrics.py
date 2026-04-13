#!/usr/bin/env python3
"""
Simulated evaluation metrics for music generation.
All metrics are simulated for demonstration purposes.
"""

import random
import time
from typing import List, Dict, Any
import numpy as np


class SimulatedMetrics:
    """Simulated metrics calculator for music generation"""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)

    def calculate_structure_score(self, notes: List[Dict]) -> float:
        """
        Simulate structure score calculation

        Args:
            notes: List of note dictionaries

        Returns:
            Structure score between 0 and 1
        """
        # Simulate computation time
        time.sleep(0.001)

        if not notes:
            return 0.0

        # Mock structure analysis
        # Check note density (not too sparse, not too dense)
        total_duration = max(note['start'] + note['duration'] for note in notes)
        note_density = len(notes) / max(total_duration, 1)

        # Check pitch range (not too wide)
        pitches = [note['pitch'] for note in notes]
        pitch_range = max(pitches) - min(pitches) if pitches else 0

        # Check rhythm consistency
        durations = [note['duration'] for note in notes]
        duration_variance = np.var(durations) if durations else 0

        # Combine factors into a score
        density_score = min(note_density / 5, 1.0)  # Optimal ~5 notes/sec
        range_score = 1.0 - min(pitch_range / 48, 1.0)  # Optimal < 4 octaves
        rhythm_score = 1.0 - min(duration_variance / 0.1, 1.0)  # Low variance

        # Weighted average
        structure_score = (0.4 * density_score +
                           0.3 * range_score +
                           0.3 * rhythm_score)

        return max(0.0, min(1.0, structure_score))

    def calculate_style_consistency(self, notes: List[Dict],
                                    target_genre: str) -> float:
        """
        Simulate style consistency score

        Args:
            notes: List of note dictionaries
            target_genre: Target genre to match

        Returns:
            Style consistency score between 0 and 1
        """
        time.sleep(0.001)

        if not notes:
            return 0.0

        # Mock genre analysis based on simple rules
        genre_profiles = {
            "pop": {
                "pitch_range": (60, 80),  # Middle range
                "note_density": 4.0,  # Medium density
                "duration_variance": 0.05  # Moderate variance
            },
            "classical": {
                "pitch_range": (48, 96),  # Wide range
                "note_density": 8.0,  # High density
                "duration_variance": 0.02  # Low variance
            },
            "jazz": {
                "pitch_range": (55, 85),  # Medium-high range
                "note_density": 6.0,  # Medium-high density
                "duration_variance": 0.08  # High variance
            },
            "rock": {
                "pitch_range": (40, 70),  # Low range
                "note_density": 3.0,  # Low density
                "duration_variance": 0.1  # Very high variance
            }
        }

        if target_genre not in genre_profiles:
            target_genre = "pop"

        profile = genre_profiles[target_genre]

        # Extract features
        pitches = [note['pitch'] for note in notes]
        avg_pitch = np.mean(pitches) if pitches else 60

        total_duration = max(note['start'] + note['duration'] for note in notes)
        note_density = len(notes) / max(total_duration, 1)

        durations = [note['duration'] for note in notes]
        duration_variance = np.var(durations) if durations else 0

        # Compare with profile
        pitch_score = 1.0 - min(abs(avg_pitch - np.mean(profile['pitch_range'])) / 20, 1.0)
        density_score = 1.0 - min(abs(note_density - profile['note_density']) / 5, 1.0)
        variance_score = 1.0 - min(abs(duration_variance - profile['duration_variance']) / 0.1, 1.0)

        # Weighted average
        style_score = (0.4 * pitch_score +
                       0.4 * density_score +
                       0.2 * variance_score)

        return max(0.0, min(1.0, style_score))

    def calculate_note_diversity(self, notes: List[Dict]) -> float:
        """Simulate note diversity score"""
        time.sleep(0.0005)

        if len(notes) < 2:
            return 0.0

        # Mock diversity calculation
        pitches = [note['pitch'] for note in notes]
        unique_pitches = len(set(pitches))
        diversity = unique_pitches / min(len(notes), 20)  # Normalize

        return min(1.0, diversity)

    def calculate_rhythm_stability(self, notes: List[Dict]) -> float:
        """Simulate rhythm stability score"""
        time.sleep(0.0005)

        if len(notes) < 3:
            return 0.5

        # Mock rhythm analysis
        durations = [note['duration'] for note in notes]
        if len(set(durations)) < 2:
            return 0.3  # Too repetitive

        # Check for patterns in durations
        # Simple mock: less variance = more stable
        variance = np.var(durations)
        stability = 1.0 - min(variance / 0.05, 1.0)

        return max(0.0, min(1.0, stability))

    def calculate_melodic_coherence(self, notes: List[Dict]) -> float:
        """Simulate melodic coherence score"""
        time.sleep(0.001)

        if len(notes) < 3:
            return 0.5

        # Mock melodic analysis
        pitches = [note['pitch'] for note in notes]

        # Check for large jumps
        jumps = [abs(pitches[i] - pitches[i - 1]) for i in range(1, len(pitches))]
        large_jumps = sum(1 for jump in jumps if jump > 7)  # > perfect fifth

        # Check direction changes
        directions = []
        for i in range(2, len(pitches)):
            dir1 = pitches[i - 1] - pitches[i - 2]
            dir2 = pitches[i] - pitches[i - 1]
            if dir1 * dir2 < 0:  # Change direction
                directions.append(1)
            else:
                directions.append(0)

        jump_score = 1.0 - (large_jumps / max(len(jumps), 1))
        direction_score = 1.0 - (sum(directions) / max(len(directions), 1))

        coherence = 0.6 * jump_score + 0.4 * direction_score

        return max(0.0, min(1.0, coherence))

    def evaluate_music(self, notes: List[Dict], target_genre: str) -> Dict:
        """
        Comprehensive evaluation of generated music

        Args:
            notes: Generated notes
            target_genre: Target genre

        Returns:
            Dictionary of all metrics
        """
        print(f"Evaluating {len(notes)} notes for {target_genre} genre...")

        metrics = {
            "structure_score": self.calculate_structure_score(notes),
            "style_consistency": self.calculate_style_consistency(notes, target_genre),
            "note_diversity": self.calculate_note_diversity(notes),
            "rhythm_stability": self.calculate_rhythm_stability(notes),
            "melodic_coherence": self.calculate_melodic_coherence(notes),
            "num_notes": len(notes)
        }

        return metrics


def main():
    """Demonstrate metrics calculation"""
    print("Simulated Music Evaluation Metrics")
    print("=" * 50)

    # Create mock notes for testing
    mock_notes = []
    for i in range(20):
        mock_notes.append({
            "pitch": random.randint(60, 72),
            "start": i * 0.5,
            "duration": random.choice([0.25, 0.5, 0.75]),
            "velocity": random.randint(70, 90)
        })

    # Initialize metrics calculator
    metrics_calc = SimulatedMetrics()

    # Calculate all metrics
    results = metrics_calc.evaluate_music(mock_notes, "pop")

    print("\nEvaluation Results:")
    for metric, value in results.items():
        print(f"  {metric}: {value:.3f}")

    # Overall quality score (weighted average)
    weights = {
        "structure_score": 0.3,
        "style_consistency": 0.3,
        "note_diversity": 0.1,
        "rhythm_stability": 0.15,
        "melodic_coherence": 0.15
    }

    overall_score = sum(results[k] * weights[k]
                        for k in weights if k in results)
    print(f"\nOverall Quality Score: {overall_score:.3f}")


if __name__ == "__main__":
    main()