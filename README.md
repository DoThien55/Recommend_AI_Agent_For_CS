# 📊  AI Agent trong Khoa học máy tính: Định hướng ứng dụng từ Phân tích độ lệch (Gap Analysis) giữa mong muốn con người và năng lực công nghệ.

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

### 1. Tổng quan (Overview): 
* Cung cấp bức tranh toàn cảnh về quy mô khảo sát (13 ngành nghề CS) và bóc tách các nhóm lý do cốt lõi thúc đẩy hoặc kìm hãm việc áp dụng AI.
### 2. Phân tích Độ Lệch (Gap Analysis)
* Toán học hóa tâm lý bằng công thức: **`Gap = Điểm khao khát (Desire) - Điểm năng lực AI (Capacity)`**.
* **Vùng E dè (Màu đỏ):** AI dư sức làm nhưng nhân sự từ chối giao phó.
* **Vùng Chờ đợi (Màu xanh):** Nhân sự quá tải, khao khát AI vượt xa năng lực công nghệ hiện tại.

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
```

## 🔄 Luồng Thực Thi Dự Án (Execution Architecture)

```text
[1. DỮ LIỆU ĐẦU VÀO]
      │
      ├─► domain_worker_desires.csv (Tâm lý khao khát & e dè)
      ├─► expert_rated_technological_capability.csv (Năng lực AI thực tế)
      ├─► domain_worker_metadata.csv (Nhân khẩu học & Kinh nghiệm)
      └─► task_statement_with_metadata.csv (Thông tin tác vụ)
      │
[2. TIỀN XỬ LÝ DỮ LIỆU]
      │
      ├─► Bộ lọc: Cô lập 13 ngành Khoa học máy tính (CS Roles)
      ├─► Gom cụm: Tính trung bình Điểm Mong muốn (Desire) & Điểm Năng lực (Capacity)
      └─► Thuật toán lõi: Tính GAP SCORE = Desire - Capacity
      │
[3. ĐIỀU HƯỚNG GIAO DIỆN (STREAMLIT APP)]
      │
      ├─► PHÂN HỆ 1: TỔNG QUAN
      │      └─ Thống kê Metrics & Biểu đồ Top lý do muốn/sợ AI toàn ngành
      │
      ├─► PHÂN HỆ 2: GAP ANALYSIS
      │      └─ Vẽ biểu đồ phân loại 3 Vùng Tâm lý (E dè / Cân bằng / Chờ đợi)
      │
      ├─► PHÂN HỆ 3: CS DEEP DIVE ──(Người dùng chọn Ngành & Kinh nghiệm)─┐
      │      │                                                            │
      │      ├─ [Gap > 0.5]  ──► Render: Biểu đồ Động lực                 │ (Lưu vào 
      │      ├─ [Gap < -0.5] ─► Render: Biểu đồ Rào cản                   │  st.session_state)
      │      └─ [Cân bằng]   ──► Render: Cả 2 biểu đồ đối trọng           │
      │                                                                   │
      └─► PHÂN HỆ 4: ĐỀ XUẤT AI AGENT ◄──(Kế thừa dữ liệu Session State)──┘
             │
             ├─ [Bước 1] Mapping dữ liệu với Dictionary cấu hình Agent chuyên biệt
             ├─ [Bước 2] Phân lớp Kinh nghiệm 
             └─ [Bước 3] Giới hạn Quyền hạn AI dựa trên Gap Score:
                  ├─ Nỗi Sợ (Gap < -0.5)    ─► Review & Compliance Agent (Human-in-the-loop)
                  ├─ An Toàn (Cân bằng)     ─► Guidance & Guardrail Agent (Cùng thao tác)
                  └─ Khao Khát (Gap > 0.5)  ─► Autonomous Co-pilot (Cấp toàn quyền tự quyết)
```

