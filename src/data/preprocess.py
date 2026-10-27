"""
Ngày 6 - Step 2: Preprocessing Pipeline
Chạy: python -m src.data.preprocess
"""
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = PROJECT_ROOT / "data" / "sample" / "sample_84.csv"
OUT_DIR = PROJECT_ROOT / "data" / "processed"

# Cột khóa/nhãn: không bao giờ bị xét là "cột hằng số"
PROTECTED = {"asset_id", "id", "time_stamp", "datetime",
             "train_test", "status_type_id"}


def preprocess_scada(input_path: Path, output_dir: Path) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    log = {"input": str(input_path),
           "run_at": datetime.now().isoformat(timespec="seconds")}

    df = pd.read_csv(input_path, sep=";")
    log["rows_initial"] = int(len(df))
    log["cols_initial"] = int(df.shape[1])

    # 1. Parse datetime, loại dòng timestamp lỗi
    df["datetime"] = pd.to_datetime(df["time_stamp"], errors="coerce")
    n_bad_t = int(df["datetime"].isna().sum())
    df = df.dropna(subset=["datetime"])
    log["rows_dropped_bad_timestamp"] = n_bad_t

    # 2. Sắp xếp tăng dần theo thời gian
    df = df.sort_values(["asset_id", "datetime", "id"]).reset_index(drop=True)

    # 3. Loại trùng theo khóa, rồi theo mốc thời gian
    n0 = len(df)
    df = df.drop_duplicates(subset=["asset_id", "id"], keep="first")
    n1 = len(df)
    df = df.drop_duplicates(subset=["asset_id", "datetime"], keep="first")
    n2 = len(df)
    log["rows_dropped_duplicate_key"] = int(n0 - n1)
    log["rows_dropped_duplicate_time"] = int(n1 - n2)
    log["rows_dropped_duplicates"] = int(n0 - n2)

    # 4. Cột hằng số: chỉ xét trên TRAIN (chống leakage), rồi áp dụng cho cả tập
    split = df["train_test"].astype(str).str.strip().str.lower()
    print(f"- Giá trị train_test: {sorted(split.unique())}")
    train_mask = split == "train"
    if not train_mask.any():
        raise ValueError(
            f"Không có dòng train. Giá trị hiện có: {sorted(split.unique())}")
    log["rows_train"] = int(train_mask.sum())
    log["rows_prediction"] = int((~train_mask).sum())

    candidates = [c for c in df.columns if c not in PROTECTED]
    const_cols = [c for c in candidates
                  if df.loc[train_mask, c].nunique(dropna=True) <= 1]
    df = df.drop(columns=const_cols)
    log["constant_cols_dropped"] = const_cols
    print(f"- Cột hằng số (xét trên Train) đã loại: {const_cols}")

    # 5. Ghi nhận tỷ lệ thiếu (CHƯA điền: thống kê điền phải lấy từ train ở giai đoạn sau)
    miss = df.isna().mean().round(4)
    log["missing_ratio_by_col"] = {k: float(v) for k, v in miss.items() if v > 0}

    # 6. Lưu dữ liệu + nhật ký
    log["rows_final"] = int(len(df))
    log["cols_final"] = int(df.shape[1])
    log["rows_dropped_total"] = log["rows_initial"] - log["rows_final"]

    out_file = output_dir / "clean_sample_84.parquet"
    df.to_parquet(out_file, index=False)
    log_file = output_dir / "preprocess_log_sample_84.json"
    log_file.write_text(json.dumps(log, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    print(f"- Dòng: {log['rows_initial']} -> {log['rows_final']} "
          f"(loại {log['rows_dropped_total']})")
    print(f"- Cột:  {log['cols_initial']} -> {log['cols_final']}")
    print(f"✅ Đã lưu dữ liệu: {out_file}")
    print(f"✅ Đã lưu nhật ký: {log_file}")
    return df


if __name__ == "__main__":
    preprocess_scada(SAMPLE_PATH, OUT_DIR)