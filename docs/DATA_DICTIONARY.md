# Data dictionary (điền sau khi kiểm tra dataset)

## Nguyên tắc
Không tự đặt tên cột. Hãy ghi chính xác tên cột xuất hiện trong file thực tế, đơn vị, kiểu dữ liệu, ý nghĩa và tỷ lệ thiếu.

| Tên cột thực tế | Ý nghĩa | Kiểu dữ liệu | Đơn vị | Thiếu (%) | Được dùng làm feature? | Ghi chú |
|---|---|---|---|---:|---|---|
| time_stamp | Mốc thời gian ghi nhận SCADA (10 phút/bản ghi) | object | - | 0.0% | Không | Định danh thời gian, không đưa trực tiếp vào ML |
| asset_id | Mã định danh tuabin gió (Asset 13 cho file 84.csv) | int64 | - | 0.0% | Không | Cột hằng trong file 84.csv, dùng phân nhóm tuabin |
| status_type_id | Mã trạng thái vận hành tuabin | int64 | - | 0.0% | Không | 0: Normal, 1: Derated, 2: Idling, 3: Service, 4: Downtime, 5: Other |
| id | Chỉ số dòng liên tục (0 đến N-1) | int64 | - | 0.0% | Không | Khóa đối chiếu khoảng thời gian sự cố với event_info.csv |
| train_test | Phân định giai đoạn dữ liệu (train / prediction) | object | - | 0.0% | Không | Dùng phân chia tập huấn luyện và dự báo |
| power_30_avg | Grid power (Công suất phát thực tế lên lưới) | float64 | kW | 0.0% | Có | Feature công suất phát chính. Dải [0, 0.98] giả định chuẩn hóa |
| power_29_avg | Possible grid active power (Công suất phát khả dụng lý thuyết) | float64 | kW | 0.0% | Có | Feature công suất tiềm năng theo tốc độ gió |
| wind_speed_3_avg | Windspeed (Tốc độ gió trung bình đo tại tuabin) | float64 | m/s | 0.0% | Có | Feature tốc độ gió chính |
| sensor_1_avg | Wind absolute direction (Hướng gió tuyệt đối) | float64 | ° | 0.0% | Có | Cảm biến góc quay (0 - 360°) |
| sensor_2_avg | Wind relative direction (Hướng gió tương đối) | float64 | ° | 0.0% | Có | Cảm biến góc quay (0 - 360°) |
| sensor_42_avg | Nacelle direction (Hướng quay nacelle) | float64 | ° | 0.0% | Có | Cảm biến góc quay (0 - 360°) |
| ... (81 cột cảm biến) | Chi tiết 81 cột cảm biến tra cứu tại data_dictionary_draft.csv | float64 | - | 0.0% | Tùy cột | Danh sách 86 cột chi tiết lưu trong file nháp |

## Những trường cần tìm và xác nhận
- **Thời gian (timestamp)**: `time_stamp` (tần suất 10 phút/bản ghi, parse datetime chuẩn, đã sắp xếp tăng dần, không có dòng trùng).
- **Mã tua-bin / tài sản (asset ID)**: `asset_id` (định danh tuabin gió; file 84.csv thuộc `asset_id = 13`).
- **Trường trạng thái vận hành (status)**: `status_type_id` (ý nghĩa README: 0=Normal Operation, 1=Derated, 2=Idling, 3=Service, 4=Downtime, 5=Other).
- **Trường phân chia train / prediction**: `train_test` (file 84.csv có 52,335 dòng `train` và 1,437 dòng `prediction`).
- **Các cảm biến và phép đo SCADA**: 81 cột cảm biến số (`_avg`, `_max`, `_min`, `_std`).
- **Nhãn hoặc khoảng thời gian sự kiện bất thường**: Không có cột nhãn theo từng dòng trong file SCADA gốc. Nhãn sự cố lưu độc lập dưới dạng khoảng `event_start_id` -> `event_end_id` trong `event_info.csv`.

> **Lưu ý**: Không dùng `time_stamp`, `asset_id`, `status_type_id`, `id` (row ID) hoặc thông tin nhãn sự kiện làm đầu vào mô hình ML như biến cảm biến. Không giả định tên cột chính xác trước khi xem file.

## SCADA Telemetry (84.csv) & Events (Xác minh Ngày 4)
- **Nguồn dữ liệu Zenodo**: Zenodo record 14006163, phiên bản Zenodo v2 (Mã MD5 zip: `537A66BE609EA5CB471D0D759048E3A2`). Wind Farm A gồm 22 file dataset thuộc 5 tuabin (`0`, `10`, `11`, `13`, `21`).
- **time_stamp**: Thời gian ghi nhận chuỗi SCADA (tần suất 10 phút/bản ghi, từ 2022-09-02 đến 2023-09-12).
- **asset_id**: Mã định danh tuabin gió (file 84.csv thuộc `asset_id = 13`).
- **status_type_id**: Mã trạng thái vận hành tuabin (trong file 84.csv xuất hiện các mã 0, 3, 4, 5).
- **power_30_avg**: Grid power (Công suất phát thực tế lên lưới).
- **power_29_avg**: Possible grid active power (Công suất phát khả dụng lý thuyết).
- **wind_speed_3_avg**: Tốc độ gió trung bình đo tại nacelle.
- **sensor_1_avg, sensor_2_avg, sensor_42_avg**: Hướng gió tuyệt đối, hướng gió tương đối và hướng nacelle.
- **Event Labels**: Nhãn sự cố lưu theo khoảng (`event_start_id` -> `event_end_id`) trong `event_info.csv`. Đối chiếu trực tiếp bằng cột chỉ số dòng `id`.

## Ghi chú kiểm định thực tế Ngay 5 (Tep sample_84.csv / Asset 13)
- **Asset ID & Quy mô file 84**: File 84.csv thuộc `asset_id = 13`. Kích thước thực tế: **53,772 dòng** x **86 cột** (5 metadata + 81 cảm biến). Tần suất 10 phút/bản ghi, chuỗi thời gian đã được sắp xếp, parse lỗi = 0.
- **Lệch mốc thời gian (Timestamp Drift & Hạn chế)**: Mốc `time_stamp` thực tế tại dải `id` sự kiện 84 (52623 -> 53627) trong file 84.csv là `2023-09-04` đến `2023-09-11`, lệch **365 ngày** so với mốc ghi trong `event_info.csv` (`2022-09-04` đến `2022-09-11`). Bắt buộc đối chiếu sự cố bằng chỉ số `id`, không dùng `time_stamp`.
- **Khoảng trống thời gian (Gap)**: Phát hiện 15 khoảng trống thời gian lớn hơn 10 phút, lớn nhất là 12 giờ 20 phút.
- **Mã trạng thái (status_type_id)**: File 84.csv chứa các mã `0`, `3`, `4`, `5`.
- **Công suất (power_29_avg, power_30_avg)**: Giá trị nằm trong dải [0, 0.98] -> **Giả định** đã được chuẩn hóa min-max (Normalized), chưa rõ công thức chuẩn hóa chi tiết.
- **Góc quay (sensor_1_avg, sensor_2_avg, sensor_42_avg)**: Giá trị góc có tính chất chu kỳ (0 - 360 độ). Cần mã hóa Sin/Cos hoặc xem xét loại bỏ ở Ngày 8.
- **Cột hằng số (sensor_46, sensor_49)**: Mang giá trị không đổi trong file 84.csv (`asset_id`, `sensor_46`, `sensor_49`). Giữ nguyên, sẽ quyết định loại bỏ ở Ngày 8 trên toàn bộ tập Train.
- **Độ tin cậy chỉ số thống kê (Cảnh báo Zenodo)**: Chỉ các cột trung bình `_avg` là đủ độ tin cậy để dùng làm đặc trưng. Các cột `_min`, `_max`, `_std` có nhiều giá trị phi vật lý.