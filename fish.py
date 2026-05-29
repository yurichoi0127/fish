import streamlit as st
import pandas as pd
import altair as alt
import os
import re
import numpy as np
import matplotlib.pyplot as plt  
import base64
import random
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import pydeck as pdk

# --- [초기 세팅] ---
st.set_page_config(page_title="나만의 열대어 키우기", page_icon="🐠", layout="wide")

st.markdown("""
<style>
[data-testid="stImage"] img {
    height: 130px; 
    object-fit: contain; 
    margin: 0 auto; 
}
.tank-box {
    border: 3px solid #4A90E2;
    border-radius: 10px;
    background-color: rgba(74, 144, 226, 0.1);
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #4A90E2;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

div[data-testid="stButton"] button p {
    white-space: nowrap !important;
}
</style>
""", unsafe_allow_html=True)

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "fish_db.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_image_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            data = f.read()
        return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    return ""

if "db_fishes" not in st.session_state:
    if os.path.exists(CSV_PATH):
        st.session_state.db_fishes = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    else:
        st.error(f"❌ {CSV_PATH} 파일을 찾을 수 없습니다!")
        st.session_state.db_fishes = pd.DataFrame(columns=[
            "fish_name", "min_ph", "max_ph", "min_temp", "max_temp", 
            "adult_size", "aggression", "pollution_factor", "difficulty", "description", "image_path", "is_custom"
        ])

if "my_tank" not in st.session_state:
    st.session_state.my_tank = {"w": 90, "l": 45, "h": 45, "filter_name": "스펀지 여과기 (기본/소형)", "filter_mult": 0.5}
if "my_fishes" not in st.session_state:
    st.session_state.my_fishes = {}
if "setup_date" not in st.session_state:
    st.session_state.setup_date = datetime.today().date()

# --- [사이드바 메뉴] ---
with st.sidebar:
    st.title("🐠 메뉴 이동")
    menu = st.radio("Navigation", [
        "🔰 초보자 가이드", 
        "📖 열대어 도감", 
        "📐 나만의 어항 만들기", 
        "🧮 생태계 시뮬레이터", 
        "🔮 가상 아쿠아리움"
    ], label_visibility="collapsed")
    st.divider()
    st.caption("© 2026 My Fish Tank")

st.title("🐠 나만의 열대어 키우기")
st.markdown("---")

# ==========================================
# 1. 초보자 가이드
# ==========================================
if menu == "🔰 초보자 가이드":
    st.header("📚 초보자를 위한 완벽 물생활 가이드")
    st.markdown("성공적인 물생활을 위해 꼭 알아야 할 핵심 지식들을 모았습니다. 아래 탭을 클릭하여 확인해 보세요!")
    st.info("""
**💡 열대어(Tropical Fish)란?** 열대어는 열대 및 아열대 지역의 담수나 해수에 서식하는 화려하고 아름다운 물고기들을 말합니다.
성공적인 물생활의 핵심은 각 열대어가 살아온 자연 환경의 수온, pH(산도), 그리고 공간적 밸런스(Bioload)를 어항 속에 조화롭게 재현하는 것입니다.
""")

    tab1, tab2, tab3, tab4 = st.tabs(["🎬 필수 시청 영상", "🧪 여과 사이클 & 환수", "🐟 합사 및 주의사항", "🛒 필수 준비물"])

    with tab1:
        st.subheader("📺 물생활 입문자를 위한 추천 영상")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.video("https://youtu.be/XgYr-k0IAFM", start_time=24)
        with c2:
            st.success("💡 **영상의 핵심 포인트**\n\n초보자가 어항을 처음 세팅할 때 흔히 하는 실수와 기본기를 아주 쉽게 설명해 주는 영상입니다.")
            st.markdown("""
            **체크 리스트:**
            - ✅ 바닥재와 여과기 세팅법
            - ✅ 물잡이의 개념과 중요성
            - ✅ 생물 투입 전 필수 대기 시간
            """)

    with tab2:
        st.subheader("생존의 핵심, '여과 사이클(물잡이)'")
        st.error("🚨 **초보자 최대 실수:** 어항에 물을 채운 당일 날 물고기를 바로 넣으면, 암모니아 중독으로 99% 폐사합니다!")
        st.caption("💡 보편적으로 어항 세팅 후 3~4주 정도 여과기를 돌리며 **물잡이** 를 합니다. 생물은 물잡이가 완전히 끝난 후 **첫 생물을 투입하는 날짜** 에 맞춰서 넣어주세요.")
        st.markdown("**여과 사이클이란?** 물고기의 배설물에서 나오는 맹독성 **암모니아**를 덜 해로운 **질산염**으로 분해해 줄 '이로운 여과 박테리아'들을 어항 내에 배양하는 과정입니다. 박테리아제를 넣더라도 물고기를 넣기 전, 물만 돌리며 최소 **3~4주**의 물잡이 기간이 필요합니다.")
        
        st.success("🧹**배설물** ➡️ (독성 MAX) 암모니아 ☠️ ➡️ *박테리아 분해* 🦠 ➡️ (독성 중간) 아질산염 ⚠️ ➡️ *박테리아 분해* 🦠 ➡️ (독성 최소) 질산염 💧 ➡️ 환수로 제거")
        st.divider()
        
        st.subheader("🪣 올바른 환수(물갈이) 방법")
        c3, c4 = st.columns(2)
        with c3:
            st.info("""**✔️주기 및 비율:** 일주일에 1회, 전체 물양의 20~30%만 교체  
                    **✔️온도 맞춤:** 새 물은 어항 물과 온도를 동일하게 맞춰야 쇼크가 없습니다.  
                    **✔️염소 제거:** 하루 전날 수돗물을 받아두거나 염소 제거제를 꼭 사용하세요.""")
        with c4:
            st.warning("""**❌** 어항 물 전체를 갈아엎거나, 여과기 스펀지를 수돗물로 씻지 마세요.  
                       ❌ 힘들게 키운 여과 박테리아가 몰살되어 수중 생태계가 완전 붕괴됩니다.  
                       ❌ 여과기 청소가 필요할 때는 반드시 '기존 어항 물'에 살살 헹궈주세요.""")
    with tab3:
        st.subheader("평화로운 어항을 위한 합사 규칙")
        st.warning('''**🐟 입에 들어가면 먹이입니다!** 열대어는 자신의 입 크기보다 작은 생물을 보면 본능적으로 사냥합니다. 크기 차이가 너무 나는 어종은 합사하지 마세요.''')
        
        with st.expander("⚠️ 생물 투입 전 필수 과정: 물맞댐 & 온도맞댐"):
            st.markdown("""
            수족관에서 물고기를 데려오자마자 어항에 붓는 것은 **화상이나 동상을 입히는 것과 같습니다.**
            1. **온도맞댐 (30분):** 봉투째로 어항 물에 띄워 수온을 서서히 맞춰줍니다.
            2. **물맞댐 (1시간):** 봉투를 열고 어항 물을 조금씩 봉투 안으로 넣어주어, 새로운 수질(pH)에 적응할 시간을 줍니다.
            """)
        with st.expander("⚠️ 먹이 급여 주의사항"):
            st.markdown("열대어 폐사 원인 1위는 아사(굶어 죽음)가 아니라 **과식과 남은 먹이로 인한 수질 오염**입니다. 먹이는 1~2분 안에 다 먹을 수 있는 양만 소량씩 주셔야 합니다.")

    with tab4:
        st.subheader("🛒 처음 시작할 때 꼭 필요한 필수 템")
        colA, colB, colC = st.columns(3)
        with colA:
            st.markdown("#### 📦 하드웨어")
            st.markdown("- **어항 (수조)**\n- **여과기** (스펀지, 걸이식 등)\n- **조명** (수초용/관상용)\n- **바닥재** (흑사, 소일, 모래)")
        with colB:
            st.markdown("#### 🌡️ 온도 관리")
            st.markdown("- **수조용 자동 온도 조절 히터** (보통 24~26도 유지)\n- **어항용 온도계**")
        with colC:
            st.markdown("#### 🧪 수질 관리 및 기타")
            st.markdown("- **수돗물 염소 제거제**\n- **생균 박테리아제**\n- **물갈이용 환수통 및 뜰채**\n- **열대어 전용 사료**")

# ==========================================
# 2. 열대어 도감
# ==========================================
elif menu == "📖 열대어 도감":
    st.subheader("📖 열대어 도감")
    df = st.session_state.db_fishes
    
    if df.empty:
        st.warning("도감 데이터가 비어있습니다.")
    else:
        cols = st.columns(5)
        for idx, row in df.iterrows():
            with cols[idx % 5]:
                with st.container(border=True):
                    name = row['fish_name']
                    diff = row['difficulty']
                    color = "#2e7d32" if diff == "초보자" else "#e65100" if diff == "중급자" else "#c62828"
                    st.markdown(f"<div style='font-size:1.1rem; font-weight:bold;'>{name} <span style='color:{color}; font-size:0.65em;'>[{diff}]</span></div>", unsafe_allow_html=True)
                    
                    img_path = os.path.join(DATA_DIR, os.path.basename(row['image_path']))
                    if os.path.exists(img_path): st.image(img_path, use_container_width=True)
                    else: st.image("https://via.placeholder.com/300x200.png?text=No+Image", use_container_width=True)
                    
                    with st.expander("🔍 상세 정보"):
                        st.markdown(f"**📝 특징:** {row['description']}")
                        st.markdown(f"**🧪 수질:** pH {row['min_ph']}\\~{row['max_ph']}  \n**🌡️ 수온:** {row['min_temp']}\\~{row['max_temp']}°C  \n**📏 크기:** {row['adult_size']}cm  \n**🧹 오염도:** {row['pollution_factor']}배")
                    
                    if 'is_custom' in row and (row['is_custom'] == True or row['is_custom'] == 1):
                        st.divider()
                        
                       
                        c1, c2 = st.columns(2, gap="small")
                        
                        with c1:
                            
                            if st.button("✏️ 수정", key=f"edit_{name}_{idx}", use_container_width=True):
                                st.session_state[f"editing_{idx}"] = True
                        with c2:
                            if st.button("🗑️ 삭제", key=f"del_{name}_{idx}", type="primary", use_container_width=True):
                                st.session_state.db_fishes = st.session_state.db_fishes.drop(idx).reset_index(drop=True)
                                st.session_state.db_fishes.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
                                
                               
                                if name in st.session_state.my_fishes:
                                    del st.session_state.my_fishes[name]
                                    
                                if f"adopt_{name}" in st.session_state:
                                    del st.session_state[f"adopt_{name}"]
                                
                                st.toast(f"❌ {name}이(가) 도감에서 삭제되었습니다.")
                                st.rerun()
                    else:
                        st.caption("🔒 기본 어종 (수정 불가)")
                    
                    if st.session_state.get(f"editing_{idx}", False):
                        with st.form(key=f"edit_form_{idx}"):
                            st.write(f"🔧 **{name} 수정**")
                            edit_desc = st.text_input("특징 변경", value=row['description'])
                            edit_size = st.number_input("크기 변경(cm)", value=float(row['adult_size']))
                            col_btn1, col_btn2 = st.columns(2)
                            if col_btn1.form_submit_button("💾 저장"):
                                st.session_state.db_fishes.at[idx, 'description'] = edit_desc
                                st.session_state.db_fishes.at[idx, 'adult_size'] = edit_size
                                st.session_state.db_fishes.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
                                st.session_state[f"editing_{idx}"] = False
                                st.toast("✅ 수정 반영 완료")
                                st.rerun()
                            if col_btn2.form_submit_button("취소"):
                                st.session_state[f"editing_{idx}"] = False
                                st.rerun()

    st.divider()
    st.subheader("➕ 나만의 도감 채우기")
    st.markdown("도감에 등장하지 않지만 당신이 키우고 싶은 새로운 물고기를 등록해 보세요! 추후 수정/삭제가 가능합니다.")
    
    with st.form("add_fish_form", clear_on_submit=True):
        cc1, cc2 = st.columns(2)
        with cc1:
            new_name = st.text_input("📝 물고기 이름", placeholder="예: 시클리드")
            new_diff = st.selectbox("🎯 사육 난이도", ["초보자", "중급자", "상급자"])
            new_ph = st.slider("🧪 적정 pH 범위 설정", 4.0, 9.0, (6.5, 7.5), step=0.1)
            new_temp = st.slider("🌡️ 적정 수온 범위 설정 (°C)", 15, 35, (24, 28))
        with cc2:
            new_size = st.number_input("📏 성체 크기 (cm)", min_value=0.5, max_value=100.0, value=5.0, step=0.5)
            new_agg = st.slider("🔥 공격성 점수 (1~10)", 1, 10, 3)
            new_poll = st.number_input("🧹 오염 가중치 (0.5 ~ 5.0)", min_value=0.5, max_value=5.0, value=1.0, step=0.1)
            new_desc = st.text_area("✍️ 어종별 한줄 요약 특징", placeholder="어항 내 합사 유의사항이나 특징을 기술해주세요.")
            
        new_img = st.file_uploader("🖼️ 가상 어항 연동용 배경 없는 물고기 이미지 업로드 (*.png 전용)", type=["png"])
        st.caption("배경이 없는 투명한 PNG 파일을 넣어야 추후 2D 어항 내부에서 이질감 없이 헤엄칠 수 있습니다.")

        submit_button = st.form_submit_button("✨ 도감 채우기", type="primary")

        if submit_button:
            if not new_name or not new_desc:
                st.error("❌ 물고기 이름과 한줄 요약 특징은 공란으로 둘 수 없는 필수값입니다.")
            elif df['fish_name'].eq(new_name).any():
                st.warning(f"⚠️ 이미 도감에 [{new_name}]이(가) 등록되어 있습니다. 다른 이름을 사용해 주세요.")
            else:
                safe_name = re.sub(r'[\\/*?:"<>|]', "", new_name)
                img_filename = f"{safe_name}.png"
                dest_file_path = os.path.join(DATA_DIR, img_filename)
                
                if new_img is not None:
                    with open(dest_file_path, "wb") as f:
                        f.write(new_img.getbuffer())
                else:
                    img_filename = "none.png"
                    
                new_row = pd.DataFrame([{
                    "fish_name": new_name, "min_ph": new_ph[0], "max_ph": new_ph[1], 
                    "min_temp": new_temp[0], "max_temp": new_temp[1], "adult_size": new_size,
                    "aggression": new_agg, "pollution_factor": new_poll, "difficulty": new_diff,
                    "description": new_desc, "image_path": img_filename, "is_custom": 1 
                }])
                
                st.session_state.db_fishes = pd.concat([st.session_state.db_fishes, new_row], ignore_index=True)
                st.session_state.db_fishes.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
                st.success(f"🎉 {new_name} 도감에 열대어가 나만의 데이터로 안전하게 추가되었습니다!")
                st.rerun()

# ==========================================
# 3. 나만의 어항 만들기
# ==========================================
elif menu == "📐 나만의 어항 만들기":
    st.header("🛠️ 내 수조 환경 설정")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📐 어항 및 장비 규격")
        st.caption("💡 추천 **평균 수조 크기는 90×45×45cm** 이며, 가정집에서 커버 가능한 **현실적인 최대 한계는 240×90×90cm** 입니다.")
        
        w = st.number_input("가로 길이 (Width cm)", min_value=15, max_value=240, value=st.session_state.my_tank['w'])
        l = st.number_input("세로 길이 (Length cm)", min_value=15, max_value=90, value=st.session_state.my_tank['l'])
        h = st.number_input("높이 (Height cm)", min_value=15, max_value=90, value=st.session_state.my_tank['h'])
        
        filter_options = {
            "무여과 (여과기 없음)": 0.2,
            "스펀지 여과기 (기본/소형)": 0.5,
            "걸이식 여과기 (중형/미관우수)": 0.8,
            "상면/저면 여과기 (여과재 다량)": 1.2,
            "외부 여과기 (대형/최고효율)": 1.6
        }
        current_filter_idx = list(filter_options.keys()).index(st.session_state.my_tank.get('filter_name', "스펀지 여과기 (기본/소형)")) if st.session_state.my_tank.get('filter_name') in filter_options else 1
        selected_filter = st.selectbox("여과기 종류 선택", list(filter_options.keys()), index=current_filter_idx)
        
        setup_date = st.date_input("🗓️ 생물 투입일 (물잡이 종료일)", value=st.session_state.setup_date)
        st.caption("💡 보편적으로 어항 세팅 후 3~4주 정도 여과기를 돌리며 '물잡이'를 합니다. 위 날짜는 물잡이가 완전히 끝난 후 **첫 생물을 투입하는 날짜**로 선택해주세요.")
        
        st.session_state.my_tank = {"w": w, "l": l, "h": h, "filter_name": selected_filter, "filter_mult": filter_options[selected_filter]}
        st.session_state.setup_date = setup_date
        
        vol_L = (w * l * h) / 1000
        st.info(f"💧 **현재 수조 총 용량:** 약 {vol_L:,.1f} 리터 (L)")
        
    with col2:
        st.subheader("🧊 수조 시각화")
        scale = 2
        box_w, box_h = w * scale, h * scale
        st.markdown(f"""
        <div style="display:flex; justify-content:center; align-items:center; height: 300px;">
            <div class="tank-box" style="width:{box_w}px; height:{box_h}px; max-width:100%;">
                {w} x {l} x {h} cm
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    c_title, c_btn1, c_btn2 = st.columns([2, 1, 1])
    with c_title: st.subheader("🐟 입양할 열대어 선택")
    
    df = st.session_state.db_fishes
    for name in df['fish_name']:
        if f"adopt_{name}" not in st.session_state:
            st.session_state[f"adopt_{name}"] = st.session_state.my_fishes.get(name, 0)
            
    with c_btn1:
        if st.button("🎲 안전 조합 랜덤 생성", type="primary", use_container_width=True):
            peaceful_fishes = df[df['aggression'] <= 4]
            if not peaceful_fishes.empty:
                for name in df['fish_name']:
                    st.session_state[f"adopt_{name}"] = 0
                
                max_safe_bioload = (vol_L * filter_options[selected_filter]) * 0.7 
                chosen_species = peaceful_fishes.sample(n=min(3, len(peaceful_fishes)))
                for _, row in chosen_species.iterrows():
                    name = row['fish_name']
                    factor = float(row['adult_size']) * float(row['pollution_factor'])
                    max_count = int((max_safe_bioload / len(chosen_species)) / factor)
                    if max_count > 0:
                        st.session_state[f"adopt_{name}"] = random.randint(1, min(10, max_count))
                st.rerun()
                
    with c_btn2:
        if st.button("🔄 전체 수량 초기화", use_container_width=True):
            st.session_state.my_fishes = {}
            for name in df['fish_name']:
                st.session_state[f"adopt_{name}"] = 0
            st.rerun()

    temp_selections = {}
    cols = st.columns(5)
    for idx, row in df.iterrows():
        with cols[idx % 5]:
            with st.container(border=True):
                name = row['fish_name']
                st.markdown(f"**{name}**")
                img_path = os.path.join(DATA_DIR, os.path.basename(row['image_path']))
                if os.path.exists(img_path): st.image(img_path, use_container_width=True)
                else: st.image("https://via.placeholder.com/300x200.png?text=No+Image", use_container_width=True)
                temp_selections[name] = st.number_input("입양 수량", min_value=0, max_value=100, key=f"adopt_{name}")
                 
    if st.button("💾 선택한 조합 저장하기", use_container_width=True, type="primary"):
        st.session_state.my_fishes = {k: v for k, v in temp_selections.items() if v > 0}
        st.toast("✅ 어항 세팅이 완료되었습니다! 다음 탭에서 생태계 밸런스를 확인하세요.")
        st.rerun()

    st.markdown("### 🛒 현재 내 어항 입양 목록")
    if st.session_state.my_fishes:
        pills_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; padding: 10px 0;'>"
        for k, v in st.session_state.my_fishes.items():
            pills_html += f"<span style='background-color:#E8F0FE; color:#1967D2; padding:5px 15px; border-radius:20px; font-weight:bold; white-space:nowrap;'>{k} {v}마리</span>"
        pills_html += "</div>"
        st.markdown(pills_html, unsafe_allow_html=True)
    else:
        st.caption("아직 선택된 열대어가 없습니다. 마릿수를 올리고 저장 버튼을 눌러주세요.")

# ==========================================
# 4. 생태계 시뮬레이터
# ==========================================
elif menu == "🧮 생태계 시뮬레이터":
    st.header("🧮 생태계 밸런스 시뮬레이터")
    
    st.info("""
    **💡 생태계 밸런스(Bioload)란 무엇인가요?**  
    어항은 하나의 작은 지구입니다. 물고기가 먹이를 먹고 배출하는 **오염 물질의 총량**을 수조의 **물의 양**과 **여과기의 성능**이 감당할 수 있어야 생태계가 유지됩니다.
    이 시뮬레이터는 입양하신 **[물고기 크기 × 오염 가중치 × 마릿수]** 로 발생하는 총 오염도를 계산하고, 이를 현재 설정하신 **[어항의 물 용량(L) × 여과기 성능]** 으로 안전하게 감당할 수 있는지 자동으로 진단해 드립니다.
    """)
    
    tank = st.session_state.my_tank
    vol_L = (tank['w'] * tank['l'] * tank['h']) / 1000
    filter_mult = tank.get('filter_mult', 1.0)
    max_capacity = vol_L * filter_mult
    
    df = st.session_state.db_fishes
    
    filter_options = {
        "무여과 (여과기 없음)": 0.2, "스펀지 여과기 (기본/소형)": 0.5, 
        "걸이식 여과기 (중형/미관우수)": 0.7, "상면/저면 여과기 (여과재 다량)": 1.1, 
        "외부 여과기 (대형/최고효율)": 1.7
    }
    
    total_bioload = 0
    worst_fish = None
    max_pollution_impact = 0
    
    for name, count in st.session_state.my_fishes.items():
        fish_data = df[df['fish_name'] == name].iloc[0]
        impact = count * float(fish_data['adult_size']) * float(fish_data['pollution_factor'])
        total_bioload += impact
        if impact > max_pollution_impact:
            max_pollution_impact = impact
            worst_fish = name
                
    st.divider()
    c1, c2 = st.columns(2)
    with c1: 
        st.metric("현재 수조가 감당 가능한 최대 오염도", f"{max_capacity:,.1f} 점", delta=f"{tank.get('filter_name')} 적용됨", delta_color="normal")
    with c2: 
        st.metric(
            label="우리 어항의 실제 생물 오염도", 
            value=f"{total_bioload:,.1f} 점", 
            delta=f"{total_bioload - max_capacity:,.1f} 초과" if total_bioload > max_capacity else "안전", 
            delta_color="inverse" if total_bioload > max_capacity else "normal"
        )

    if total_bioload == 0:
        st.warning("어항이 비어있습니다. 이전 페이지에서 열대어를 입양해주세요.")
    elif total_bioload <= max_capacity:
        st.success("🎉 완벽합니다! 현재 어항 크기와 여과기 성능으로 모든 물고기들이 쾌적하게 살아갈 수 있습니다.")
    else:
        st.error(f"⚠️ 과밀 상태입니다! 여과력이 부족해 어항 물이 빠르게 썩게 됩니다.")
        
        fish_data = df[df['fish_name'] == worst_fish].iloc[0]
        one_fish_impact = float(fish_data['adult_size']) * float(fish_data['pollution_factor'])
        excess_bioload = total_bioload - max_capacity
        reduce_count = int(np.ceil(excess_bioload / max(one_fish_impact, 0.1)))
        
        st.markdown(f"### 🚑 해결 솔루션 제안")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        # 솔루션 A: 다이어트
        with col_btn1:
            st.info(f"**해결책 A: 개체수 다이어트**\n\n오염을 가장 많이 유발하는 **[{worst_fish}]** 을(를) **{reduce_count}마리** 줄입니다.")
            if st.button("🐟 해결책 A 적용", use_container_width=True):
                st.session_state.my_fishes[worst_fish] = max(0, st.session_state.my_fishes[worst_fish] - reduce_count)
                for key in st.session_state.keys():
                    if key.startswith(f"adopt_{worst_fish}"):
                        st.session_state[key] = max(0, st.session_state[key] - reduce_count)
                st.rerun()
                
        # 솔루션 B: 여과기 업그레이드
        with col_btn2:
            required_mult = total_bioload / max(vol_L, 1)
            possible_filters = {k: v for k, v in filter_options.items() if v >= required_mult and v > filter_mult}
            
            if possible_filters:
                best_filter = list(possible_filters.keys())[0]
                st.info(f"**해결책 B: 여과기 업그레이드**\n\n여과기를 **[{best_filter}]** (으)로 변경하여 밸런스를 맞춥니다.")
                if st.button("🔌 해결책 B 적용", use_container_width=True):
                    st.session_state.my_tank['filter_name'] = best_filter
                    st.session_state.my_tank['filter_mult'] = filter_options[best_filter]
                    st.rerun()
            else:
                st.warning("**해결책 B: 여과기 업그레이드 (불가)**\n\n최고 효율의 여과기를 사용 중이거나, 변경만으로는 부족합니다.")
                st.button("🔌 적용 불가", disabled=True, use_container_width=True, key="btn_b_disabled")

        # 솔루션 C: 수조 크기 업그레이드
        with col_btn3:
            required_w = int(np.ceil((total_bioload * 1000) / (tank['l'] * tank['h'] * filter_mult)))
            
            if required_w > 240:
                st.error(f"**해결책 C: 수조 확장 (불가)**\n\n필요한 가로 길이가 **{required_w}cm** 로 가정집 한계(240cm)를 넘습니다.")
                st.button("📐 적용 불가", disabled=True, use_container_width=True, key="btn_c_disabled")
            else:
                st.info(f"**해결책 C: 수조 크기 확장**\n\n현재 마릿수를 유지하려면 어항 가로 길이를 **{required_w}cm** 로 더 크게 변경합니다.")
                if st.button("📐 해결책 C 적용", use_container_width=True):
                    st.session_state.my_tank['w'] = required_w
                    st.rerun()

    st.divider()
    st.subheader("📊 생태계 분석 및 예측 시각화")
    c_bar, c_scatter = st.columns(2)

    with c_bar:
        st.markdown("**수조 여과 한계치 vs 현재 오염도**")
        bar_data = pd.DataFrame({"Tank": ["My Tank"], "Bioload Score": [total_bioload]})
        
        max_y_value = max(max_capacity, total_bioload) * 1.1
        bar_chart = alt.Chart(bar_data).mark_bar(size=80).encode(
            x=alt.X('Tank', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Bioload Score', title='Bioload Score', scale=alt.Scale(domain=[0, max_y_value])),
            color=alt.condition(
                alt.datum['Bioload Score'] > max_capacity,
                alt.value('coral'), alt.value('lightgreen')
            )
        )
        
        limit_line = alt.Chart(pd.DataFrame({'Limit': [max_capacity]})).mark_rule(
            color='red', strokeDash=[5, 5]
        ).encode(y='Limit')
        
        limit_text = alt.Chart(pd.DataFrame({'Tank': ['My Tank'], 'Limit': [max_capacity]})).mark_text(
            align='center', baseline='bottom', dy=-5, color='red', fontWeight='bold'
        ).encode(
            x='Tank', y='Limit', text=alt.value(f'여과 한계 (Max: {max_capacity:.1f})')
        )
        st.altair_chart(bar_chart + limit_line + limit_text, use_container_width=True)

    with c_scatter:
        st.markdown("**서식 환경 (pH & 수온) 교집합**")
        st.caption("산점도 상의 거리가 가까울수록 서식 환경이 유사하여 합사에 유리합니다.")
        if len(st.session_state.my_fishes) > 0:
            adopted_fishes = df[df['fish_name'].isin(st.session_state.my_fishes.keys())]
            chart_data = pd.DataFrame({
                'Fish': adopted_fishes['fish_name'],
                'Avg_pH': (adopted_fishes['min_ph'] + adopted_fishes['max_ph']) / 2,
                'Avg_Temp': (adopted_fishes['min_temp'] + adopted_fishes['max_temp']) / 2
            })
            scatter_fig = alt.Chart(chart_data).mark_circle(size=200, color='#4A90E2', opacity=0.8).encode(
                x=alt.X('Avg_pH', scale=alt.Scale(domain=[5.0, 9.0]), title="평균 pH (산성 ~ 알칼리성)"),
                y=alt.Y('Avg_Temp', scale=alt.Scale(domain=[20, 32]), title="평균 수온 (20~32°C)"),
                tooltip=['Fish', 'Avg_pH', 'Avg_Temp'] 
            ).properties(height=400)
            st.altair_chart(scatter_fig, use_container_width=True)
            
    st.divider()
    st.subheader("📈 생물 투입 후 30일 수질(질산염) 악화 예측")
    st.caption("생물 투입일 기준으로 오염 물질이 누적되는 시뮬레이션입니다. 질산염 50ppm 도달 시 환수(물갈이)가 필수적입니다.")

    total_pollution = total_bioload if total_bioload > 0 else 0.1
    daily_increase = (total_pollution / max(max_capacity, 1)) * 5.0
    days = np.arange(1, 31) 
    no3_levels = np.array([5.0 + (daily_increase * d * (1.05 ** d)) for d in days]) 

    chart_data_no3 = pd.DataFrame({'NO3 농도 (ppm)': no3_levels}, index=days)
    st.line_chart(chart_data_no3)
    
    exceed_indices = np.where(no3_levels >= 50)[0]
    if len(exceed_indices) > 0:
        danger_day = exceed_indices[0] + 1
        danger_date = st.session_state.setup_date + timedelta(days=int(danger_day))
        st.error(f"🚨 **시뮬레이션 결과:** 생물 투입 후 **{danger_day}일 차 ({danger_date.strftime('%m월 %d일')})에** 위험치(50ppm)를 돌파합니다! 이 날짜 이전에 반드시 물의 30%를 환수해주세요.")
    else:
        st.success("✨ **시뮬레이션 결과:** 한 달 동안 위험 수치(50ppm)에 도달하지 않는 아주 안정적인 어항입니다. 2주에 한 번씩만 가볍게 환수해주시면 됩니다!")

# ==========================================
# 5. 가상 아쿠아리움 & 대시보드
# ==========================================
elif menu == "🔮 가상 아쿠아리움":
    st.header("🔮 가상 아쿠아리움 & 수질 대시보드")
    
    tank = st.session_state.my_tank
    vol_L = (tank['w'] * tank['l'] * tank['h']) / 1000
    max_capacity = vol_L * tank.get('filter_mult', 1.0)
    
    total_bioload = 0
    df = st.session_state.db_fishes
    for name, count in st.session_state.my_fishes.items():
        if count > 0:
            fish_data = df[df['fish_name'] == name].iloc[0]
            total_bioload += count * float(fish_data['adult_size']) * float(fish_data['pollution_factor'])
            
    total_pollution = total_bioload if total_bioload > 0 else 0.1
    daily_increase = (total_pollution / max(max_capacity, 1)) * 5.0
    days = np.arange(1, 31) 
    no3_levels = np.array([5.0 + (daily_increase * d * (1.05 ** d)) for d in days]) 
    exceed_indices = np.where(no3_levels >= 50)[0]
    
    m1, m2, m3 = st.columns(3)
    elapsed_days = (datetime.today().date() - st.session_state.setup_date).days
    
    if elapsed_days < 1:
        current_no3 = 5.0 
    elif elapsed_days > 30:
        current_no3 = no3_levels[-1]
    else:
        current_no3 = no3_levels[elapsed_days - 1]

    if current_no3 < 20:
        current_status = "✨ 아주 맑음"
        delta_color = "normal"
    elif current_no3 < 50:
        current_status = "⚠️ 오염 진행 중"
        delta_color = "off"
    else:
        current_status = "🚨 즉시 환수 요망"
        delta_color = "inverse"
        
    m1.metric(label="현재 수조 수질 상태", value=current_status, delta=f"추정 질산염: {current_no3:.1f}ppm", delta_color=delta_color)
    m2.metric(label="생물 투입 후 경과일", value=f"D+{elapsed_days}일" if elapsed_days >= 0 else f"투입 전 (D{elapsed_days})")
    
    if len(exceed_indices) > 0:
        danger_day = exceed_indices[0] + 1
        danger_date = st.session_state.setup_date + timedelta(days=int(danger_day))
        m3.metric(label="🚨 위험 수치 예상일", value=f"투입 후 {danger_day}일 차", delta=f"{danger_date.strftime('%Y-%m-%d')}", delta_color="inverse")
    else:
        m3.metric(label="권장 환수 주기", value="2주 1회", delta="안전")

    st.subheader("🌊 내 방 안의 2D 물멍 수족관")
    st.info("🖱️ **어항 속을 마우스로 클릭해보세요!** 갈색 사료가 떨어지면 물고기들이 밥을 먹으러 다가옵니다.")
    
    fish_js_array = []
    df = st.session_state.db_fishes
    
    for name, count in st.session_state.my_fishes.items():
        if count > 0:
            row = df[df['fish_name'] == name].iloc[0]
            img_path = os.path.join(DATA_DIR, os.path.basename(row['image_path']))
            b64_img = get_image_base64(img_path)
            size = min(float(row['adult_size']) * 8 + 20, 280)
            
            for _ in range(count):
                speed = random.uniform(0.5, 2.0)
                y_pos = random.randint(50, 250)
                fish_js_array.append(f"{{src: '{b64_img}', size: {size}, x: {random.randint(0,800)}, y: {y_pos}, speed: {speed}, direction: 1}}")

    js_fishes = "[\n" + ",\n".join(fish_js_array) + "\n]"
    bg_path = os.path.join(DATA_DIR, "어항.png")
    bg_b64 = get_image_base64(bg_path)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; overflow:hidden; background-color:#E0F7FA;">
        <canvas id="aquarium" style="width: 100%; height: 350px; display: block;"></canvas>
        <script>
            const canvas = document.getElementById('aquarium');
            const ctx = canvas.getContext('2d');
            
            function resize() {{
                canvas.width = canvas.clientWidth;
                canvas.height = canvas.clientHeight;
            }}
            window.addEventListener('resize', resize);
            resize(); 
            
            const bgImg = new Image();
            bgImg.src = '{bg_b64}';

            function drawBackground() {{
                if (bgImg.complete && bgImg.src && bgImg.src.length > 20) {{
                    ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);
                }} else {{
                    ctx.fillStyle = "#E0F7FA";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                }}
            }}

            const fishData = {js_fishes};
            const fishes = [];
            const foods = []; 

            fishData.forEach(data => {{
                const img = new Image();
                img.src = data.src;
                fishes.push({{...data, img: img}});
            }});
            
            canvas.addEventListener('click', function(e) {{
                const rect = canvas.getBoundingClientRect();
                const x = (e.clientX - rect.left) * (canvas.width / rect.width);
                const y = (e.clientY - rect.top) * (canvas.height / rect.height);
                foods.push({{x: x, y: y}});
            }});

            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                drawBackground();
                
                ctx.fillStyle = '#654321';
                for(let i = foods.length - 1; i >= 0; i--) {{
                    foods[i].y += 0.5;
                    ctx.beginPath();
                    ctx.arc(foods[i].x, foods[i].y, 2, 0, Math.PI * 2);
                    ctx.fill();
                    
                    if(foods[i].y > canvas.height - 10) {{
                        foods.splice(i, 1);
                    }}
                }}

                fishes.forEach(fish => {{
                    if (foods.length > 0) {{
                        let nearest = null;
                        let minDist = Infinity;
                        let foodIndex = -1;
                        
                        for(let i=0; i<foods.length; i++) {{
                            let dx = foods[i].x - (fish.x + fish.size/2);
                            let dy = foods[i].y - (fish.y + fish.size/2);
                            let dist = Math.sqrt(dx*dx + dy*dy);
                            if(dist < minDist) {{
                                minDist = dist;
                                nearest = foods[i];
                                foodIndex = i;
                            }}
                        }}
                        
                        if(nearest) {{
                            let dx = nearest.x - (fish.x + fish.size/2);
                            let dy = nearest.y - (fish.y + fish.size/2);
                            let angle = Math.atan2(dy, dx);
                            fish.x += Math.cos(angle) * (fish.speed * 1.5);
                            fish.y += Math.sin(angle) * (fish.speed * 1.5);
                            fish.direction = dx > 0 ? 1 : -1;
                            
                            if(minDist < fish.size/3) {{
                                foods.splice(foodIndex, 1);
                            }}
                        }}
                    }} else {{
                        fish.x += fish.speed * fish.direction;
                        if (fish.x > canvas.width - fish.size || fish.x < 0) {{
                            fish.direction *= -1;
                        }}
                        if(fish.y < 20) fish.y = 20;
                        if(fish.y > canvas.height - fish.size - 20) fish.y = canvas.height - fish.size - 20;
                    }}

                    ctx.save();
                    ctx.translate(fish.x + fish.size/2, fish.y + fish.size/2);
                    ctx.scale(fish.direction, 1);
                    if(fish.img.complete && fish.img.width > 0) {{
                        let aspectRatio = fish.img.height / fish.img.width;
                        let drawWidth = fish.size;
                        let drawHeight = fish.size * aspectRatio;
                        ctx.drawImage(fish.img, -drawWidth/2, -drawHeight/2, drawWidth, drawHeight);
                    }}
                    ctx.restore();
                }});
                requestAnimationFrame(animate);
            }}
            setTimeout(animate, 500);
        </script>
    </body>
    </html>
    """
    
    if not st.session_state.my_fishes:
        st.warning("수족관이 비어있습니다. '나만의 어항 만들기'에서 물고기를 입양해 주세요!")
    else:
        components.html(html_code, height=360) 
        st.caption("🎵 편안한 수족관 ASMR과 함께 물멍을 즐겨보세요.")
        audio_path = os.path.join(DATA_DIR, "fishtank.mp3")
        if os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mpeg", loop=True)
        else:
            st.warning("fishtank.mp3 파일을 찾을 수 없습니다. (data 폴더 내 확인)")
        
    st.divider()
    
    st.subheader("🗺️ 대한민국 대표 아쿠아리움 지도")
    st.caption("물멍의 스케일을 키우고 싶으신가요? 주말에 가족, 연인과 함께 전국 곳곳의 대형 아쿠아리움을 방문해 보세요!")
    
    korea_aquariums = pd.DataFrame({
        'lat': [37.5125, 37.5139, 37.2384, 35.1587, 34.7451, 33.4305, 37.6653],
        'lon': [127.0588, 127.1044, 127.0610, 129.1604, 127.7469, 126.9279, 126.7543],
        'name': [
            '코엑스 아쿠아리움 (서울)', '롯데월드 아쿠아리움 (서울)', '아쿠아플라넷 광교 (경기)', 
            '씨라이프 (부산)', '아쿠아플라넷 (여수)', '아쿠아플라넷 (제주)', '아쿠아플라넷 (일산)'
        ]
    })
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=korea_aquariums,
        get_position="[lon, lat]",
        get_fill_color=[255, 50, 50, 200], 
        get_radius=1800, 
        pickable=True,    
    )

    view_state = pdk.ViewState(
        latitude=36.0,      
        longitude=127.7,    
        zoom=6.2,           
        pitch=0,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style='light', 
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{name}"} 
        )
    )
