#!/usr/bin/env python3
"""
Prepare CSV data for Label Studio import
"""

import pandas as pd
import json
import os
from pathlib import Path


def create_label_studio_json(data_path="../data/raw/audio_features.csv"):
    """
    Convert CSV data to Label Studio JSON format
    """
    # Read CSV data
    df = pd.read_csv(data_path)

    # Create JSON for Label Studio
    tasks = []

    for _, row in df.iterrows():
        task = {
            "data": {
                "segment_id": row["segment_id"],
                "audio_url": f"/data/upload/{row['segment_id']}.mp3",  # Update this path
                "genre_csv": row.get("genre", ""),
                "mood_csv": row.get("mood", ""),
                "bpm": row.get("bpm", ""),
                "duration": row.get("duration_sec", ""),
                "key": row.get("key", "")
            },
            "predictions": [
                {
                    "result": [
                        {
                            "from_name": "genre",
                            "to_name": "audio",
                            "type": "choices",
                            "value": {
                                "choices": [row.get("genre", "")]
                            }
                        },
                        {
                            "from_name": "mood",
                            "to_name": "audio",
                            "type": "choices",
                            "value": {
                                "choices": [row.get("mood", "")]
                            }
                        }
                    ]
                }
            ]
        }
        tasks.append(task)

    # Save to JSON file
    output_path = "labeling/label_studio_tasks.json"
    with open(output_path, "w") as f:
        json.dump(tasks, f, indent=2)

    print(f"Created Label Studio JSON with {len(tasks)} tasks")
    print(f"Saved to: {output_path}")

    return tasks


def create_simple_csv_for_upload():
    """
    Create a simple CSV with audio file references for Label Studio
    """
    df = pd.read_csv("../data/raw/audio_features.csv")

    # Create a simplified CSV for Label Studio
    simple_df = pd.DataFrame({
        "id": df["segment_id"],
        "segment_id": df["segment_id"],
        "audio": df["segment_id"] + ".mp3",  # Assuming .mp3 files exist
        "genre_original": df["genre"],
        "mood_original": df["mood"],
        "bpm": df["bpm"],
        "duration": df["duration_sec"]
    })

    output_path = "labeling/label_studio_upload.csv"
    simple_df.to_csv(output_path, index=False)

    print(f"Created upload CSV: {output_path}")
    print("Columns:", list(simple_df.columns))

    return simple_df


def generate_sample_audio_links():
    """
    Generate sample audio file links or instructions
    """
    instructions = """
    Audio File Setup Instructions:

    1. Place your audio files in: /data/upload/
    2. Name them as: seg_001.mp3, seg_002.mp3, etc.
    3. Or use hosted URLs in the CSV:
       - Format: http://your-server/audio/seg_001.mp3

    For testing, you can use placeholder audio files or:
    1. Download sample music from: https://freemusicarchive.org/
    2. Convert to MP3 format
    3. Rename to match segment_id from CSV
    """

    print(instructions)

    # Create a sample audio mapping file
    mapping = []
    df = pd.read_csv("../data/raw/audio_features.csv")

    for seg_id in df["segment_id"]:
        mapping.append({
            "segment_id": seg_id,
            "expected_file": f"{seg_id}.mp3",
            "local_path": f"./data/upload/{seg_id}.mp3",
            "hosted_url": f"http://localhost:8080/data/upload/{seg_id}.mp3"
        })

    mapping_path = "labeling/audio_file_mapping.json"
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2)

    print(f"Audio mapping created: {mapping_path}")

    return mapping


def main():
    """Main function to prepare Label Studio data"""
    print("=" * 60)
    print("PREPARING DATA FOR LABEL STUDIO")
    print("=" * 60)

    # Ensure labeling directory exists
    Path("labeling").mkdir(exist_ok=True)

    # 1. Create Label Studio JSON
    print("\n1. Creating Label Studio JSON format...")
    tasks = create_label_studio_json()

    # 2. Create simplified CSV
    print("\n2. Creating simplified CSV for upload...")
    simple_df = create_simple_csv_for_upload()

    # 3. Generate audio file instructions
    print("\n3. Generating audio file setup instructions...")
    mapping = generate_sample_audio_links()

    # 4. Create complete setup summary
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nFiles created:")
    print("1. labeling/music_labeling_interface.xml - Labeling interface")
    print("2. labeling/label_studio_tasks.json - Tasks in JSON format")
    print("3. labeling/label_studio_upload.csv - Simplified CSV for upload")
    print("4. labeling/audio_file_mapping.json - Audio file mapping")

    print("\nNext steps in Label Studio:")
    print("1. Create new project: 'Music-Generation-Quality'")
    print("2. Import labeling/label_studio_upload.csv")
    print("3. Copy interface code from music_labeling_interface.xml")
    print("4. Start labeling!")

    return True


if __name__ == "__main__":
    main()