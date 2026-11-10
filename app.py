import streamlit as st
from openai import OpenAI
import time
import re
import base64
import pandas as pd
from datetime import datetime
import html
import random

# 1. 网页基础设置
st.set_page_config(page_title="和云风 AI营销传播助手", page_icon="✨", layout="wide")


# 2. 读取本地图片并转为 Base64
@st.cache_data(show_spinner=False)
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""


bin_str = get_base64_of_bin_file('bg.webp')
logo_str = get_base64_of_bin_file('logo.png')

# ==================== Q弹玻璃胶囊 UI 注入 ====================
st.markdown(f"""
<style>
#MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
[data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(rgba(5, 7, 12, 0.65), rgba(5, 7, 12, 0.85)), url("data:image/webp;base64,{bin_str}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) saturate(150%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
}}
.stMarkdown, p, h1, h2, h3, h4, label, span {{ color: #f8fafc !important; }}

/* 强制消除所有原生的白色分割线 hr */
hr {{
    border-color: rgba(255, 255, 255, 0.1) !important;
    background-color: transparent !important;
}}

/* 修复 Toast */
div[data-testid="stToast"], [data-baseweb="toast"] {{
    background-color: #262730 !important; border: 1px solid rgba(255,255,255,0.2) !important;
}}
div[data-testid="stToast"] *, [data-baseweb="toast"] * {{ color: white !important; }}

.bubble-title {{
    display: inline-flex; align-items: center; background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px); padding: 12px 35px; border-radius: 50px;
    border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255,255,255,0.5);
    color: white; font-weight: 800; margin-bottom: 20px; transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}}
.bubble-title:hover {{ transform: scale(1.05, 0.95); background: rgba(255, 255, 255, 0.12); }}
.bubble-subtitle {{
    display: inline-block; background: rgba(255, 255, 255, 0.06); backdrop-filter: blur(10px);
    padding: 8px 25px; border-radius: 30px; border: 1px solid rgba(255, 255, 255, 0.2);
    color: #e2e8f0; font-size: 1.1rem; margin-bottom: 40px;
}}
.stMarkdown h3 {{
    display: inline-block; background: rgba(255, 255, 255, 0.08) !important; backdrop-filter: blur(10px);
    padding: 10px 20px !important; border-radius: 30px !important; border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1), inset 0 1px 1px rgba(255,255,255,0.4) !important; margin-bottom: 15px !important;
}}

/* 修复输入框 */
[data-testid="stWidgetLabel"] p {{
    display: inline-block; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(5px);
    padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.15);
    font-size: 0.95rem; color: #f8fafc !important; margin-bottom: 5px;
}}
.stTextInput input, .stTextArea textarea {{
    border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.4) !important; 
    background-color: rgba(40, 45, 60, 0.7) !important; color: #ffffff !important; 
    backdrop-filter: blur(10px) !important; transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.2) !important;
}}
.stTextInput > div, .stTextArea > div {{ background-color: transparent !important; border: none !important; box-shadow: none !important; }}
input::placeholder, textarea::placeholder {{ color: rgba(255, 255, 255, 0.4) !important; }}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border: 1px solid rgba(139, 92, 246, 0.8) !important; box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3) !important;
    background-color: rgba(50, 55, 75, 0.8) !important;
}}

/* 修复下拉框和单选框 */
div[data-baseweb="select"] > div {{
    background-color: rgba(40, 45, 60, 0.7) !important; color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}}
div[data-baseweb="select"] div {{ color: white !important; }}
ul[data-baseweb="menu"] {{ background-color: #262730 !important; }}
ul[data-baseweb="menu"] li {{ color: white !important; }}
div[data-testid="stRadio"] label {{ color: white !important; }}

/* 修复按钮 */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {{
    background: rgba(255, 255, 255, 0.08) !important; backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important; border-radius: 50px !important; 
    color: white !important; font-weight: 600 !important; padding: 10px 24px !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15), inset 0 1px 1px rgba(255,255,255,0.5) !important;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {{
    transform: scale(1.08, 0.92) !important; background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2), inset 0 2px 5px rgba(255,255,255,0.8) !important;
}}

/* Tabs 胶囊导航 */
.stTabs [data-baseweb="tab-list"] {{ gap: 15px; background-color: transparent; border-bottom: none; }}
.stTabs [data-baseweb="tab"] {{
    border-radius: 50px !important; background-color: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important; padding: 10px 25px !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important; 
    border: 1px solid rgba(255, 255, 255, 0.15) !important; color: #cbd5e1 !important; 
    font-weight: 500 !important; box-shadow: inset 0 1px 1px rgba(255,255,255,0.3) !important;
}}
.stTabs [data-baseweb="tab"]:hover {{ transform: scale(1.05, 0.95) !important; background-color: rgba(255, 255, 255, 0.1) !important; }}
.stTabs [aria-selected="true"] {{
    background: rgba(255, 255, 255, 0.15) !important; color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), inset 0 1px 2px rgba(255,255,255,0.6) !important;
}}

/* 容器卡片 */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px) saturate(150%) !important;
    border-radius: 24px !important; border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 2px rgba(255,255,255,0.3) !important;
    transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    transform: scale(1.01, 0.99) !important; border-color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2), inset 0 1px 2px rgba(255,255,255,0.5) !important;
    background: rgba(255, 255, 255, 0.08) !important;
}}

/* 🌟 暴力修复代码块 */
div[data-testid="stCodeBlock"], div[data-testid="stCodeBlock"] > div, div[data-testid="stCodeBlock"] pre {{
    background-color: #1a1c24 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}}
div[data-testid="stCodeBlock"] *, div[data-testid="stCodeBlock"] code {{
    color: #e2e8f0 !important;
}}

/* 修复表格白线 */
.custom-table-container {{
    width: 100%; overflow-x: auto; border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.15); background: rgba(255, 255, 255, 0.03);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}
.custom-table {{
    width: 100%; table-layout: fixed; border-collapse: collapse !important;
    word-wrap: break-word; white-space: normal; border: none !important;
}}
.custom-table th {{
    background: rgba(255, 255, 255, 0.1); color: #f8fafc; padding: 12px 10px; text-align: left;
    font-weight: bold; border: none !important; 
    border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important; word-wrap: break-word;
}}
.custom-table td {{
    padding: 12px 10px; 
    border: none !important; 
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; 
    color: #e2e8f0; line-height: 1.6; word-wrap: break-word; white-space: normal;
}}
.custom-table tr:last-child td {{ border-bottom: none !important; }}
.custom-table tr:hover {{ background: rgba(255,255,255,0.05); }}

.highlight-hit {{
    background-color: rgba(239, 68, 68, 0.4); color: #fca5a5; border: 1px solid #ef4444;
    padding: 2px 6px; border-radius: 6px; font-weight: bold;
}}
.op-suggestion {{
    background: rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; border-left: 4px solid #8b5cf6; margin-top: 15px;
}}
@media (max-width: 768px) {{
  .bubble-title {{ font-size: 1.8rem !important; padding: 10px 20px !important; gap: 10px !important; }}
  .bubble-title img {{ width: 56px !important; }}
  .bubble-subtitle {{ font-size: 0.9rem !important; }}
  .stTabs [data-baseweb="tab"] {{ padding: 8px 14px !important; font-size: 0.85rem !important; }}
}}
</style>
""", unsafe_allow_html=True)

# 3. 获取 API Key & 工具函数
API_KEY = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"
ERR_PREFIX = "\n\n> ⚠️ 生成中断："

TEMP_SCRIPT = 0.7
TEMP_EDIT = 0.5
TEMP_DIAG = 0.6
TEMP_LEGAL = 0.3


def friendly_error(e):
    m = str(e)
    if "401" in m or "Authentication" in m: return "API Key 无效，请检查 secrets.toml"
    if "429" in m: return "请求过于频繁，请 30 秒后重试"
    if "timeout" in m.lower(): return "请求超时，请检查网络"
    return f"发生错误：{m}"


def stream_chat(messages, temperature):
    try:
        res = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=temperature, stream=True
        )
        for chunk in res:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"{ERR_PREFIX}{friendly_error(e)}"


# ==================== 4. 状态初始化 ====================
_DEFAULTS = {
    "logged_in": False, "user_phone": "", "review_result": "",
    "last_script": "", "op_advice": "", "dir_input": "",
    "review_input": "", "sms_code": "",
    "rule_hits": [], "ai_calls": 0,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ==================== 5. 组件渲染函数 ====================
def render_storyboard(last_script):
    st.markdown("### 完美换行分镜表")
    st.caption("🤝 **人机协作**：AI 生成初稿 → 展开下方抽屉 **双击单元格** 即可修改 → 导出执行清单")
    try:
        def _is_md_separator(line):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            non_empty = [c for c in cells if c]
            return bool(non_empty) and all(re.fullmatch(r':?-{3,}:?', c) for c in non_empty)

        table_text = ""
        for line in last_script.split('\n'):
            s = line.strip()
            if s.startswith('|') and not _is_md_separator(s):
                table_text += line + "\n"

        if table_text:
            lines = table_text.strip().split('\n')
            header = [h.strip() for h in lines[0].strip('|').split('|')]
            data = []
            for l in lines[1:]:
                row = [c.strip() for c in l.strip('|').split('|')]
                if len(row) == len(header):
                    data.append(row)
                elif len(row) > len(header):
                    merged = row[: len(header) - 1] + [" | ".join(row[len(header) - 1:])]
                    data.append(merged)

            if not data:
                st.markdown(
                    '<div style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); padding: 15px; border-radius: 12px; color: #fcd34d; margin-bottom: 15px; font-weight: bold;">⚠️ AI 输出的表格格式不完整，已展示原始文本：</div>',
                    unsafe_allow_html=True)
                st.markdown(last_script)
                return

            df = pd.DataFrame(data, columns=header)

            _W = [5, 10, 15, 25, 30, 15]
            colgroup_html = ('<colgroup>' + ''.join(
                f'<col style="width:{w}%">' for w in _W[:len(header)]) + '</colgroup>') if len(header) <= len(
                _W) else ''

            html_table = df.to_html(index=False, classes='custom-table', escape=True, justify='left', border=0)
            html_table = re.sub(r'<table[^>]*>', f'<table class="custom-table">{colgroup_html}', html_table, count=1)

            st.markdown(f'<div class="custom-table-container">{html_table}</div>', unsafe_allow_html=True)

            with st.expander("✏️ 展开以双击修改分镜表 & 导出"):
                config = {}
                if "镜号" in df.columns:
                    numeric = pd.to_numeric(df["镜号"], errors="coerce")
                    if numeric.notna().all():
                        df["镜号"] = numeric.astype(int)
                        config["镜号"] = st.column_config.NumberColumn("镜号", width="small", step=1)
                    else:
                        config["镜号"] = st.column_config.TextColumn("镜号", width="small")
                if "时间" in df.columns: config["时间"] = st.column_config.TextColumn("时间", width="small")
                if "景别与运镜" in df.columns: config["景别与运镜"] = st.column_config.TextColumn("景别与运镜",
                                                                                                  width="small")
                if "画面动作" in df.columns: config["画面动作"] = st.column_config.TextColumn("画面动作",
                                                                                              width="medium")
                if "口播文案" in df.columns: config["口播文案"] = st.column_config.TextColumn("口播文案", width="large")
                if "音效" in df.columns: config["音效"] = st.column_config.TextColumn("音效/BGM", width="medium")

                edited_df = st.data_editor(df, key="script_editor", use_container_width=True, num_rows="dynamic",
                                           column_config=config)

                ts = datetime.now().strftime("%Y%m%d_%H%M")
                csv = edited_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 导出修改后的执行清单 (CSV)", csv, f"执行清单_{ts}.csv", "text/csv",
                                   type="primary", use_container_width=True)
    except Exception as e:
        st.markdown(
            f'<div style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); padding: 15px; border-radius: 12px; color: #fcd34d; margin-bottom: 15px; font-weight: bold;">⚠️ 分镜表结构化失败，已展示原始文本：{e}</div>',
            unsafe_allow_html=True)
        st.markdown(last_script)


# ==================== 登录界面 ====================
if not st.session_state["logged_in"]:
    st.markdown(f"""
    <div style="text-align: center; margin-top: 50px;">
        <div class="bubble-title" style="font-size: 2.8rem; gap: 20px;">
            <img src="data:image/png;base64,{logo_str}" width="110" style="border-radius: 50%; background-color: rgba(255,255,255,0.9); padding: 5px;"> 
            <span>和云风 AI营销传播助手</span>
        </div>
        <br>
        <div class="bubble-subtitle">您的专属 AI 营销增长引擎</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### 手机号快捷登录 / 注册")
            with st.form("login_form", clear_on_submit=False):
                phone = st.text_input("请输入您的手机号", placeholder="请输入 11 位手机号", max_chars=11)
                col_code1, col_code2 = st.columns([2, 1])
                with col_code1:
                    verify_code = st.text_input("请输入验证码", placeholder="输入 4 位验证码", max_chars=4)
                with col_code2:
                    st.write("")
                    st.write("")
                    submit_code = st.form_submit_button("获取验证码", use_container_width=True)

                st.write("")
                submit_login = st.form_submit_button("登录 / 进入系统", type="primary", use_container_width=True)

                if submit_code:
                    if re.match(r"^1[3-9]\d{9}$", phone):
                        random_code = f"{random.randint(0, 9999):04d}"
                        st.session_state["sms_code"] = random_code
                        st.toast(f"验证码已发送！(演示环境码: {random_code})", icon="✅")
                    else:
                        st.toast("请输入正确的手机号！", icon="❌")

                if submit_login:
                    if not phone or not verify_code:
                        # 🌟 替换为纯 HTML 警告框
                        st.markdown(
                            '<div style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); padding: 15px; border-radius: 12px; color: #fcd34d; margin-bottom: 15px; font-weight: bold;">⚠️ 手机号和验证码不能为空哦！</div>',
                            unsafe_allow_html=True)
                    elif not re.match(r"^1[3-9]\d{9}$", phone):
                        st.markdown(
                            '<div style="background-color: rgba(220, 38, 38, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); padding: 15px; border-radius: 12px; color: #fca5a5; margin-bottom: 15px; font-weight: bold;">❌ 手机号格式不正确，请检查！</div>',
                            unsafe_allow_html=True)
                    elif verify_code != st.session_state.get("sms_code"):
                        st.markdown(
                            '<div style="background-color: rgba(220, 38, 38, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); padding: 15px; border-radius: 12px; color: #fca5a5; margin-bottom: 15px; font-weight: bold;">❌ 验证码错误！</div>',
                            unsafe_allow_html=True)
                    else:
                        with st.spinner("正在安全登录..."):
                            time.sleep(0.3)
                            st.session_state["logged_in"] = True
                            st.session_state["user_phone"] = phone[:3] + "****" + phone[-4:]
                            st.rerun()

            st.caption("演示环境：验证码通过右上角悬浮窗展示，生产环境将接入短信服务商。")

        st.markdown("""
        <div style="text-align: center; margin-top: 30px; font-size: 0.9rem; color: rgba(255,255,255,0.6);">
            <p>技术指导：和云风 | 联系邮箱：1620339694@qq.com</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== 主系统 ====================
else:
    with st.sidebar:
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 24px; text-align: center; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.15); backdrop-filter: blur(10px);">
            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, rgba(255,255,255,0.4), rgba(255,255,255,0.1)); margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 30px; color: white; font-weight: bold; border: 1px solid rgba(255,255,255,0.5);">
                👤
            </div>
            <h4 style="color: white; margin-top: 15px; margin-bottom: 5px;">尊贵用户</h4>
            <p style="color: #e2e8f0; font-size: 14px;">{st.session_state['user_phone']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.metric("本次会话 AI 调用", st.session_state["ai_calls"])

        with st.popover("⚙️ 账号设置", use_container_width=True):
            st.write("点击下方按钮退出登录")
            if st.button("退出登录", type="primary", use_container_width=True):
                st.session_state.clear()
                st.rerun()

        st.info("💡 **双引擎驱动**：AI导演 + AI法务。一站式解决普通人创作与合规痛点。")

    # 主界面标题
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 40px; margin-top: 10px;">
        <div class="bubble-title" style="font-size: 3.3rem; gap: 20px; padding: 15px 45px;">
            <img src="data:image/png;base64,{logo_str}" width="120" style="border-radius: 50%; background-color: rgba(255,255,255,0.9); padding: 5px;"> 
            <span>和云风 AI营销传播助手</span>
        </div>
        <br>
        <div class="bubble-subtitle" style="font-size: 1.2rem;">双引擎驱动：结构化分镜生成 & 双层合规审查，让科技普惠每一个创作者。</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["AI 导演：分镜与流水线", "AI 法务：双层合规审查"])

    # ==================== 选项卡 1：分镜生成 ====================
    with tab1:
        with st.container(border=True):
            st.markdown("### 创作参数设置")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                platform = st.selectbox("目标平台", ["抖音", "小红书", "视频号", "B站"])
            with col_p2:
                audience = st.selectbox("目标受众", ["年轻女性", "宝妈群体", "大学生", "职场新人", "中老年群体"])
            with col_p3:
                style = st.radio("视频风格", ["真诚分享", "搞笑剧情", "干货科普", "情感共鸣"], horizontal=True)

            st.markdown("---")
            c_in1, c_in2 = st.columns([4, 1])
            with c_in2:
                if st.button("💡 填入案例", key="demo_dir", use_container_width=True):
                    st.session_state["dir_input"] = "烟台红富士苹果，高山种植，脆甜多汁，现摘现发，助农直供。"
                    st.rerun()

            with c_in1:
                st.text_area("请输入你的产品、门店或想表达的主题：", height=100, key="dir_input",
                             placeholder="例如：烟台红富士苹果，脆甜多汁。")

            if st.button("一键生成爆款分镜", type="primary", use_container_width=True, key="btn_tab3"):
                if not st.session_state.get("dir_input", "").strip():
                    st.markdown(
                        '<div style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); padding: 15px; border-radius: 12px; color: #fcd34d; margin-bottom: 15px; font-weight: bold;">⚠️ 请先输入你的主题哦！</div>',
                        unsafe_allow_html=True)
                else:
                    system_prompt = f"""你是一个拥有千万粉丝的短视频爆款操盘手。请生成分镜脚本。目标平台【{platform}】，受众【{audience}】，风格【{style}】。

【重要】必须在第一个镜头（0-3秒）设置极强的留人钩子。
请严格按以下两部分输出：
第一部分：Markdown表格，包含六列：| 镜号 | 时间 | 景别与运镜 | 画面动作 | 口播文案 | 音效 |
第二部分：在表格下方，写上“【运营建议】”，然后列出：1.黄金3秒钩子；2.爆款标题备选（至少3个）；3.话题标签；4.封面建议。"""
                    try:
                        loading_ph = st.empty()
                        loading_ph.markdown(
                            '<div style="color:#8b5cf6; font-weight:bold; padding: 10px 0;">✍️ AI 导演正在构思分镜，流式输出中...</div>',
                            unsafe_allow_html=True)

                        full_text = st.write_stream(stream_chat([{"role": "system", "content": system_prompt},
                                                                 {"role": "user",
                                                                  "content": f"我的主题是：{st.session_state['dir_input']}"}],
                                                                temperature=TEMP_SCRIPT))
                        loading_ph.empty()

                        is_error = ERR_PREFIX.strip() in full_text
                        if is_error:
                            st.session_state.pop("script_editor", None)
                            st.stop()

                        st.session_state["ai_calls"] += 1

                        if "【运营建议】" in full_text:
                            table_text, op_text = full_text.split("【运营建议】", 1)
                            st.session_state['last_script'] = table_text.strip()
                            st.session_state['op_advice'] = "**【运营建议】**\n" + op_text.strip()
                        else:
                            st.session_state['last_script'] = full_text
                            st.session_state['op_advice'] = ""
                        st.session_state.pop("script_editor", None)

                        time.sleep(0.5)
                        st.rerun()
                    except Exception as e:
                        st.error(friendly_error(e))

        if st.session_state['last_script']:
            st.markdown("<br>", unsafe_allow_html=True)
            platform_urls = {"抖音": "https://www.douyin.com/", "小红书": "https://www.xiaohongshu.com/",
                             "视频号": "https://channels.weixin.qq.com/", "B站": "https://www.bilibili.com/"}
            target_url = platform_urls.get(platform, "#")

            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <a href="{target_url}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; justify-content: center; text-decoration: none; background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(12px); padding: 12px 30px; border-radius: 50px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15), inset 0 1px 1px rgba(255,255,255,0.5); color: white; font-weight: 600; font-size: 1rem; transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);" onmouseover="this.style.transform='scale(1.08, 0.92)'; this.style.background='rgba(255, 255, 255, 0.15)';" onmouseout="this.style.transform='scale(1)'; this.style.background='rgba(255, 255, 255, 0.08)';">
                    🚀 点击直接前往 {platform} 发布作品
                </a>
            </div>
            """, unsafe_allow_html=True)

            with st.container(border=True):
                render_storyboard(st.session_state['last_script'])

            if st.session_state.get('op_advice'):
                raw_advice = st.session_state['op_advice']
                safe_advice = raw_advice.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                st.markdown(f'<div class="op-suggestion">{safe_advice}</div>', unsafe_allow_html=True)

            st.caption(
                f"💡 本次会话已调用 AI {st.session_state['ai_calls']} 次 · 人机协作流程：AI 起草 → 人工修订 → 导出执行")

        st.markdown("---")
        col_j1, col_j2 = st.columns(2)
        with col_j1:
            with st.container(border=True):
                st.markdown("### ✂️ 剪映保姆级教程")
                if st.button("生成剪映实操教程", key="btn_jianying", use_container_width=True):
                    script_content = st.session_state.get('last_script', st.session_state.get("dir_input", ""))
                    if not script_content:
                        st.markdown(
                            '<div style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); padding: 15px; border-radius: 12px; color: #fcd34d; margin-bottom: 15px; font-weight: bold;">⚠️ 请先生成分镜脚本！</div>',
                            unsafe_allow_html=True)
                    else:
                        try:
                            loading_ph = st.empty()
                            loading_ph.markdown(
                                '<div style="color:#8b5cf6; font-weight:bold; padding: 10px 0;">✍️ AI 导师正在定制教程...</div>',
                                unsafe_allow_html=True)

                            full_text = st.write_stream(stream_chat([{"role": "system",
                                                                      "content": f"你是剪辑导师。根据脚本【{script_content}】，写“剪映”App实操教程。细化到点哪个按钮。"},
                                                                     {"role": "user", "content": "教程。"}],
                                                                    temperature=TEMP_EDIT))
                            loading_ph.empty()

                            is_error = ERR_PREFIX.strip() in full_text
                            if not is_error:
                                st.session_state["ai_calls"] += 1
                        except Exception as e:
                            st.error(friendly_error(e))

        with col_j2:
            with st.container(border=True):
                st.markdown("### 📹 视频剪辑成果诊断")
                uploaded_video = st.file_uploader("上传剪辑视频 (mp4/mov/avi)", type=["mp4", "mov", "avi"])
                if uploaded_video is not None:
                    if uploaded_video.size > 50 * 1024 * 1024:
                        st.markdown(
                            '<div style="background-color: rgba(220, 38, 38, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); padding: 15px; border-radius: 12px; color: #fca5a5; margin-bottom: 15px; font-weight: bold;">❌ 视频过大，建议上传 < 50MB 的剪辑片段</div>',
                            unsafe_allow_html=True)
                    else:
                        st.video(uploaded_video)
                        user_desc = st.text_area("剪辑难点？", key="video_diag_input",
                                                 placeholder="例如：不知道怎么加转场。")
                        if st.button("获取 AI 专家修改建议", type="primary", key="btn_review",
                                     use_container_width=True):
                            try:
                                loading_ph = st.empty()
                                loading_ph.markdown(
                                    '<div style="color:#8b5cf6; font-weight:bold; padding: 10px 0;">✍️ AI 专家正在分析痛点...</div>',
                                    unsafe_allow_html=True)

                                full_text = st.write_stream(stream_chat([{"role": "system",
                                                                          "content": f"你是编导。脚本【{st.session_state.get('last_script', '')}】。难点【{user_desc}】。请给出诊断和剪映建议。"},
                                                                         {"role": "user", "content": "建议。"}],
                                                                        temperature=TEMP_DIAG))
                                loading_ph.empty()

                                is_error = ERR_PREFIX.strip() in full_text
                                if not is_error:
                                    st.session_state["ai_calls"] += 1
                            except Exception as e:
                                st.error(friendly_error(e))

    # ==================== 选项卡 2：合规审查 ====================
    with tab2:
        with st.container(border=True):
            st.markdown("### 输入直播带货脚本，双层引擎排查风险")

            c_in1, c_in2 = st.columns([4, 1])
            with c_in2:
                if st.button("💡 填入案例", key="demo_cmp", use_container_width=True):
                    st.session_state["review_input"] = "家人们，今天这款养生茶绝对是全网最低价！喝了能包治百病，连医院都不用去了！"
                    st.rerun()

            with c_in1:
                st.text_area("请输入您的直播带货脚本：", height=100, key="review_input",
                             placeholder="例如：全网最低价...")

            if st.button("开启双层合规审查", type="primary", use_container_width=True, key="btn_tab1"):
                input_text = st.session_state.get("review_input", "")
                if not input_text.strip():
                    st.markdown(
                        '<div style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); padding: 15px; border-radius: 12px; color: #fcd34d; margin-bottom: 15px; font-weight: bold;">⚠️ 请先输入文案哦！</div>',
                        unsafe_allow_html=True)
                else:
                    try:
                        local_rules = ["全网最低", "绝对", "第一", "包治百病", "连医院都不用去", "最便宜", "特效"]
                        hits = [word for word in local_rules if word in input_text]
                        rule_msg = f"\n\n【注意】本地规则库已命中：{hits}，请重点报告。" if hits else ""

                        loading_ph = st.empty()
                        loading_ph.markdown(
                            '<div style="color:#8b5cf6; font-weight:bold; padding: 10px 0;">✍️ 双层引擎审查中，正在生成结构化报告...</div>',
                            unsafe_allow_html=True)

                        full_text = st.write_stream(stream_chat(
                            [{"role": "system",
                              "content": "你是资深法务。请严格按以下格式输出：\n1. 第一行必须输出【风险评分：X分】（0-100分，越高风险越大）。\n2. 第二行输出【判定结论】。\n3. 用 Markdown 表格输出风险清单（列名：风险等级 | 原文片段 | 风险类型 | 法律依据(如广告法第X条) | 安全改写）。\n4. 最后输出【安全版口播稿】：一段完整的修改后文案。"},
                             {"role": "user", "content": f"待审原文：{input_text}{rule_msg}"}], temperature=TEMP_LEGAL
                        ))
                        loading_ph.empty()

                        is_error = ERR_PREFIX.strip() in full_text
                        if is_error:
                            st.stop()

                        st.session_state["ai_calls"] += 1
                        st.session_state["review_result"] = full_text
                        st.session_state["rule_hits"] = hits
                        time.sleep(0.5)
                        st.rerun()
                    except Exception as e:
                        st.error(friendly_error(e))

        if st.session_state.get("review_result"):
            st.markdown("---")
            result_text = st.session_state["review_result"]

            score_match = re.search(r'【风险评分：\s*(\d+)\s*分】', result_text)
            score = int(score_match.group(1)) if score_match else (80 if st.session_state.get("rule_hits") else None)

            safe_version = result_text.split("【安全版口播稿】")[
                -1].strip() if "【安全版口播稿】" in result_text else "AI 未按要求输出安全版。"
            analysis_text = result_text.split("【安全版口播稿】")[0] if "【安全版口播稿】" in result_text else result_text

            if score is not None:
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 1rem; color: #a0aec0;">AI 综合风险判定</div>
                    <div style="font-size: 3rem; font-weight: 800; color: {'#ef4444' if score >= 60 else '#10b981'}; margin: 10px 0;">
                        {score} <span style="font-size: 1.5rem; color: #a0aec0;">/ 100</span>
                    </div>
                    <div style="font-size: 1.1rem; color: {'#ef4444' if score >= 60 else '#10b981'}; font-weight: bold;">
                        {'🚨 高危！切勿直接发布' if score >= 60 else '✅ 风险较低，可酌情发布'}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.5); padding: 15px; border-radius: 12px; color: #fcd34d; margin-bottom: 15px; font-weight: bold;">⚠️ AI 未给出确切评分，请人工复核。</div>',
                    unsafe_allow_html=True)

            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("#### ❌ 原稿 (包含风险)")
                if st.session_state.get("rule_hits"):
                    st.markdown(
                        '<div style="background-color: rgba(220, 38, 38, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); padding: 15px; border-radius: 12px; color: #fca5a5; margin-bottom: 15px; font-weight: bold;">⚠️ 本地规则引擎拦截：发现高危极限词</div>',
                        unsafe_allow_html=True)
                    raw_text = st.session_state.get("review_input", "")
                    display_text = html.escape(raw_text)
                    for word in st.session_state["rule_hits"]:
                        safe_word = html.escape(word)
                        display_text = display_text.replace(safe_word,
                                                            f'<span class="highlight-hit">{safe_word}</span>')
                    st.markdown(
                        f'<div style="background:rgba(0,0,0,0.3); padding:15px; border-radius:12px; border:1px solid rgba(255,255,255,0.1); margin-bottom:15px; line-height:1.8;">{display_text}</div>',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div style="background:rgba(0,0,0,0.3); padding:15px; border-radius:12px; border:1px solid rgba(255,255,255,0.1); margin-bottom:15px; line-height:1.8;">{html.escape(st.session_state.get("review_input", ""))}</div>',
                        unsafe_allow_html=True)

                verdict = re.search(r'【判定结论】\s*(.+)', analysis_text)
                if verdict:
                    st.markdown(f"**判定结论**：{verdict.group(1).strip()}")

                clean_analysis = re.sub(r'【判定结论】[\s\S]*?(?=\n【|$)', '', analysis_text, count=1)
                with st.container(border=True):
                    st.markdown(clean_analysis)

            with col_right:
                st.markdown("#### ✅ AI 安全改写版")
                st.markdown(
                    '<div style="background-color: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.5); padding: 15px; border-radius: 12px; color: #6ee7b7; margin-bottom: 15px; font-weight: bold;">建议使用以下话术，规避封号风险：</div>',
                    unsafe_allow_html=True)
                st.markdown(
                    f'<div style="background-color: #1a1c24; border: 1px solid rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; color: #e2e8f0; font-family: monospace; white-space: pre-wrap; margin-bottom: 15px;">{html.escape(safe_version)}</div>',
                    unsafe_allow_html=True)

                ts = datetime.now().strftime("%Y%m%d_%H%M")
                st.download_button(label="📥 下载完整合规报告 (TXT)", data=st.session_state["review_result"],
                                   file_name=f"合规报告_{ts}.txt", mime="text/plain", type="primary",
                                   use_container_width=True)

            if st.button("🗑️ 清空当前审查记录", use_container_width=True):
                st.session_state["review_result"] = ""
                st.session_state["rule_hits"] = []
                st.rerun()

    # ==================== 底部技术指导 ====================
    st.markdown("""
    <div style="text-align: center; margin-top: 60px; padding-bottom: 30px; font-size: 0.9rem; color: rgba(255,255,255,0.6);">
        <hr style="border-color: rgba(255, 255, 255, 0.1); margin-bottom: 15px; width: 40%; margin-left: 30%;">
        <p>技术指导：和云风 | 联系邮箱：1620339694@qq.com</p>
    </div>
    """, unsafe_allow_html=True)