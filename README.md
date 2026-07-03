# 📊 🌐 Đo Lường Khoảng Trống AI: Đánh Giá Năng Lực Tự Động Hóa Và Nhu Cầu Của Người Lao Động Trong Khối Ngành Khoa Học Máy Tính

Ứng dụng web trực quan hóa dữ liệu được xây dựng trên nền tảng **Streamlit** nhằm hỗ trợ các nhà quản lý, kỹ sư công nghệ và chuyên gia AI có góc nhìn sâu sắc về nhu cầu thực tế của người lao động đối lập với năng lực công nghệ hiện tại trong ngành Khoa học Máy tính. Từ đó, hệ thống đưa ra các giải pháp cấu hình **AI Agent** tối ưu nhất cho từng vị trí công việc chuyên biệt, giúp tối ưu hóa ROI và quản trị rủi ro nhân sự.

---

## 📂 Dataset

Ứng dụng xử lý bộ dữ liệu đa chiều liên kết giữa hành vi con người và năng lực công nghệ:

| File | Nội dung | Records | Trạng thái trong Code |
|------|----------|---------|-----------------------|
| `domain_worker_desires.csv` | Worker tự đánh giá mong muốn tự động hóa cho từng task | 5,731 tasks | **Đang sử dụng**  |
| `domain_worker_metadata.csv` | Thông tin nhân khẩu học và thái độ về AI của worker | 1,500 workers | **Đang sử dụng** |
| `expert_rated_technological_capability.csv` | Chuyên gia đánh giá khả năng tự động hóa của task | 2,057 tasks | **Đang sử dụng** |
| `task_statement_with_metadata.csv` | O*NET task metadata (tần suất, tầm quan trọng, skill) | ~1,200+ tasks | **Đang sử dụng** |

---

## 🚀 Các Tính Năng Chính Của Ứng Dụng

Hệ thống phân tích chuyên sâu **13 ngành nghề trọng điểm** thuộc khối Khoa học Máy tính (CS Roles) và được chia làm 4 phân hệ chính điều hướng qua Sidebar:

### 2. Phân tích Độ Lệch (Gap Analysis)
* Toán học hóa tâm lý bằng công thức: **`Gap = Điểm khao khát (Desire) - Điểm năng lực AI (Capacity)`**.
* **Nhóm Đỏ (Gap < 0):** Vùng e dè. AI dư sức làm nhưng nhân sự từ chối giao phó.
* **Nhóm Xanh (Gap > 0):** Vùng chờ đợi. Nhân sự quá tải, khao khát AI vượt xa năng lực công nghệ hiện tại.

### 3. Phân tích Chuyên Sâu (CS Deep Dive)
* Lọc dữ liệu theo cụm **Nghề nghiệp** và **Số năm kinh nghiệm**.
* **Dynamic UI (Giao diện động):** Thuật toán tự động nhận diện điểm Gap để thay đổi giao diện hiển thị:
    * *Gap > 0.5:* Chỉ hiển thị biểu đồ Động lực.
    * *Gap < -0.5:* Chỉ hiển thị biểu đồ Nỗi lo / Rào cản.
    * *-0.5 <= Gap <= 0.5:* Hiển thị đối trọng cả hai biểu đồ.

### 4. Đề xuất AI Agent Tự Động (Actionable Recommendations)
* Kế thừa dữ liệu từ bộ lọc bằng `st.session_state` để tự động hóa quy trình đề xuất.
* Dựa vào chỉ số Gap, hệ thống tự động "kê đơn":
    * **Gap > 0.5:** Đề xuất mô hình **Autonomous Co-pilot** (Cấp quyền tối đa để giải phóng sức lao động).
    * **Gap < -0.5:** Đề xuất mô hình **Review & Compliance Agent** (Áp dụng chiến lược Human-in-the-loop, AI chỉ làm nháp, con người phê duyệt).
    * **Cân bằng:** Đề xuất **Guidance & Guardrail Agent** (Hướng dẫn từng bước).
---

## 🛠️ Công Nghệ Sử Dụng 
* **Ngôn ngữ:** Python 3
* **Framework:** Streamlit (Xây dựng UI/UX và tương tác web)
* **Xử lý dữ liệu:** Pandas
* **Trực quan hóa:** Plotly Express, Plotly Graph Objects
---

## 💻 Hướng dẫn Cài đặt & Khởi chạy

### 1. Chuẩn bị môi trường
Hãy đảm bảo bạn đã cài đặt các thư viện cần thiết:
```bash
pip install streamlit pandas plotly