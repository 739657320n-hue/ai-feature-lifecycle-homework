#!/usr/bin/env python3
"""
数据质量检查 - 音乐生成项目
包含至少10个检查：3个语法 + 4个结构 + 3个统计
"""

import pandas as pd
import json
import numpy as np
import os
import re
from pathlib import Path


class TestDataQuality:
    """数据质量测试类"""

    @classmethod
    def setup_class(cls):
        """测试前准备"""
        print("\n" + "=" * 60)
        print("DATA QUALITY CHECKS - Music Generation Dataset")
        print("=" * 60)

        # 加载数据
        cls.csv_path = Path("../data/raw/audio_features.csv")
        cls.jsonl_path = Path("../data/raw/note_sequences.jsonl")
        cls.splits_dir = Path("../data/splits")

        cls.df = pd.read_csv(cls.csv_path)
        cls.segment_ids = cls.df["segment_id"].tolist()

        # 加载JSONL数据
        cls.jsonl_data = []
        with open(cls.jsonl_path, "r") as f:
            for line in f:
                cls.jsonl_data.append(json.loads(line.strip()))

    def test_01_csv_file_exists(self):
        """语法检查1: CSV文件存在且非空"""
        assert self.csv_path.exists(), "CSV文件不存在"
        assert os.path.getsize(self.csv_path) > 0, "CSV文件为空"
        print("✓ CSV文件存在且非空")

    def test_02_jsonl_file_exists(self):
        """语法检查2: JSONL文件存在且非空"""
        assert self.jsonl_path.exists(), "JSONL文件不存在"
        assert os.path.getsize(self.jsonl_path) > 0, "JSONL文件为空"
        print("✓ JSONL文件存在且非空")

    def test_03_csv_format_correct(self):
        """语法检查3: CSV格式正确"""
        # 检查必需的列
        required_columns = [
            "segment_id", "duration_sec", "bpm", "key",
            "genre", "mood", "time_signature"
        ]

        for col in required_columns:
            assert col in self.df.columns, f"缺少必需列: {col}"

        # 检查行数
        assert len(self.df) == 20, f"CSV应有20行，实际有{len(self.df)}行"

        print("✓ CSV格式正确")

    def test_04_no_missing_values(self):
        """结构检查1: 无缺失值"""
        # 检查CSV中的缺失值
        missing_counts = self.df.isnull().sum()
        total_missing = missing_counts.sum()

        assert total_missing == 0, f"发现缺失值: {missing_counts[missing_counts > 0].to_dict()}"

        # 检查JSONL中的缺失值
        for item in self.jsonl_data:
            assert "segment_id" in item, "JSONL缺少segment_id"
            assert "notes" in item, "JSONL缺少notes"
            assert len(item["notes"]) > 0, "JSONL的notes数组为空"

        print("✓ 无缺失值")

    def test_05_segment_id_format(self):
        """结构检查2: segment_id格式正确"""
        # 检查CSV中的segment_id格式
        pattern = r"^seg_\d{3}$"
        for seg_id in self.df["segment_id"]:
            assert re.match(pattern, seg_id), f"segment_id格式错误: {seg_id}"

        # 检查JSONL中的segment_id格式
        for item in self.jsonl_data:
            seg_id = item["segment_id"]
            assert re.match(pattern, seg_id), f"JSONL中segment_id格式错误: {seg_id}"

        print("✓ segment_id格式正确")

    def test_06_no_duplicate_segment_ids(self):
        """结构检查3: 无重复segment_id"""
        # 检查CSV中的重复
        duplicate_ids = self.df[self.df.duplicated(["segment_id"])]["segment_id"].tolist()
        assert len(duplicate_ids) == 0, f"发现重复segment_id: {duplicate_ids}"

        # 检查JSONL中的重复
        jsonl_ids = [item["segment_id"] for item in self.jsonl_data]
        assert len(jsonl_ids) == len(set(jsonl_ids)), "JSONL中发现重复segment_id"

        print("✓ 无重复segment_id")

    def test_07_cross_file_consistency(self):
        """结构检查4: 跨文件一致性"""
        # 检查CSV和JSONL中的segment_id一致
        csv_ids = set(self.df["segment_id"])
        jsonl_ids = set(item["segment_id"] for item in self.jsonl_data)

        assert csv_ids == jsonl_ids, f"CSV和JSONL中的segment_id不一致"

        # 检查每个segment_id的数据一致性
        for seg_id in csv_ids:
            csv_row = self.df[self.df["segment_id"] == seg_id].iloc[0]
            jsonl_item = next(item for item in self.jsonl_data if item["segment_id"] == seg_id)

            # 检查时长一致性（允许微小差异）
            csv_duration = csv_row["duration_sec"]

            # 计算JSONL中的最大结束时间
            if jsonl_item["notes"]:
                max_end_time = max(note["start"] + note["duration"] for note in jsonl_item["notes"])
                # 允许0.5秒差异
                assert abs(csv_duration - max_end_time) <= 0.5, \
                    f"{seg_id}: CSV时长{csv_duration}与JSONL最大结束时间{max_end_time}不一致"

        print("✓ 跨文件一致性检查通过")

    def test_08_note_sequence_validity(self):
        """语法扩展检查: 音符序列有效性"""
        invalid_notes = []

        for item in self.jsonl_data:
            seg_id = item["segment_id"]
            notes = item["notes"]

            for i, note in enumerate(notes):
                # 检查音高范围
                if not (0 <= note["pitch"] <= 127):
                    invalid_notes.append(f"{seg_id}-note{i}: 音高超出范围 {note['pitch']}")

                # 检查开始时间
                if note["start"] < 0:
                    invalid_notes.append(f"{seg_id}-note{i}: 开始时间为负 {note['start']}")

                # 检查时长
                if note["duration"] <= 0:
                    invalid_notes.append(f"{seg_id}-note{i}: 时长非正 {note['duration']}")

                # 检查力度
                if not (0 <= note["velocity"] <= 127):
                    invalid_notes.append(f"{seg_id}-note{i}: 力度超出范围 {note['velocity']}")

        assert len(invalid_notes) == 0, f"发现无效音符: {invalid_notes}"
        print("✓ 音符序列有效性检查通过")

    def test_09_genre_distribution(self):
        """统计检查1: 流派分布合理"""
        genre_counts = self.df["genre"].value_counts()

        # 检查是否有流派完全缺失
        expected_genres = ["pop", "classical", "jazz", "rock"]
        for genre in expected_genres:
            assert genre in genre_counts.index, f"流派缺失: {genre}"

        # 检查分布相对平衡（每个流派至少有2个样本）
        min_samples = 2
        for genre, count in genre_counts.items():
            assert count >= min_samples, f"流派{genre}样本太少: {count}"

        print(f"✓ 流派分布合理: {genre_counts.to_dict()}")

    def test_10_bpm_range_validity(self):
        """统计检查2: BPM范围合理"""
        bpm_values = self.df["bpm"]

        # 检查范围
        assert bpm_values.min() >= 40, f"BPM过低: {bpm_values.min()}"
        assert bpm_values.max() <= 200, f"BPM过高: {bpm_values.max()}"

        # 检查多样性（至少有3个不同的BPM值）
        unique_bpms = bpm_values.nunique()
        assert unique_bpms >= 3, f"BPM多样性不足: 只有{unique_bpms}个不同值"

        print(f"✓ BPM范围合理: {bpm_values.min()}-{bpm_values.max()}")

    def test_11_duration_distribution(self):
        """统计检查3: 时长分布合理"""
        durations = self.df["duration_sec"]

        # 检查范围
        assert durations.min() >= 5.0, f"片段太短: {durations.min()}秒"
        assert durations.max() <= 30.0, f"片段太长: {durations.max()}秒"

        # 检查平均值在合理范围
        mean_duration = durations.mean()
        assert 8.0 <= mean_duration <= 15.0, f"平均时长异常: {mean_duration:.1f}秒"

        print(f"✓ 时长分布合理: {durations.min():.1f}-{durations.max():.1f}秒, 平均{mean_duration:.1f}秒")

    def test_12_splits_exist_and_valid(self):
        """结构扩展检查: 拆分文件存在且有效"""
        split_files = ["train_ids.txt", "val_ids.txt", "test_ids.txt"]

        for filename in split_files:
            file_path = self.splits_dir / filename
            assert file_path.exists(), f"拆分文件不存在: {filename}"

            with open(file_path, "r") as f:
                ids = [line.strip() for line in f if line.strip()]
                assert len(ids) > 0, f"拆分文件为空: {filename}"

                # 检查ID格式
                for seg_id in ids:
                    assert re.match(r"^seg_\d{3}$", seg_id), f"拆分文件中ID格式错误: {seg_id}"

        print("✓ 拆分文件存在且有效")

    def test_13_no_data_leakage(self):
        """结构扩展检查: 无数据泄漏"""
        # 加载拆分
        splits = {}
        for split_name in ["train", "val", "test"]:
            file_path = self.splits_dir / f"{split_name}_ids.txt"
            with open(file_path, "r") as f:
                splits[split_name] = [line.strip() for line in f if line.strip()]

        # 检查无重叠
        train_set = set(splits["train"])
        val_set = set(splits["val"])
        test_set = set(splits["test"])

        assert len(train_set & val_set) == 0, "训练集和验证集有重叠"
        assert len(train_set & test_set) == 0, "训练集和测试集有重叠"
        assert len(val_set & test_set) == 0, "验证集和测试集有重叠"

        # 检查覆盖所有segment_id
        all_split_ids = train_set | val_set | test_set
        all_csv_ids = set(self.segment_ids)

        assert all_split_ids == all_csv_ids, "拆分未覆盖所有segment_id"

        print("✓ 无数据泄漏")

    def test_14_feature_value_ranges(self):
        """统计扩展检查: 特征值范围合理"""
        # 检查音频特征范围
        mfcc_cols = [col for col in self.df.columns if "mfcc_mean" in col]
        for col in mfcc_cols:
            values = self.df[col]
            assert values.abs().max() < 10, f"MFCC特征{col}值过大: {values.abs().max()}"

        chroma_cols = [col for col in self.df.columns if "chroma" in col]
        for col in chroma_cols:
            values = self.df[col]
            assert values.min() >= 0, f"Chroma特征{col}有负值: {values.min()}"
            assert values.max() <= 1, f"Chroma特征{col}超过1: {values.max()}"

        print("✓ 特征值范围合理")


def run_all_tests():
    """运行所有测试并生成报告"""
    import sys

    test_instance = TestDataQuality()
    test_instance.setup_class()

    test_methods = [
        "test_01_csv_file_exists",
        "test_02_jsonl_file_exists",
        "test_03_csv_format_correct",
        "test_04_no_missing_values",
        "test_05_segment_id_format",
        "test_06_no_duplicate_segment_ids",
        "test_07_cross_file_consistency",
        "test_08_note_sequence_validity",
        "test_09_genre_distribution",
        "test_10_bpm_range_validity",
        "test_11_duration_distribution",
        "test_12_splits_exist_and_valid",
        "test_13_no_data_leakage",
        "test_14_feature_value_ranges"
    ]

    passed = []
    failed = []

    print("\n" + "=" * 60)
    print("RUNNING DATA QUALITY CHECKS")
    print("=" * 60)

    for method_name in test_methods:
        try:
            method = getattr(test_instance, method_name)
            method()
            passed.append(method_name)
            print(f"  ✓ {method_name}")
        except AssertionError as e:
            failed.append((method_name, str(e)))
            print(f"  ✗ {method_name}: {e}")
        except Exception as e:
            failed.append((method_name, f"Unexpected error: {e}"))
            print(f"  ✗ {method_name}: Unexpected error")

    # 生成报告
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(test_methods)}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed tests:")
        for method_name, error in failed:
            print(f"  - {method_name}: {error}")

        print("\n" + "=" * 60)
        print("DATA QUALITY CHECK FAILED")
        print("=" * 60)
        sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("ALL DATA QUALITY CHECKS PASSED!")
        print("=" * 60)

        # 保存测试报告
        report = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "total_tests": len(test_methods),
            "passed_tests": len(passed),
            "failed_tests": len(failed),
            "test_results": {
                "passed": passed,
                "failed": [{"test": name, "error": error} for name, error in failed]
            }
        }

        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / "data_quality_report.json"

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Report saved to {report_path}")


if __name__ == "__main__":
    run_all_tests()