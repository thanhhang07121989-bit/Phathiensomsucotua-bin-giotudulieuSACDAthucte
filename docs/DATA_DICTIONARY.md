# Data dictionary (điền sau khi kiểm tra dataset)

## Nguyên tắc
Không tự đặt tên cột. Hãy ghi chính xác tên cột xuất hiện trong file thực tế, đơn vị, kiểu dữ liệu, ý nghĩa và tỷ lệ thiếu.

| Tên cột thực tế | Ý nghĩa | Kiểu dữ liệu | Đơn vị | Thiếu (%) | Được dùng làm feature? | Ghi chú |
|---|---|---|---|---:|---|---|
| Điền sau khi inspect | | | | | | |

## Những trường cần tìm và xác nhận
- Thời gian (timestamp)
- Mã tua-bin / tài sản (asset ID)
- Trường trạng thái vận hành (status)
- Trường phân chia train / prediction nếu có
- Các cảm biến và phép đo SCADA
- Nhãn hoặc khoảng thời gian sự kiện bất thường, nếu được cung cấp

Không dùng timestamp, asset ID, status ID, row ID hoặc thông tin nhãn làm đầu vào mô hình như cảm biến. Không giả định tên cột chính xác trước khi xem file.

## SCADA Telemetry (84.csv) & Events (Xác minh Ngày 4)
- time_stamp: Thoi gian ghi nhan chuoi SCADA (10 phut/ban ghi)
- asset_id: Ma dinh danh tua-bin gio
- status_type_id: Ma trang thai van hanh
- power_29_avg: Cong suat phat trung binh

- wind_speed_3_avg: Tốc độ gió trung bình
- Event Labels: Nhãn sự cố lưu theo khoảng (event_start_id -> event_end_id) trong event_info.csv

## Ghi chu kiem dinh thuc te Ngay 5 (Tep sample_84.csv / Asset 13)
- **Asset ID & Tan suat**: File 84 thuoc asset_id = 13. Tan suat ghi 10 phut/ban ghi, chuoi thoi gian da duoc sap xep, khong trung timestamp.
- **Khoang trong thoi gian (Gap)**: Phat hien 1 khoảng trong 3h50m (mat ~22 ban ghi) -> Can luu y khi tao cua so trut (sliding window) o Ngay 7-8.
- **Ma trang thai (status_type_id)**: File 84 chua cac ma [0, 4, 5]; File 0 chua [0, 3, 5]. Can doi chieu README de ghi dung y nghia nghiep vu cua tung ma.
- **Cong suat (power_29_avg, power_30_avg)**: Gia tri nam trong [0, 0.98] -> Da duoc chuan hoa (Normalized [0, 1]), khong phai kW thieu chuan hoa.
- **Goc quay (sensor_1_avg, sensor_2_avg, sensor_42_avg)**: Gia tri goc co tinh chat chu ky (0 - 360 do / -177 den 180 do). Can ma hoa Sin/Cos hoac loai bo o Ngay 8.
- **Cot hang so (sensor_46, sensor_49)**: Mang gia tri khong doi trong tap sample 35 ngay. Giu nguyen, se quyet dinh loai bo o Ngay 8 tren toan bo tap Train.
- **Chat luong tong the**: Khong phat hien gia tri di biet kieu -9999.
