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

## SCADA Telemetry (84.csv)
- time_stamp: Thoi gian ghi nhan chuoi SCADA (10 phut/ban ghi)
- asset_id: Ma dinh danh tua-bin gio
- status_type_id: Ma trang thai van hanh
- power_29_avg: Cong suat phat trung binh
- wind_speed_3_avg: Toc do gio trung binh
