import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

st.set_page_config(page_title="AI Agent trong CS", layout="wide")

# --- ĐOẠN CSS ĐỂ PHÓNG TO TOÀN BỘ CHỮ TRÊN STREAMLIT ---
st.markdown("""
<style>
    /* Phóng to chữ văn bản bình thường (Markdown, text) */
    html, body, [class*="st-"] p, li {
        font-size: 22px !important;
        color: black !important;
    }
    
    /* Phóng to các tiêu đề con (Subheader) */
    h3 {
        font-size: 30px !important;
        color: black !important;
    }

    /* Phóng to phần con số bự trong thẻ st.metric */
    [data-testid="stMetricValue"] {
        font-size: 45px !important;
        font-weight: bold !important;
        color: black !important;
    }
    
    /* Phóng to chữ tiêu đề nhỏ phía trên con số trong thẻ st.metric */
    [data-testid="stMetricLabel"] {
        font-size: 24px !important;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    try:
        d = pd.read_csv(os.path.join(DATA_DIR, "domain_worker_desires.csv"))
        c = pd.read_csv(os.path.join(DATA_DIR, "expert_rated_technological_capability.csv"))
        m = pd.read_csv(os.path.join(DATA_DIR, "domain_worker_metadata.csv")) 
        n = pd.read_csv(os.path.join(DATA_DIR, "task_statement_with_metadata.csv"))
        return d, c, m, n 
    except FileNotFoundError:
        st.error("Không tìm thấy các file dữ liệu CSV trong thư mục. Vui lòng kiểm tra lại!")
        st.stop()

# Khai báo thêm biến metadata để hứng dữ liệu từ file mới
desires, capability, worker_metadata, task_metadata = load_data()

CS_ROLES = [
    "Computer Programmers", "Computer Systems Analysts",
    "Computer Systems Engineers/Architects", "Computer Network Support Specialists",
    "Computer User Support Specialists", "Computer and Information Systems Managers",
    "Computer and Information Research Scientists", "Software Quality Assurance Analysts and Testers",
    "Web Developers", "Database Administrators", "Information Security Analysts",
    "Information Technology Project Managers", "Network and Computer Systems Administrators"
]
# ===== KHỞI TẠO BỘ NHỚ TẠM (LIÊN KẾT TRANG 3 VÀ TRANG 4) =====
if "saved_role" not in st.session_state:
    st.session_state["saved_role"] = CS_ROLES[0]
if "saved_exp" not in st.session_state:
    st.session_state["saved_exp"] = "Tất cả mức kinh nghiệm"
if "saved_gap" not in st.session_state:
    st.session_state["saved_gap"] = 0.0

# Lọc riêng bảng dữ liệu mong muốn của nhân viên, chỉ giữ lại 13 ngành Khoa học máy tính
cs_desires_filtered = desires[desires["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]
avg_desire = cs_desires_filtered.groupby("Occupation (O*NET-SOC Title)")["Automation Desire Rating"].mean()

# Lọc riêng bảng dữ liệu đánh giá của chuyên gia, chỉ giữ lại 13 ngành Khoa học máy tính
cs_capability_filtered = capability[capability["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]
avg_cap = cs_capability_filtered.groupby("Occupation (O*NET-SOC Title)")["Automation Capacity Rating"].mean()

common = avg_desire.index.intersection(avg_cap.index)

# Gộp dữ liệu thành bảng đối chiếu
gap_df = pd.DataFrame({"Occupation": common, "Worker Desire": avg_desire[common].values,
                       "Expert Capacity": avg_cap[common].values})
gap_df["Gap"] = (gap_df["Worker Desire"] - gap_df["Expert Capacity"]).round(2)
cs_gap = gap_df.sort_values("Gap")

# Khai báo menu điều hướng
pages = ["Tổng quan", "Gap Analysis", "CS Deep Dive", "Đề xuất AI Agent"]
choice = st.sidebar.radio("Chọn", pages)

# =====================================================================
# 1. TRANG TỔNG QUAN
# =====================================================================
if choice == "Tổng quan":
    st.title("AI Agent trong Khoa học Máy tính")
    
    cs_desires = desires[desires["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]
    cs_capability = capability[capability["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]

    st.markdown("**Dataset**: Phân tích các tác vụ từ người lao động và đánh giá từ chuyên gia AI")

    col1, col2, col3 = st.columns(3)
    col1.metric("Khảo sát Người lao động", f"{len(cs_desires):,}")
    col2.metric("Đánh giá từ Chuyên gia", f"{len(cs_capability):,}")
    col3.metric("Số Ngành IT Phân tích", len(CS_ROLES))

    st.divider()

    st.subheader("1. Tại sao kỹ sư IT khao khát dùng AI?")
    st.markdown("Thay vì ôm việc, người lao động muốn giao việc cho AI để giải quyết những nỗi đau thực tế sau:")

    reason_map = {
        "Reasons for Automation Desire - Free Time": "Giải phóng thời gian rảnh rỗi  ",
        "Reasons for Automation Desire - Scale": "Giúp xử lý lượng dữ liệu khổng lồ  ",
        "Reasons for Automation Desire - Human Error": "Tránh con người làm sai sót lặt vặt  ",
        "Reasons for Automation Desire - Repetitive": "Thoát khỏi việc copy-paste lặp đi lặp lại  ",
        "Reasons for Automation Desire - Stress": "Giảm bớt áp lực, căng thẳng  ",
        "Reasons for Automation Desire - Difficulty": "Đỡ phải tính toán quá phức tạp  "
    }

    rc = {label: int(cs_desires[col].sum()) for col, label in reason_map.items()}
    rdf = pd.DataFrame({"Reason": list(rc.keys()), "Count": list(rc.values())})
    rdf["%"] = (rdf["Count"] / len(cs_desires) * 100).round(1)
    
    rdf = rdf.sort_values("Count").reset_index(drop=True)
    fig1 = px.bar(rdf, x="Count", y="Reason", orientation="h", color="Count", color_continuous_scale="Blues")
    
    fig1.update_traces(
        texttemplate="%{x} người (%{customdata}%)", 
        textposition="outside",
        customdata=rdf[["%"]], 
        textfont=dict(color="black", size=16)
    ) 
    
    fig1.update_layout(
        title="Top lý do muốn tự động hóa công việc",
        title_font_size=22, height=550, margin=dict(l=450, r=80)
    )
    fig1.update_yaxes(title="", tickfont=dict(size=18, color="black"))
    fig1.update_xaxes(title="Số lượng người", tickfont=dict(size=18, color="black"), title_font=dict(size=18, color="black"))
    st.plotly_chart(fig1, use_container_width=True, theme=None)

    st.subheader("2. Tại sao lại sợ giao phó 100% cho AI?")
    st.markdown("Dù AI rất giỏi, nhưng con người vẫn kiên quyết phải giữ lại quyền can thiệp vì những lo lắng sau:")

    agency_map = {
        "Reasons for Human Agency - Quality Oversight": "Phải có người duyệt chất lượng cuối cùng  ",
        "Reasons for Human Agency - Control": "Sợ mất quyền kiểm soát hệ thống  ",
        "Reasons for Human Agency - Ethical": "Ai sẽ chịu trách nhiệm pháp lý/đạo đức khi có lỗi  ",
        "Reasons for Human Agency - Domain Knowledge": "AI không hiểu sâu ngữ cảnh kinh doanh công ty  ",
        "Reasons for Human Agency - Dynamic": "Khách hàng thay đổi liên tục, AI không linh hoạt bằng  ",
        "Reasons for Human Agency - Empathy": "Cần sự thấu cảm, dỗ dành khách hàng  "
    }

    ac = {label: int(cs_desires[col].sum()) for col, label in agency_map.items()}
    adf = pd.DataFrame({"Reason": list(ac.keys()), "Count": list(ac.values())})
    adf["%"] = (adf["Count"] / len(cs_desires) * 100).round(1)
    adf = adf.sort_values("Count", ascending=True).reset_index(drop=True)

    # CHỈNH SỬA: Thêm tham số orientation="h" định dạng chuẩn thanh ngang
    fig2 = px.bar(adf, x="Count", y="Reason", orientation="h", color="Count", color_continuous_scale="Reds")
    
    fig2.update_traces(
        texttemplate="%{x} người (%{customdata}%)", 
        textposition="outside",
        customdata=adf[["%"]], 
        textfont=dict(color="black", size=16)
    )
    
    fig2.update_layout(
        title="Top lý do kiên quyết phải giữ lại con người",
        title_font_size=22, height=550, margin=dict(l=450, r=80)
    )
    fig2.update_yaxes(title="", tickfont=dict(size=20, color="black"))
    fig2.update_xaxes(title="Số lượng người", tickfont=dict(size=18, color="black"), title_font=dict(size=18, color="black"))
    st.plotly_chart(fig2, use_container_width=True, theme=None)

# =====================================================================
# 2. TRANG GAP ANALYSIS
# =====================================================================
elif choice == "Gap Analysis":
    st.title("Phân tích Độ Lệch: Giữa 'Mong Muốn' và 'Thực Tế'")
    st.markdown("""
    Lấy **Mức độ nhân viên muốn** trừ đi **Năng lực thực tế AI làm được**. 
    Kết quả sinh ra 2 trường hợp:
    * 🛑 **Độ lệch Âm (Vùng E Dè):** AI làm dư sức, nhưng con người sợ hãi không dám giao việc.
    * 🟢 **Độ lệch Dương (Vùng Chờ Đợi):** Con người rất khát khao tự động hóa, nhưng AI hiện tại chưa đáp ứng được.
    """)

    fig2 = px.bar(cs_gap, x="Gap", y="Occupation", orientation="h", color="Gap", color_continuous_scale="RdYlGn")
    
    fig2.update_traces(
        texttemplate="%{x:.2f}", 
        textposition="outside",
        textfont=dict(size=16, color="black")
    )
    fig2.update_layout(height=750, margin=dict(l=400, r=80))
    fig2.update_yaxes(title="", categoryorder="total ascending", tickfont=dict(size=18, color="black"))
    fig2.update_xaxes(title="Điểm Gap (Mong muốn - Năng lực)", tickfont=dict(size=18, color="black"), title_font=dict(size=18, color="black"))
    
    # Thêm theme=None để giữ phông chữ to rõ ràng
    st.plotly_chart(fig2, use_container_width=True, theme=None)

    st.markdown("---")
    st.subheader("💡 Đọc vị tâm lý nhân sự từ Biểu đồ Độ lệch")
    
    col_red, col_green = st.columns(2)
    
    with col_red:
        st.error("""
        **🛑 Nhóm Cảnh Giác & E Dè (Thanh màu Đỏ - Gap Âm):**
        * **Đại diện tiêu biểu:** Database Administrators, Computer Network Support Specialists, Web Developers.
        * **Đặc điểm:** Đây là những người nắm giữ "huyết mạch" của hệ thống (dữ liệu khách hàng, máy chủ, hạ tầng mạng). Mọi sai sót của AI đều có thể gây sập hệ thống hoặc lộ dữ liệu nhạy cảm.
        * **Insight:** AI hiện tại đủ sức làm, nhưng nhân viên từ chối giao quyền tự quyết. Họ thà tự làm còn hơn chịu rủi ro đạo đức/pháp lý do AI gây ra.
        """)
        
    with col_green:
        st.success("""
        **🟢 Nhóm Khao Khát & Chờ Đợi (Thanh màu Xanh - Gap Dương):**
        * **Đại diện tiêu biểu:** Computer and Information Research Scientists, Information Technology Project Managers.
        * **Đặc điểm:** Đây là những công việc thiên về xử lý khối lượng thông tin khổng lồ, đọc tài liệu khoa học, hoặc quản lý tiến độ tổng thể. Họ đang bị quá tải (cognitive overload).
        * **Insight:** Nhóm này sẵn sàng chấp nhận việc AI chưa hoàn hảo, miễn là AI giúp họ tóm tắt, tổng hợp và giảm bớt gánh nặng. Động lực giải phóng sức lao động hoàn toàn lấn át rào cản sợ hãi.
        """)
        
    st.info("""
    **⚖️ Nhóm Cân Bằng (Khu vực trung tâm - Xấp xỉ 0):** \n
    Các ngành như *Software Quality Assurance Analysts* hay *Computer Systems Analysts* có độ lệch không quá lớn. Họ hiểu rõ giới hạn của AI: biết dùng AI để tăng tốc công việc, nhưng vẫn ý thức được việc phải tự mình rà soát lại kết quả cuối cùng.
    """)
# =====================================================================
# 3. TRANG CS DEEP DIVE
# =====================================================================
elif choice == "CS Deep Dive":
    st.title("Phân tích xem nhân viên Ngành Khoa Học Máy Tính nghĩ gì?")
    st.markdown("Nỗi lo lớn nhất của nhân viên các ngành thuộc Khoa Học Máy Tính là gì:")

    # 1. Gộp dữ liệu Tâm lý (desires) và Nhân khẩu học (metadata)
    df_merged = pd.merge(desires, worker_metadata, on=['User ID', 'Occupation (O*NET-SOC Title)'], how='inner')

    # 2. Tạo 2 Selectbox cạnh nhau (Nghề nghiệp và Kinh nghiệm)
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        role = st.selectbox("Lựa Chọn Nghề Nghiệp:", CS_ROLES)
    with col_filter2:
        danh_sach_kinh_nghiem = [
            "Tất cả mức kinh nghiệm", 
            "Less than 1 year", 
            "1-2 year", 
            "3-5 years", 
            "6-10 years", 
            "More than 10 years"
        ]
        exp = st.selectbox("Lựa Chọn Số Năm Kinh Nghiệm:", danh_sach_kinh_nghiem)

    # 3. Lọc dữ liệu theo lựa chọn
    if exp == "Tất cả mức kinh nghiệm":
        d_sub = df_merged[df_merged["Occupation (O*NET-SOC Title)"] == role]
    else:
        d_sub = df_merged[(df_merged["Occupation (O*NET-SOC Title)"] == role) & (df_merged["Experience"] == exp)]

    st.markdown("---")
    
    # 4. Tính toán điểm Gap ĐỘNG (Dynamic Gap)
    diem_may_gioi = avg_cap.get(role, 0)

    if len(d_sub) > 0:
        diem_muon = d_sub["Automation Desire Rating"].mean()
        diem_gap = diem_muon - diem_may_gioi

        dong_luc = {
            "Muốn có thời gian nghỉ ngơi  ": d_sub["Reasons for Automation Desire - Free Time"].sum(),
            "Việc nhiều quá, làm tay không nổi  ": d_sub["Reasons for Automation Desire - Scale"].sum(),
            "Máy làm sẽ ít sai vặt hơn người  ": d_sub["Reasons for Automation Desire - Human Error"].sum(),
            "Chán phải làm đi làm lại một việc  ": d_sub["Reasons for Automation Desire - Repetitive"].sum(),
            "Công việc hiện tại quá mệt mỏi  ": d_sub["Reasons for Automation Desire - Stress"].sum()
        }
        thich_nhat = max(dong_luc, key=dong_luc.get) if sum(dong_luc.values()) > 0 else "Không có dữ liệu"

        rao_can = {
            "Sợ máy làm sai, phải có người kiểm tra ": d_sub["Reasons for Human Agency - Quality Oversight"].sum(),
            "Sợ máy tự làm hỏng hệ thống ": d_sub["Reasons for Human Agency - Control"].sum(),
            "Nếu máy sai ai đền? Cần người chịu trách nhiệm ": d_sub["Reasons for Human Agency - Ethical"].sum(),
            "Máy không hiểu tình hình thực tế của công ty ": d_sub["Reasons for Human Agency - Domain Knowledge"].sum()
        }
        so_nhat = max(rao_can, key=rao_can.get) if sum(rao_can.values()) > 0 else "Không có dữ liệu"

        # Đánh giá chung dựa trên biên độ 0.5
        if diem_gap < -0.5:
            nhan_xet = "Nhóm Cẩn Thận (Máy làm dư sức nhưng nhân viên không dám giao)"
            loi_khuyen = "Tuyệt đối không để máy tự làm tự quyết. Phải bắt máy làm nháp, người kiểm tra xong mới được chạy."
        elif diem_gap > 0.5:
            nhan_xet = "Nhóm Mệt Mỏi (Đang làm việc quá sức, rất muốn có máy làm thay)"
            loi_khuyen = "Cứ mạnh dạn giao hết mấy việc lặt vặt cho máy làm để nhân viên được nghỉ ngơi."
        else:
            nhan_xet = "Nhóm Cân Bằng (Biết chia việc hợp lý)"
            loi_khuyen = "Chia việc đôi bên cùng làm. Máy xử lý dữ liệu thô, con người ra quyết định."

        st.subheader(f"Kết quả phân tích: {role} ({exp})")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Điểm Gap (Mong muốn - Năng lực AI)", f"{diem_gap:+.2f}")
            st.write(f"**Điểm khao khát của nhóm này:** {diem_muon:.2f} / 5.0")
            st.write(f"**Điểm năng lực AI thực tế:** {diem_may_gioi:.2f} / 5.0")
        
        with col2:
            st.markdown(f"**Nhận xét:** {nhan_xet}")
            st.markdown(f"**Lời Khuyên:** {loi_khuyen}")

        # ===== HIỂN THỊ BIỂU ĐỒ ĐỘNG THEO BIÊN ĐỘ (-0.5 ĐẾN 0.5) =====
        st.markdown("---")
        df_dong_luc = pd.DataFrame({
            "Lý do": list(dong_luc.keys()),
            "Số người chọn": list(dong_luc.values())
        }).sort_values("Số người chọn", ascending=True)
        
        df_rao_can = pd.DataFrame({
            "Lý do": list(rao_can.keys()),
            "Số người chọn": list(rao_can.values())
        }).sort_values("Số người chọn", ascending=True)

        if diem_gap > 0.5: 
            st.subheader("📈 Tại sao nhóm này lại khao khát AI đến vậy?")
            st.markdown("*(Khoảng cách Gap lớn hơn 0.5. Chỉ hiển thị các lý do khuyến khích xài AI do nhu cầu quá lớn)*")
            fig_muon = px.bar(df_dong_luc, x="Số người chọn", y="Lý do", orientation="h", color_discrete_sequence=["#1E88E5"])
            fig_muon.update_traces(texttemplate="%{x} người", textposition="outside", textfont=dict(size=16, color="black"))
            fig_muon.update_layout(height=450, font=dict(size=16, color="black"), margin=dict(l=350, r=100))
            fig_muon.update_yaxes(title="")
            st.plotly_chart(fig_muon, use_container_width=True, theme=None)

        elif diem_gap < -0.5:
            st.subheader("🛡️ Điều gì khiến nhóm này e dè việc giao quyền cho AI?")
            st.markdown("*(Khoảng cách Gap thấp hơn -0.5. Chỉ hiển thị các rào cản tâm lý do sự e dè lấn át)*")
            fig_so = px.bar(df_rao_can, x="Số người chọn", y="Lý do", orientation="h", color_discrete_sequence=["#D32F2F"])
            fig_so.update_traces(texttemplate="%{x} người", textposition="outside", textfont=dict(size=16, color="black"))
            fig_so.update_layout(height=450, font=dict(size=16, color="black"), margin=dict(l=350, r=100))
            fig_so.update_yaxes(title="")
            st.plotly_chart(fig_so, use_container_width=True, theme=None)

        else:
            st.subheader("⚖️ Trạng thái giằng co: Điểm mong muốn và thực tế khá cân bằng")
            st.markdown(f"*(Khoảng cách Gap là **{diem_gap:+.2f}**, nằm trong vùng dao động từ -0.5 đến 0.5. Hiển thị đối trọng cả hai góc nhìn)*")
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.markdown("**Động lực thúc đẩy:**")
                fig_muon = px.bar(df_dong_luc, x="Số người chọn", y="Lý do", orientation="h", color_discrete_sequence=["#1E88E5"])
                fig_muon.update_traces(texttemplate="%{x} người", textposition="outside", textfont=dict(size=16, color="black"))
                fig_muon.update_layout(height=400, font=dict(size=16, color="black"), margin=dict(l=350, r=50))
                fig_muon.update_yaxes(title="")
                st.plotly_chart(fig_muon, use_container_width=True, theme=None)
            with chart_col2:
                st.markdown("**Rào cản tâm lý:**")
                fig_so = px.bar(df_rao_can, x="Số người chọn", y="Lý do", orientation="h", color_discrete_sequence=["#D32F2F"])
                fig_so.update_traces(texttemplate="%{x} người", textposition="outside", textfont=dict(size=16, color="black"))
                fig_so.update_layout(height=400, font=dict(size=16, color="black"), margin=dict(l=350, r=50))
                fig_so.update_yaxes(title="")
                st.plotly_chart(fig_so, use_container_width=True, theme=None)


# =====================================================================
# 4. TRANG ĐỀ XUẤT AI AGENT (ĐỘNG THEO LỰA CHỌN)
# =====================================================================
elif choice == "Đề xuất AI Agent":
    st.title("Đề Xuất AI Agent Chuyên Biệt")
    st.markdown("Cấu hình hệ thống AI được thiết kế tự động hóa dựa trên điểm Gap tâm lý của từng nhóm kinh nghiệm.")

    # 1. Gộp dữ liệu để tính toán giống Trang 3
    df_merged = pd.merge(desires, worker_metadata, on=['User ID', 'Occupation (O*NET-SOC Title)'], how='inner')

    # 2. Bộ lọc (Tự động lấy giá trị từ Session State nếu có, nếu không lấy mặc định)
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        default_role = st.session_state.get("saved_role", CS_ROLES[0])
        role = st.selectbox("Lựa Chọn Nghề Nghiệp:", CS_ROLES, index=CS_ROLES.index(default_role))
    with col_filter2:
        danh_sach_kinh_nghiem = ["Tất cả mức kinh nghiệm", "Less than 1 year", "1-2 year", "3-5 years", "6-10 years", "More than 10 years"]
        default_exp = st.session_state.get("saved_exp", danh_sach_kinh_nghiem[0])
        exp = st.selectbox("Lựa Chọn Số Năm Kinh Nghiệm:", danh_sach_kinh_nghiem, index=danh_sach_kinh_nghiem.index(default_exp))

    # Cập nhật lại session_state nếu người dùng đổi lựa chọn ngay tại Trang 4
    st.session_state["saved_role"] = role
    st.session_state["saved_exp"] = exp

    agent_configs = {
        "Computer Programmers": {
            "agents": ["Code Generation Agent", "Code Review Agent", "Documentation Agent"],
            "reason": "Lập trình viên thường chán nản khi viết đi viết lại những đoạn code cơ bản. Các AI Agent này sẽ giúp viết nháp, tự dò lỗi sai và tự động viết tài liệu giải thích code."
        },
        "Software Quality Assurance Analysts and Testers": {
            "agents": ["Test Automation Agent", "Bug Detection Agent", "Test Case Generator"],
            "reason": "Việc bấm thử phần mềm hàng ngàn lần rất tốn thời gian. AI Agent có thể tự động viết kịch bản test, chạy thử ngầm mỗi đêm và báo cáo lỗi (bug)."
        },
        "Web Developers": {
            "agents": ["Web Dev Agent", "UI-to-Code Agent", "Accessibility Agent"],
            "reason": "Giúp tiết kiệm thời gian bằng cách nhìn vào bản vẽ thiết kế và tự động gõ ra thành code trang web hoàn chỉnh."
        },
        "Database Administrators": {
            "agents": ["DBA Agent", "Query Optimization Agent", "NL2SQL Agent"],
            "reason": "AI đọc dữ liệu siêu nhanh, giúp tìm ra nguyên nhân làm trang web bị chậm, tự động dọn dẹp và sao lưu (backup) dữ liệu mỗi ngày."
        },
        "Network and Computer Systems Administrators": {
            "agents": ["Network Admin Agent", "Self-healing Agent", "Security Response Agent"],
            "reason": "Con người không thể thức 24/7 để canh máy chủ. AI Agent sẽ trực thay, nếu thấy mạng nghẽn thì tự động phân luồng lại cho hết nghẽn."
        },
        "Computer Network Support Specialists": {
            "agents": ["Helpdesk Agent", "Troubleshooting Agent", "Network Monitoring Agent"],
            "reason": "Đỡ đần việc trả lời tin nhắn của nhân viên. AI có thể chẩn đoán mạng lỗi do đâu và chỉ cho người dùng cách khởi động lại."
        },
        "Computer User Support Specialists": {
            "agents": ["IT Helpdesk Agent", "FAQ Bot", "Remote Troubleshooting Agent"],
            "reason": "Tự động hướng dẫn người dùng cuối giải quyết mấy lỗi vặt như quên mật khẩu, máy in không chạy, màn hình xanh."
        },
        "Computer and Information Research Scientists": {
            "agents": ["Research Agent", "Literature Review Agent", "Experiment Design Agent"],
            "reason": "Nhà nghiên cứu mất rất nhiều thời gian đọc tài liệu. AI sẽ đọc hộ hàng ngàn bài báo khoa học, tóm tắt lại và gợi ý cách làm thí nghiệm."
        },
        "Computer Systems Analysts": {
            "agents": ["Requirement Analysis Agent", "System Design Agent", "Documentation Agent"],
            "reason": "Giúp nghe và ghi chép lại yêu cầu của khách hàng, sau đó tự động vẽ sơ đồ thiết kế hệ thống."
        },
        "Computer Systems Engineers/Architects": {
            "agents": ["Architecture Review Agent", "Design Validation Agent", "Tech Stack Advisor"],
            "reason": "Kiểm tra lại xem bản thiết kế hệ thống có bị hổng bảo mật hay không, gợi ý xem nên dùng công nghệ gì thì rẻ và tốt nhất."
        },
        "Information Security Analysts": {
            "agents": ["Security Monitoring Agent", "Threat Detection Agent", "Compliance Checker"],
            "reason": "Đọc hàng triệu lịch sử thao tác trên máy chủ để báo động ngay lập tức nếu có dấu hiệu hacker xâm nhập."
        },
        "Information Technology Project Managers": {
            "agents": ["Project Planning Agent", "Risk Monitoring Agent", "Report Generator"],
            "reason": "Tự động gom số liệu công việc từ các phòng ban, đoán xem dự án có bị trễ hạn không và tự động vẽ báo cáo cho Sếp."
        },
        "Computer and Information Systems Managers": {
            "agents": ["Dashboard Agent", "Resource Planning Agent", "Decision Support Agent"],
            "reason": "Phân tích dữ liệu lớn để giúp Giám đốc quyết định xem nên đầu tư thêm tiền vào đâu, cắt giảm chi phí chỗ nào."
        }
    }

    # 3. Lọc dữ liệu và tính Gap
    if exp == "Tất cả mức kinh nghiệm":
        d_sub = df_merged[df_merged["Occupation (O*NET-SOC Title)"] == role]
    else:
        d_sub = df_merged[(df_merged["Occupation (O*NET-SOC Title)"] == role) & (df_merged["Experience"] == exp)]

    st.markdown("---")
    diem_may_gioi = avg_cap.get(role, 0)
    base_config = agent_configs[role]

    if len(d_sub) > 0:
        diem_muon = d_sub["Automation Desire Rating"].mean()
        diem_gap = diem_muon - diem_may_gioi
        st.session_state["saved_gap"] = diem_gap # Lưu lại phòng khi chuyển tab

        # ===== LOGIC TỰ ĐỘNG ĐỀ XUẤT AGENT DỰA VÀO ĐIỂM GAP TÍNH ĐƯỢC =====
        if diem_gap > 0.5:
            loai_agent = "Autonomous Co-pilot (Trợ lý Tự chủ Hoàn toàn)"
            danh_sach_agent = base_config['agents'] # Cấp full bộ Agent
            chien_luoc = f"**Động lực áp đảo Nỗi lo:** Nhóm này đang quá tải và khát khao AI.\n\n **Chiến lược:** Cấp quyền tối đa. Để AI Agent tự động hóa hoàn toàn các task nhàm chán nhằm giải phóng sức lao động.\n\n*Chi tiết:* {base_config['reason']}"
            mau_sac = "success"
        elif diem_gap < -0.5:
            loai_agent = "Review & Compliance Agent (Trợ lý Phân tích & Đệ trình)"
            danh_sach_agent = [f"Drafting {base_config['agents'][0]}", "Audit Agent", "Compliance Checker"]
            chien_luoc = f"**Nỗi lo áp đảo Động lực:** Nhóm này khắt khe, sợ mất kiểm soát và e dè rủi ro hệ thống.\n\n **Chiến lược:** Thiết lập mô hình Human-in-the-loop (Con người là trung tâm). AI Agent chỉ có nhiệm vụ tổng hợp thông tin, viết bản nháp và đệ trình. Quyết định bấm nút 'Approve' (Phê duyệt) cuối cùng bắt buộc phải do con người thực hiện."
            mau_sac = "error"
        else:
            loai_agent = "Guidance & Guardrail Agent (Trợ lý Hướng dẫn & Kiểm duyệt)"
            danh_sach_agent = [f"Step-by-step {base_config['agents'][0]}", "Validation Agent", "Knowledge Base Agent"]
            chien_luoc = f"**Trạng thái Cân bằng:** Nhóm này có sự dè chừng nhất định, cần AI nhưng không tin tưởng tuyệt đối.\n\n **Chiến lược:** Không cấp quyền cho AI tự động chạy. AI Agent đóng vai trò hướng dẫn từng bước (Step-by-step) và cảnh báo rủi ro nếu thao tác sai."
            mau_sac = "warning"

        st.subheader(f"Cấu hình triển khai: {role}")
        st.info(f"Dữ liệu đang dựa trên nhóm kinh nghiệm: **{exp}** | Điểm Gap hiện tại: **{diem_gap:+.2f}**")
        
        st.markdown(f"**🔹 Phân loại hệ thống AI:** {loai_agent}")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if mau_sac == "success":
                st.success("**Các Agent cần kích hoạt:**")
            elif mau_sac == "error":
                st.error("**Các Agent cần kích hoạt:**")
            else:
                st.warning("**Các Agent cần kích hoạt:**")
                
            for agent in danh_sach_agent:
                st.markdown(f"- {agent}")
                
        with col2:
            st.markdown("**Chiến lược Quản trị Rủi ro (HR Strategy):**")
            if mau_sac == "success":
                st.success(chien_luoc)
            elif mau_sac == "error":
                st.error(chien_luoc)
            else:
                st.warning(chien_luoc)

    else:
        st.warning(f"Không có dữ liệu khảo sát cho ngành **{role}** ở mức kinh nghiệm **{exp}**.")