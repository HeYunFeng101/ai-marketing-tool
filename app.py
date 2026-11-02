import streamlit as st
from openai import OpenAI
import time
import re
import base64

# 1. 网页基础设置
st.set_page_config(page_title="AI 营销与传播助手", page_icon="✨", layout="wide")

# 2. 读取本地图片并转为 Base64
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# 读取背景图和 LOGO
bin_str = get_base64_of_bin_file('bg.jpg')
logo_str = get_base64_of_bin_file('LOGO.png')

# ==================== Q弹玻璃胶囊 UI 注入 ====================
st.markdown(f"""
<style>
/* 隐藏默认菜单和页脚 */
#MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}

/* 核心改动：降低暗色遮罩，让原图更加透亮 */
[data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(rgba(10, 12, 20, 0.2), rgba(10, 12, 20, 0.4)), url("data:image/jpeg;base64,{bin_str}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}

/* 侧边栏毛玻璃效果 */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) saturate(150%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
}}

/* 所有文本强制亮色 */
.stMarkdown, p, h1, h2, h3, h4, label, span {{
    color: #f8fafc !important;
}}

/* 标题气泡：大圆角 */
.bubble-title {{
    display: inline-flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    padding: 12px 35px;
    border-radius: 50px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15), inset 0 1px 2px rgba(255,255,255,0.5);
    color: white;
    font-weight: 800;
    margin-bottom: 20px;
    transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}}
.bubble-title:hover {{
    transform: scale(1.05, 0.95); 
    background: rgba(255, 255, 255, 0.12);
}}

.bubble-subtitle {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(10px);
    padding: 8px 25px;
    border-radius: 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #e2e8f0;
    font-size: 1.1rem;
    margin-bottom: 40px;
}}

/* 区块标题胶囊 */
.stMarkdown h3 {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(10px);
    padding: 10px 20px !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1), inset 0 1px 1px rgba(255,255,255,0.4) !important;
    margin-bottom: 15px !important;
}}

/* 输入框 Label 胶囊 */
[data-testid="stWidgetLabel"] p {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    font-size: 0.95rem;
    color: #f8fafc !important;
    margin-bottom: 5px;
}}

/* 输入框本体：玻璃胶囊化 */
.stTextInput input, .stTextArea textarea {{
    border-radius: 16px !important; 
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    background-color: rgba(255, 255, 255, 0.05) !important; 
    color: white !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.1) !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
    transform: scale(1.01) !important; 
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.1), inset 0 2px 5px rgba(0,0,0,0.1) !important;
}}

/* ===== 按钮：极致挤压感的玻璃胶囊 ===== */
.stButton > button {{
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 50px !important; 
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15), inset 0 1px 1px rgba(255,255,255,0.5) !important;
}}
.stButton > button:hover {{
    transform: scale(1.08, 0.92) !important; 
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2), inset 0 2px 5px rgba(255,255,255,0.8) !important;
}}
.stButton > button:active {{
    transform: scale(0.95, 0.95) !important;
}}

/* Tabs 胶囊导航挤压感 */
.stTabs [data-baseweb="tab-list"] {{ gap: 15px; background-color: transparent; border-bottom: none; }}
.stTabs [data-baseweb="tab"] {{
    border-radius: 50px !important; 
    background-color: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    padding: 10px 25px !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important; 
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: #cbd5e1 !important; 
    font-weight: 500 !important;
    box-shadow: inset 0 1px 1px rgba(255,255,255,0.3) !important;
}}
.stTabs [data-baseweb="tab"]:hover {{ 
    transform: scale(1.05, 0.95) !important;
    background-color: rgba(255, 255, 255, 0.1) !important; 
}}
.stTabs [aria-selected="true"] {{
    background: rgba(255, 255, 255, 0.15) !important; 
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), inset 0 1px 2px rgba(255,255,255,0.6) !important;
}}

/* 容器卡片全面玻璃化 + 挤压动效 */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) saturate(150%) !important;
    border-radius: 24px !important; 
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 2px rgba(255,255,255,0.3) !important;
    transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    transform-origin: center !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    transform: scale(1.02, 0.98) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2), inset 0 1px 2px rgba(255,255,255,0.5) !important;
    background: rgba(255, 255, 255, 0.08) !important;
}}
</style>
""", unsafe_allow_html=True)

# 3. 获取 API Key
API_KEY = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

# 4. 初始化登录状态
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "user_phone" not in st.session_state: st.session_state["user_phone"] = ""

# ==================== 登录界面 ====================
if not st.session_state["logged_in"]:
    st.markdown(f"""
    <div style="text-align: center; margin-top: 50px;">
        <div class="bubble-title" style="font-size: 2.8rem; gap: 20px;">
            <!-- 调大了 LOGO 尺寸，去掉了圆角 -->
            <img src="data:image/png;base64,{logo_str}" width="110"> 
            <span>AI 营销与传播全链路助手</span>
        </div>
        <br>
        <div class="bubble-subtitle">您的专属 AI 营销增长引擎</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### 📱 手机号快捷登录 / 注册")
            phone = st.text_input("请输入您的手机号", placeholder="请输入 11 位手机号", max_chars=11)

            col_code1, col_code2 = st.columns([2, 1])
            with col_code1:
                verify_code = st.text_input("请输入验证码", placeholder="输入 4 位验证码", max_chars=4)
            with col_code2:
                st.write("")
                st.write("")
                if st.button("获取验证码", use_container_width=True):
                    if re.match(r"^1[3-9]\d{9}$", phone):
                        st.toast("验证码已发送！(测试环境: 1234)", icon="✅")
                    else:
                        st.toast("请输入正确的手机号！", icon="❌")

            st.write("")
            if st.button("登录 / 进入系统", type="primary", use_container_width=True):
                if not phone or not verify_code:
                    st.warning("手机号和验证码不能为空哦！")
                elif not re.match(r"^1[3-9]\d{9}$", phone):
                    st.error("手机号格式不正确，请检查！")
                elif verify_code != "1234":
                    st.error("验证码错误！")
                else:
                    with st.spinner("正在安全登录..."):
                        time.sleep(1)
                        st.session_state["logged_in"] = True
                        st.session_state["user_phone"] = phone[:3] + "****" + phone[-4:]
                        st.rerun()

# ==================== 登录成功后的主系统 ====================
else:
    # 侧边栏——精致的用户卡片
    with st.sidebar:
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 24px; text-align: center; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.15); backdrop-filter: blur(10px); transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); box-shadow: 0 8px 32px rgba(0,0,0,0.1), inset 0 1px 1px rgba(255,255,255,0.4);" onmouseover="this.style.transform='scale(1.03, 0.97)'" onmouseout="this.style.transform='scale(1)'">
            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, rgba(255,255,255,0.4), rgba(255,255,255,0.1)); margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 30px; color: white; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.5);">
                👤
            </div>
            <h4 style="color: white; margin-top: 15px; margin-bottom: 5px;">尊贵用户</h4>
            <p style="color: #e2e8f0; font-size: 14px;">{st.session_state['user_phone']}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.popover("⚙️ 账号设置", use_container_width=True):
            st.write("点击下方按钮退出登录")
            if st.button("退出登录", type="primary", use_container_width=True):
                st.session_state["logged_in"] = False
                st.rerun()

        st.info("💡 提示：我们提供从脚本策划、合规审查到后期剪辑的完整 AI 辅助工作流。")

    # 主界面
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <div class="bubble-title" style="font-size: 2.2rem; gap: 15px;">
            <!-- 调大了 LOGO 尺寸 -->
            <img src="data:image/png;base64,{logo_str}" width="80"> 
            <span>AI 营销与传播全链路助手</span>
        </div>
        <br>
        <div class="bubble-subtitle" style="font-size: 1rem;">基于 DeepSeek 大模型，一站式解决直播合规、口碑评估、短视频分镜与剪辑指导。</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🛡️ 直播违规词审查", "😊 店铺口碑评估机", "🎬 短视频分镜与剪辑"])

    # ==================== 选项卡 1：违规审查 ====================
    with tab1:
        with st.container(border=True):
            st.markdown("### 输入直播带货脚本，AI 自动排查风险")
            user_input_1 = st.text_area("请输入您的直播带货脚本：", height=120,
                                        placeholder="例如：家人们，全网最低价的养生茶，喝了包治百病！")

            col_btn1, col_btn2 = st.columns([3, 1])
            with col_btn2:
                if st.button("开启合规审查", type="primary", use_container_width=True, key="btn_tab1"):
                    if not user_input_1.strip():
                        st.warning("请先输入文案哦！")
                    else:
                        with st.spinner("AI 法务审查中..."):
                            try:
                                response = client.chat.completions.create(
                                    model="deepseek-flash",
                                    messages=[{"role": "system",
                                               "content": "你是一个资深的电商直播合规审查员。找出极限词、医疗夸大、侵权风险，并给出优化后的安全文案。"},
                                              {"role": "user", "content": user_input_1}]
                                )
                                st.markdown("---")
                                st.markdown(response.choices[0].message.content)
                            except Exception as e:
                                st.error(f"发生错误：{e}")
        st.info("示例输入：家人们，今天这款养生茶绝对是全网最低价！喝了包治百病，连医院都不用去了！")

    # ==================== 选项卡 2：口碑评估 ====================
    with tab2:
        with st.container(border=True):
            st.markdown("### 输入店铺信息，AI 生成情绪反馈")
            user_input_2 = st.text_input("例如：济南某烧烤店，有人说肉串很香，但有人抱怨老板态度极差。", key="input_tab2")

            col_btn1, col_btn2 = st.columns([3, 1])
            with col_btn2:
                if st.button("评估店铺口碑", type="primary", use_container_width=True, key="btn_tab2"):
                    if not user_input_2.strip():
                        st.warning("请输入店铺信息哦！")
                    else:
                        with st.spinner("AI 正在全网模拟分析..."):
                            try:
                                response = client.chat.completions.create(
                                    model="deepseek-flash",
                                    messages=[{"role": "system",
                                               "content": "你是一个专业的店铺口碑评估专家。请判断口碑情况。如果口碑好，在回答最后加上 [SMILE]；如果存在严重差评风险，加上 [CRY]。"},
                                              {"role": "user", "content": user_input_2}]
                                )
                                result = response.choices[0].message.content

                                if "[SMILE]" in result:
                                    st.balloons()
                                    st.markdown("<h1 style='text-align: center; font-size: 150px;'>😊</h1>",
                                                unsafe_allow_html=True)
                                    st.success("口碑极佳！")
                                elif "[CRY]" in result:
                                    st.markdown("<h1 style='text-align: center; font-size: 150px;'>😭</h1>",
                                                unsafe_allow_html=True)
                                    st.error("口碑堪忧！")

                                st.markdown("---")
                                st.write(result.replace("[SMILE]", "").replace("[CRY]", ""))
                            except Exception as e:
                                st.error(f"发生错误：{e}")

    # ==================== 选项卡 3：短视频分镜与剪辑 ====================
    with tab3:
        with st.expander("⚙️ 展开/收起 创作参数设置", expanded=True):
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1: platform = st.selectbox("目标平台", ["抖音", "小红书", "视频号", "B站"])
            with col_p2: audience = st.selectbox("目标受众",
                                                 ["年轻女性", "宝妈群体", "大学生", "职场新人", "中老年群体"])
            with col_p3: style = st.radio("视频风格", ["真诚分享", "搞笑剧情", "干货科普", "情感共鸣"], horizontal=True)

        with st.container(border=True):
            st.markdown("### 输入主题，一键生成分镜脚本")
            user_input_3 = st.text_area("请输入你的产品、门店或想表达的主题：", height=100,
                                        placeholder="例如：烟台红富士苹果，脆甜多汁，产地直发。", key="input_tab3")

            col_btn3, col_btn4 = st.columns([3, 1])
            with col_btn4:
                if st.button("一键生成爆款分镜", type="primary", use_container_width=True, key="btn_tab3"):
                    if not user_input_3.strip():
                        st.warning("请先输入你的主题哦！")
                    else:
                        with st.spinner("AI 导演正在构思分镜和爆款文案..."):
                            system_prompt = f"你是一个拥有千万粉丝的短视频爆款操盘手。请生成分镜脚本。目标平台【{platform}】，受众【{audience}】，风格【{style}】。严格使用 Markdown 表格输出五列：| 镜号 | 时间(秒) | 画面景别与动作 | 口播文案 | 音效/BGM建议 |。表格后给出运营建议。"
                            try:
                                response = client.chat.completions.create(
                                    model="deepseek-flash",
                                    messages=[{"role": "system", "content": system_prompt},
                                              {"role": "user", "content": f"我的主题是：{user_input_3}"}],
                                    temperature=0.7
                                )
                                result_text = response.choices[0].message.content
                                st.success("🎬 导演，您的分镜脚本已生成！")
                                st.markdown(result_text)
                                st.session_state['last_script'] = result_text
                                st.code(result_text, language="markdown")
                            except Exception as e:
                                st.error(f"发生错误：{e}")

        st.markdown("---")
        with st.container(border=True):
            st.markdown("### ✂️ 拍完不会剪？一键获取剪映保姆级教程")
            if st.button("生成剪映实操教程", key="btn_jianying"):
                script_content = st.session_state.get('last_script', user_input_3)
                if not script_content:
                    st.warning("请先生成分镜脚本！")
                else:
                    with st.spinner("AI 导师正在为你定制剪映操作流程..."):
                        edit_prompt = f"你是一个耐心的剪辑导师。请根据脚本【{script_content}】，写一份详细的“剪映”App实操教程。要求细化到点哪个按钮，如：点击底部【文本】->【识别字幕】。用【图1】占位。"
                        try:
                            edit_response = client.chat.completions.create(model="deepseek-flash", messages=[
                                {"role": "system", "content": edit_prompt}, {"role": "user", "content": "请给我教程。"}],
                                                                           temperature=0.5)
                            st.success("✂️ 专属剪映教程已生成！")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.image("https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400",
                                         caption="图1：剪映界面示例")
                            with col2:
                                st.image("https://images.unsplash.com/photo-1626544827763-d516dce335e2?w=400",
                                         caption="图2：添加字幕示例")
                            st.markdown(edit_response.choices[0].message.content)
                        except Exception as e:
                            st.error(f"教程生成失败：{e}")

        st.markdown("---")
        with st.container(border=True):
            st.markdown("### 📹 视频剪辑成果检测与 AI 诊断")
            uploaded_video = st.file_uploader("请上传你的剪辑视频 (支持 mp4/mov/avi)", type=["mp4", "mov", "avi"])
            if uploaded_video is not None:
                st.video(uploaded_video)
                user_desc = st.text_area("剪辑中遇到了什么问题？", placeholder="例如：不知道怎么加转场，字幕出太慢。")
                if st.button("获取 AI 专家修改建议", type="primary", key="btn_review"):
                    with st.spinner("AI 专家正在分析你的剪辑痛点..."):
                        review_prompt = f"你是短视频编导。脚本是【{st.session_state.get('last_script', '')}】。用户的难点是【{user_desc}】。请给出诊断和剪映实操建议。"
                        try:
                            review_response = client.chat.completions.create(model="deepseek-flash", messages=[
                                {"role": "system", "content": review_prompt}, {"role": "user", "content": "请给建议。"}],
                                                                             temperature=0.6)
                            st.success("🩺 诊断报告已生成！")
                            st.markdown(review_response.choices[0].message.content)
                        except Exception as e:
                            st.error(f"诊断失败：{e}")