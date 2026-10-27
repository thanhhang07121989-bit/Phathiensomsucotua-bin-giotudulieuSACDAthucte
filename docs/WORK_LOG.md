# Nhật ký công việc nhóm

| Ngày | Người phụ trách | Việc đã làm | File thay đổi | Kết quả / vấn đề | Việc tiếp theo |
|---|---|---|---|---|---|

- [x] Ngay 3: Da hoan thanh kiem ke file 84.csv (53,772 dong, 86 cot, 2 gia tri NULL).
- [x] Ngày 4: Xác minh schema thực tế (time_stamp, asset_id, status_type_id), đồng bộ project.yaml và ghi nhận cơ chế nhãn khoảng thời gian từ event_info.csv.



### Chi tiet kiem dinh du lieu mau Ngay 5 (sample_84.csv)
- Kich thuoc tap mau: 5000 dong, 86 cot
- Khoang thoi gian: Tu 2022-09-02 15:30:00 den 2022-10-07 12:20:00
- Ban ghi trung lap thoi gian: 0 ban ghi
- Tan suat ghi nhan (Mode): 0 days 00:10:00
- So cot hang so (nunique <= 1): 4 cot ['asset_id', 'train_test', 'sensor_46', 'sensor_49']
- Bieu do chuoi thoi gian: reports/figures/eda_sample_84.png


- Ngay 4: Da chay check_day4.py (Wind Farm A: 22 file, 5 tuabin; 84.csv 53772 dong, id 0..53771), xac minh nhan chi la khoang trong event_info, doi chieu bang id, cap nhat DATA_DICTIONARY.md va project.yaml.
