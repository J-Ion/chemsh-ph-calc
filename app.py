# 터미널에서 실행 시 안내
# streamlit run /Users/minjunkwak/Desktop/ChemSh/app.py

import streamlit as st
import math

st.title("다양한 산/염기 지원 pH 계산기")

st.markdown("""
사용자가 산과 염기 종류를 선택하고 농도, 부피를 입력하면 혼합 용액의 pH를 계산합니다.
현재 강산: HCl, HNO3, H2SO4 / 약산: CH3COOH, HF
강염기: NaOH, KOH, Ba(OH)2 / 약염기: NH3, CH3NH2 지원.

⚠️ `streamlit run app.py`로 실행하세요.
""")

# 산/염기 데이터
acid_data = {
    "강산 (HCl)": None,
    "강산 (HNO3)": None,
    "강산 (H2SO4)": None,
    "약산 (CH3COOH, Ka=1.8e-5)": 1.8e-5,
    "약산 (HF, Ka=6.6e-4)": 6.6e-4
}

base_data = {
    "강염기 (NaOH)": None,
    "강염기 (KOH)": None,
    "강염기 (Ba(OH)2)": None,
    "약염기 (NH3, Kb=1.8e-5)": 1.8e-5,
    "약염기 (CH3NH2, Kb=4.4e-4)": 4.4e-4
}

st.header("산 입력")
acid_type = st.selectbox("산 종류", list(acid_data.keys()))
acid_conc = st.number_input("산 농도 [mol/L]", min_value=0.0, step=0.1)
acid_vol = st.number_input("산 부피 [mL]", min_value=0.0, step=1.0)

st.header("염기 입력")
base_type = st.selectbox("염기 종류", list(base_data.keys()))
base_conc = st.number_input("염기 농도 [mol/L]", min_value=0.0, step=0.1)
base_vol = st.number_input("염기 부피 [mL]", min_value=0.0, step=1.0)

if st.button("pH 계산"):
    acid_mol = acid_conc * (acid_vol / 1000)
    base_mol = base_conc * (base_vol / 1000)
    if base_type == "강염기 (Ba(OH)2)":
        base_mol *= 2  # Ba(OH)2는 2배 OH- 발생
    total_vol = (acid_vol + base_vol) / 1000

    if total_vol == 0:
        st.error("총 부피가 0입니다.")
    else:
        net_H = 0
        Ka = acid_data[acid_type]
        if Ka is None:
            net_H += acid_mol
        else:
            H_approx = math.sqrt(Ka * acid_mol) if acid_mol > 0 else 0
            net_H += H_approx

        net_OH = 0
        Kb = base_data[base_type]
        if Kb is None:
            net_OH += base_mol
        else:
            OH_approx = math.sqrt(Kb * base_mol) if base_mol > 0 else 0
            net_OH += OH_approx

        if net_H > net_OH:
            h_conc = (net_H - net_OH) / total_vol
            pH = -math.log10(h_conc) if h_conc > 0 else 7.0
        elif net_OH > net_H:
            oh_conc = (net_OH - net_H) / total_vol
            pOH = -math.log10(oh_conc) if oh_conc > 0 else 7.0
            pH = 14 - pOH
        else:
            pH = 7.0

        st.success(f"계산된 pH: {pH:.2f}")
