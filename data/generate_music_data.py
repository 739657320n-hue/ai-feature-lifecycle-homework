#!/usr/bin/env python3
"""
生成模拟音乐数据 - 20个音乐片段
生成CSV特征数据和JSONL音符序列
"""

import pandas as pd
import numpy as np
import json
import os
import random
from datetime import datetime
from pathlib import Path

# 设置随机种子确保可重复性
random.seed(42)
np.random.seed(42)


def generate_segment_id(index):
    """生成片段ID，格式: seg_001"""
    return f"seg_{index:03d}"


def generate_music_parameters():
    """生成音乐参数"""
    genres = ["pop", "classical", "jazz", "rock"]
    moods = ["happy", "sad", "calm", "energetic"]
    keys = ["C_major", "G_major", "D_minor", "A_minor", "F_major", "E_minor"]

    return {
        "duration_sec": random.uniform(8.0, 15.0),
        "bpm": random.randint(80, 160),
        "key": random.choice(keys),
        "genre": random.choice(genres),
        "mood": random.choice(moods),
        "time_signature": "4/4"
    }


def generate_note_sequence(duration_sec, bpm, key, genre):
    """生成音符序列"""
    notes = []

    # 根据流派确定音符生成规则
    if genre == "pop":
        # 流行音乐：简单和弦进行
        chords = [
            [60, 64, 67],  # C major
            [62, 65, 69],  # D minor
            [59, 62, 67],  # G major
            [60, 64, 67],  # C major
        ]
        note_duration = 1.0  # 1小节

    elif genre == "classical":
        # 古典音乐：琶音模式
        chords = [
            [60, 64, 67],  # C major arpeggio
            [62, 65, 69],  # D minor arpeggio
        ]
        note_duration = 0.25  # 16分音符

    elif genre == "jazz":
        # 爵士音乐：七和弦
        chords = [
            [60, 64, 67, 70],  # C major 7
            [62, 65, 69, 72],  # D minor 7
        ]
        note_duration = 0.5  # 8分音符

    else:  # rock
        # 摇滚音乐：强力和弦
        chords = [
            [60, 67],  # C5 power chord
            [62, 69],  # D5 power chord
        ]
        note_duration = 0.5

    # 生成音符
    current_time = 0.0
    beat_duration = 60.0 / bpm  # 每拍时长

    while current_time < duration_sec:
        # 选择和弦
        chord = random.choice(chords)

        # 生成和弦中的音符
        for pitch in chord:
            if current_time + note_duration <= duration_sec:
                notes.append({
                    "pitch": pitch,
                    "start": round(current_time, 2),
                    "duration": round(note_duration, 2),
                    "velocity": random.randint(70, 90)
                })

        current_time += note_duration

    return notes


def extract_audio_features(notes, duration_sec, bpm, genre):
    """提取音频特征（模拟）"""
    # MFCC特征 (13维均值)
    mfcc_means = np.random.randn(13) * 0.5 + np.random.rand(13)

    # Chroma特征 (12维)
    chroma = np.random.rand(12)

    # 频谱对比度 (7维)
    spectral_contrast = np.random.rand(7)

    # 节奏特征
    tempo_features = {
        "tempo_confidence": random.uniform(0.7, 1.0),
        "beat_count": int(duration_sec * bpm / 60)
    }

    return {
        "mfcc_mean_1": float(mfcc_means[0]),
        "mfcc_mean_2": float(mfcc_means[1]),
        "mfcc_mean_3": float(mfcc_means[2]),
        "mfcc_mean_4": float(mfcc_means[3]),
        "mfcc_mean_5": float(mfcc_means[4]),
        "mfcc_mean_6": float(mfcc_means[5]),
        "mfcc_mean_7": float(mfcc_means[6]),
        "mfcc_mean_8": float(mfcc_means[7]),
        "mfcc_mean_9": float(mfcc_means[8]),
        "mfcc_mean_10": float(mfcc_means[9]),
        "mfcc_mean_11": float(mfcc_means[10]),
        "mfcc_mean_12": float(mfcc_means[11]),
        "mfcc_mean_13": float(mfcc_means[12]),

        "chroma_1": float(chroma[0]),
        "chroma_2": float(chroma[1]),
        "chroma_3": float(chroma[2]),
        "chroma_4": float(chroma[3]),
        "chroma_5": float(chroma[4]),
        "chroma_6": float(chroma[5]),
        "chroma_7": float(chroma[6]),
        "chroma_8": float(chroma[7]),
        "chroma_9": float(chroma[8]),
        "chroma_10": float(chroma[9]),
        "chroma_11": float(chroma[10]),
        "chroma_12": float(chroma[11]),

        "spectral_contrast_1": float(spectral_contrast[0]),
        "spectral_contrast_2": float(spectral_contrast[1]),
        "spectral_contrast_3": float(spectral_contrast[2]),
        "spectral_contrast_4": float(spectral_contrast[3]),
        "spectral_contrast_5": float(spectral_contrast[4]),
        "spectral_contrast_6": float(spectral_contrast[5]),
        "spectral_contrast_7": float(spectral_contrast[6]),

        "tempo_confidence": tempo_features["tempo_confidence"],
        "beat_count": tempo_features["beat_count"],
        "zero_crossing_rate": random.uniform(0.01, 0.1),
        "spectral_centroid": random.uniform(1000, 4000),
        "spectral_bandwidth": random.uniform(2000, 8000),
        "spectral_rolloff": random.uniform(3000, 8000)
    }


def create_splits(segment_ids):
    """创建训练/验证/测试拆分"""
    random.shuffle(segment_ids)

    n = len(segment_ids)
    n_train = int(0.7 * n)
    n_val = int(0.15 * n)

    train_ids = segment_ids[:n_train]
    val_ids = segment_ids[n_train:n_train + n_val]
    test_ids = segment_ids[n_train + n_val:]

    return train_ids, val_ids, test_ids


def save_splits(train_ids, val_ids, test_ids):
    """保存拆分到文件"""
    splits_dir = Path("splits")
    splits_dir.mkdir(exist_ok=True)

    with open(splits_dir / "train_ids.txt", "w") as f:
        for sid in train_ids:
            f.write(f"{sid}\n")

    with open(splits_dir / "val_ids.txt", "w") as f:
        for sid in val_ids:
            f.write(f"{sid}\n")

    with open(splits_dir / "test_ids.txt", "w") as f:
        for sid in test_ids:
            f.write(f"{sid}\n")

    print(f"Saved splits: train={len(train_ids)}, val={len(val_ids)}, test={len(test_ids)}")


def generate_dataset(num_segments=50):
    """生成完整数据集"""
    print(f"Generating {num_segments} music segments...")

    csv_data = []
    jsonl_data = []
    segment_ids = []

    for i in range(num_segments):
        segment_id = generate_segment_id(i + 1)
        segment_ids.append(segment_id)

        # 生成音乐参数
        params = generate_music_parameters()

        # 生成音符序列
        notes = generate_note_sequence(
            params["duration_sec"],
            params["bpm"],
            params["key"],
            params["genre"]
        )

        # 提取音频特征
        features = extract_audio_features(
            notes,
            params["duration_sec"],
            params["bpm"],
            params["genre"]
        )

        # 创建CSV行
        csv_row = {
            "segment_id": segment_id,
            "duration_sec": round(params["duration_sec"], 2),
            "bpm": params["bpm"],
            "key": params["key"],
            "genre": params["genre"],
            "mood": params["mood"],
            "time_signature": params["time_signature"]
        }

        # 添加音频特征
        csv_row.update(features)
        csv_data.append(csv_row)

        # 创建JSONL对象
        jsonl_obj = {
            "segment_id": segment_id,
            "notes": notes,
            "time_signature": params["time_signature"],
            "tempo_changes": [
                {"time": 0.0, "bpm": params["bpm"]}
            ]
        }
        jsonl_data.append(jsonl_obj)

        print(f"  Generated {segment_id}: {params['genre']} {params['mood']} {params['bpm']}BPM")

    # 创建数据目录
    data_dir = Path("raw")
    data_dir.mkdir(exist_ok=True)

    # 保存CSV文件
    csv_path = data_dir / "audio_features.csv"
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV to {csv_path}")

    # 保存JSONL文件
    jsonl_path = data_dir / "note_sequences.jsonl"
    with open(jsonl_path, "w") as f:
        for obj in jsonl_data:
            f.write(json.dumps(obj) + "\n")
    print(f"Saved JSONL to {jsonl_path}")

    # 创建数据拆分
    train_ids, val_ids, test_ids = create_splits(segment_ids)
    save_splits(train_ids, val_ids, test_ids)

    # 创建数据统计报告
    create_data_report(df, segment_ids)

    return df, jsonl_data


def create_data_report(df, segment_ids):
    """创建数据统计报告"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    # 基础统计
    stats = {
        "generation_date": datetime.now().isoformat(),
        "total_segments": len(df),
        "duration_stats": {
            "min": float(df["duration_sec"].min()),
            "max": float(df["duration_sec"].max()),
            "mean": float(df["duration_sec"].mean()),
            "std": float(df["duration_sec"].std())
        },
        "bpm_stats": {
            "min": int(df["bpm"].min()),
            "max": int(df["bpm"].max()),
            "mean": float(df["bpm"].mean())
        },
        "genre_distribution": df["genre"].value_counts().to_dict(),
        "mood_distribution": df["mood"].value_counts().to_dict(),
        "key_distribution": df["key"].value_counts().to_dict(),
        "segment_ids": segment_ids
    }

    # 保存报告
    report_path = report_dir / "data_generation_report.json"
    with open(report_path, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"Saved data report to {report_path}")

    # 打印摘要
    print("\n" + "=" * 60)
    print("DATA GENERATION SUMMARY")
    print("=" * 60)
    print(f"Total segments: {stats['total_segments']}")
    print(f"Duration: {stats['duration_stats']['min']:.1f}-{stats['duration_stats']['max']:.1f} sec")
    print(f"BPM range: {stats['bpm_stats']['min']}-{stats['bpm_stats']['max']}")
    print(f"Genres: {stats['genre_distribution']}")
    print(f"Moods: {stats['mood_distribution']}")
    print(f"Keys: {stats['key_distribution']}")

    return stats


def main():
    """主函数"""
    print("=" * 60)
    print("MUSIC SEGMENT GENERATION - HW3")
    print("=" * 60)

    # 生成20个音乐片段
    df, jsonl_data = generate_dataset(20)

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)
    print("\nFiles created:")
    print("1. data/audio_features.csv - 音频特征数据")
    print("2. data/note_sequences.jsonl - 音符序列数据")
    print("3. data/splits/ - 数据拆分文件")
    print("4. reports/data_generation_report.json - 数据统计报告")

    print("\nNext steps:")
    print("1. Run data quality checks: python -m pytest tests/test_data_checks.py")
    print("2. Initialize DVC: dvc init")
    print("3. Add data to DVC: dvc add data/audio_features.csv data/note_sequences.jsonl")
    print("4. Commit to Git: git add . && git commit -m 'HW3: Generated music data'")


if __name__ == "__main__":
    main()