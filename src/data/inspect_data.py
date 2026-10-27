
"""
Ngày 6 - Step 1: Inspect Data Quality
Chạy: python -m src.data.inspect_data
"""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = PROJECT_ROOT / "data" / "sample" / "sample_84.csv"

REQUIRED_COLS = ["asset_id", "id", "time_stamp"]


def inspect_dataset(file_path: Path) -> None:
    print(f"=== Đang kiểm tra tệp: {file_path} ===")
    if not file_path.exists():
        print(f"❌ Không tìm thấy tệp {file_path}")
        return

    df = pd.read_csv(file_path, sep=";")

    # 1. Kích thước, cột, kiểu dữ liệu
    print(f"\n[1] Kích thước: {df.shape[0]} dòng x {df.shape[1]} cột")
    print("Cột và kiểu dữ liệu:")
    print(df.dtypes.to_string())

    missing_req = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing_req:
        print(f"❌ Thiếu cột bắt buộc: {missing_req}. Kiểm tra lại sep hoặc tên cột.")
        return

    # 2. Timestamp (kiểm tra thứ tự theo TỪNG turbine)
    t = pd.to_datetime(df["time_stamp"], errors="coerce")
    per_asset = t.groupby(df["asset_id"]).apply(lambda s: s.is_monotonic_increasing)
    print("\n[2] Timestamp")
    print(f"- Parse lỗi: {t.isna().sum()}")
    print(f"- Số turbine (asset_id): {df['asset_id'].nunique()}")
    print(f"- Số turbine có thời gian KHÔNG tăng dần: {(~per_asset).sum()}")
    print(f"- Mốc thời gian: {t.min()} --> {t.max()}")
    print("  (Nếu 'Parse lỗi' > 0 thì cờ tăng dần chưa phản ánh đúng thứ tự thời gian)")

    # 3. Trùng lặp
    dup_key = df.duplicated(subset=["asset_id", "id"]).sum()
    dup_time = df.duplicated(subset=["asset_id", "time_stamp"]).sum()
    print("\n[3] Trùng lặp")
    print(f"- Trùng khóa (asset_id, id): {dup_key}")
    print(f"- Trùng mốc thời gian (asset_id, time_stamp): {dup_time}")

    # 4. Phân bố train/prediction
    if "train_test" in df.columns:
        print("\n[4] Phân bố train_test")
        print(df["train_test"].value_counts(dropna=False).to_string())

    # 5. Missing theo từng cột
    report = pd.DataFrame({
        "null_rows": df.isna().sum(),
        "null_pct": (df.isna().mean() * 100).round(2),
    }).sort_values("null_pct", ascending=False)
    print("\n[5] Giá trị thiếu theo từng cột (giảm dần)")
    print(report.to_string())
    print(f"- Số cột có thiếu dữ liệu: {(report['null_rows'] > 0).sum()}/{len(report)}")


if __name__ == "__main__":
    inspect_dataset(SAMPLE_PATH)