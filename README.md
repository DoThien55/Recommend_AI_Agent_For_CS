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

* **1. Tổng quan (Overview):** 
  * Hiển thị thống kê nhanh số lượng mẫu và số ngành IT.
  * Trực quan hóa **Top lý do muốn dùng AI** (Giải phóng thời gian, xử lý data lớn...) và **Top rào cản tâm lý** (Cần người duyệt chất lượng, trách nhiệm đạo đức/pháp lý...).
* **2. Phân tích Độ Lệch (Gap Analysis):** 
  * Tính toán chỉ số lệch bằng công thức $Gap = \text{Worker Desire} - \text{Expert Capacity}$.
* **3. Phân tích Chuyên Sâu (CS Deep Dive):** 
  * Tự động phân loại nhóm hành vi (*Nhóm Cẩn Thận, Nhóm Mệt Mỏi, Nhóm Cân Bằng*) để đưa ra lời khuyên quản trị nhân sự thực tế.
* **4. Đề xuất AI Agent:**
  * Khuyến nghị tự động cấu hình các AI Agent chuyên biệt phù hợp cho từng vị trí (Ví dụ: `Code Review Agent` cho Lập trình viên, `Self-healing Agent` cho SRE...) nhằm tối ưu hóa hiệu suất làm việc.

---

## 🛠️ Công nghệ & Tối ưu 

* **Framework & Thư viện:** `Python 3.11+`, `Streamlit`, `Pandas`, `Plotly Express` & `Graph Objects`.
* **Cơ chế An toàn dữ liệu:** Tích hợp bọc `try-except` thông minh khi đọc file CSV. Thông báo lỗi UI an toàn thay vì crash ứng dụng.
* **Tối ưu hiển thị:** Nhúng mã CSS trực tiếp để tối ưu hóa trải nghiệm trên màn hình lớn/máy chiếu (Chữ văn bản: **22px**, Tiêu đề: **30px**, Metric: **45px Bold**).

---

## 💻 Hướng dẫn Cài đặt & Khởi chạy

### 1. Chuẩn bị môi trường
Hãy đảm bảo bạn đã cài đặt các thư viện cần thiết:
```bash
pip install streamlit pandas plotly