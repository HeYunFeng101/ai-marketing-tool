import streamlit as st
from openai import OpenAI
import time
import re

# 1. 网页基础设置
st.set_page_config(page_title="AI 营销与传播助手", page_icon="🚀", layout="wide")

# 2. 获取 API Key
API_KEY = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

# 3. 初始化登录状态
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_phone" not in st.session_state:
    st.session_state["user_phone"] = ""

# ==================== 登录界面 ====================
if not st.session_state["logged_in"]:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🚀 AI 营销与传播全链路助手</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>您的专属 AI 营销增长引擎</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
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
                    st.toast("验证码已发送！(测试环境验证码为: 1234)", icon="✅")
                else:
                    st.toast("请输入正确的手机号！", icon="❌")
        
        st.write("") 
        if st.button("登录 / 进入系统", type="primary", use_container_width=True):
            if not phone or not verify_code:
                st.warning("手机号和验证码不能为空哦！")
            elif not re.match(r"^1[3-9]\d{9}$", phone):
                st.error("手机号格式不正确，请检查！")
            elif verify_code != "1234":
                st.error("验证码错误，请重新输入！")
            else:
                with st.spinner("正在安全登录..."):
                    time.sleep(1) 
                    st.session_state["logged_in"] = True
                    masked_phone = phone[:3] + "****" + phone[-4:]
                    st.session_state["user_phone"] = masked_phone
                    st.rerun()

# ==================== 登录成功后的主系统 ====================
else:
    # 侧边栏
    with st.sidebar:
        st.success(f"👤 当前用户：{st.session_state['user_phone']}")
        if st.button("退出登录", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()
        st.markdown("---")
        
        st.header("⚙️ 创作参数设置")
        st.markdown("*(仅在生成短视频相关内容时生效)*")
        platform = st.selectbox("目标平台", ["抖音", "小红书", "视频号", "B站"])
        audience = st.selectbox("目标受众", ["年轻女性", "宝妈群体", "大学生", "职场新人", "中老年群体"])
        style = st.radio("视频风格", ["真诚分享", "搞笑剧情", "干货科普", "情感共鸣"])
        st.markdown("---")
        st.info("💡 提示：我们提供从脚本策划、合规审查到后期剪辑的完整 AI 辅助工作流。")

    # 主界面
    st.title("🚀 AI 营销与传播全链路助手")
    st.markdown("基于 DeepSeek 大模型，一站式解决直播合规、口碑评估、短视频分镜、剪辑指导与视频诊断。")

    tab1, tab2, tab3 = st.tabs(["🛡️ 直播违规词审查", "😊 店铺口碑评估机", "🎬 短视频分镜与剪辑"])

    # ==================== 选项卡 1：违规审查 ====================
    with tab1:
        st.markdown("### 输入直播带货脚本，AI 自动排查风险")
        user_input_1 = st.text_area(
            "请输入您的直播带货脚本：", 
            height=120, 
            placeholder="例如：家人们，全网最低价的养生茶，喝了包治百病！"
        )
        if st.button("🚀 开启合规审查", type="primary", key="btn_tab1"):
            if not user_input_1.strip():
                st.warning("请先输入文案哦！")
            else:
                with st.spinner("AI 法务审查中..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-flash",
                            messages=[
                                {"role": "system", "content": "你是一个资深的电商直播合规审查员。找出极限词、医疗夸大、侵权风险，并给出优化后的安全文案。"},
                                {"role": "user", "content": user_input_1}
                            ]
                        )
                        st.markdown(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"发生错误：{e}")

    # ==================== 选项卡 2：口碑评估 ====================
    with tab2:
        st.markdown("### 输入店铺信息，AI 生成情绪反馈")
        user_input_2 = st.text_input(
            "例如：济南某烧烤店，有人说肉串很香，但有人抱怨老板态度极差。",
            key="input_tab2"
        )
        if st.button("🔍 评估店铺口碑", type="primary", key="btn_tab2"):
            if not user_input_2.strip():
                st.warning("请输入店铺信息哦！")
            else:
                with st.spinner("AI 正在全网模拟分析..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-flash",
                            messages=[
                                {"role": "system", "content": "你是一个专业的店铺口碑评估专家。请判断口碑情况。如果口碑好，在回答最后加上 [SMILE]；如果存在严重差评风险，加上 [CRY]。"},
                                {"role": "user", "content": user_input_2}
                            ]
                        )
                        result = response.choices[0].message.content
                        
                        if "[SMILE]" in result:
                            st.balloons()
                            st.markdown("<h1 style='text-align: center; font-size: 150px;'>😊</h1>", unsafe_allow_html=True)
                            st.success("口碑极佳！")
                        elif "[CRY]" in result:
                            st.markdown("<h1 style='text-align: center; font-size: 150px;'>😭</h1>", unsafe_allow_html=True)
                            st.error("口碑堪忧！")
                        
                        st.markdown("---")
                        st.write(result.replace("[SMILE]", "").replace("[CRY]", ""))
                    except Exception as e:
                        st.error(f"发生错误：{e}")

    # ==================== 选项卡 3：短视频分镜与剪辑 ====================
    with tab3:
        st.markdown("### 输入主题，一键生成分镜脚本")
        st.info(f"当前配置：平台【{platform}】 | 受众【{audience}】 | 风格【{style}】 (可在左侧边栏修改)")
        
        user_input_3 = st.text_area(
            "请输入你的产品、门店或想表达的主题：", 
            height=100, 
            placeholder="例如：烟台红富士苹果，脆甜多汁，产地直发。",
            key="input_tab3"
        )
        
        if st.button("🎬 一键生成爆款分镜", type="primary", key="btn_tab3"):
            if not user_input_3.strip():
                st.warning("请先输入你的主题哦！")
            else:
                with st.spinner("AI 导演正在构思分镜和爆款文案..."):
                    system_prompt = f"""
                    你是一个拥有千万粉丝的短视频爆款操盘手和资深导演。
                    请根据用户提供的主题，生成一份小白也能直接照拍的“短视频分镜脚本”。
                    要求：
                    1. 目标平台【{platform}】，目标受众【{audience}】，视频风格【{style}】。
                    2. 必须包含“黄金前3秒”的留人钩子。
                    3. 严格使用 Markdown 表格输出五列：| 镜号 | 时间(秒) | 画面景别与动作 | 口播文案 | 音效/BGM建议 |。
                    4. 表格后给出【爆款运营建议】。
                    """
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-flash",
                            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"我的主题是：{user_input_3}"}],
                            temperature=0.7 
                        )
                        result_text = response.choices[0].message.content
                        
                        st.success("🎬 导演，您的分镜脚本已生成！")
                        st.markdown("---")
                        st.markdown(result_text)
                        
                        st.session_state['last_script'] = result_text
                        
                        st.markdown("### 📥 导出脚本")
                        st.code(result_text, language="markdown")
                        st.caption("点击右上角的小图标即可一键复制，发给摄影师直接照着拍！")
                        
                    except Exception as e:
                        st.error(f"发生错误：{e}")

        # ------ 剪映图文教程 ------
        st.markdown("---")
        st.markdown("### ✂️ 拍完不会剪？一键获取剪映保姆级教程")
        
        if st.button("🧑‍💻 生成剪映实操教程", key="btn_jianying"):
            script_content = st.session_state.get('last_script', user_input_3)
            
            if not script_content:
                st.warning("请先在上方输入主题并生成分镜脚本！")
            else:
                with st.spinner("AI 导师正在为你定制剪映操作流程..."):
                    edit_prompt = f"""
                    你是一个耐心的短视频剪辑导师。请根据以下脚本：
                    【{script_content}】
                    为完全不懂剪辑的新手写一份“剪映”实操教程。
                    要求：
                    1. 分为四阶段：素材准备、粗剪、精剪、导出。
                    2. 必须细化到点哪个按钮（如：点击底部【文本】->【识别字幕】）。
                    3. 当你提到关键界面时，请用【图1】或【图2】来占位。
                    """
                    try:
                        edit_response = client.chat.completions.create(
                            model="deepseek-flash",
                            messages=[{"role": "system", "content": edit_prompt}, {"role": "user", "content": "请给我详细的剪映教程。"}],
                            temperature=0.5
                        )
                        st.success("✂️ 专属剪映教程已生成！")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image("https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400", caption="图1：剪映界面示例")
                        with col2:
                            st.image("https://images.unsplash.com/photo-1626544827763-d516dce335e2?w=400", caption="图2：添加字幕与音效示例")
                            
                        st.markdown(edit_response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"教程生成失败：{e}")

        # ------ 视频上传诊断 ------
        st.markdown("---")
        st.markdown("### 📹 视频剪辑成果检测与 AI 诊断")
        st.markdown("上传你按教程剪好的视频，AI 老师为你提供修改建议！")
        
        uploaded_video = st.file_uploader("请上传你的剪辑视频 (支持 mp4/mov/avi)", type=["mp4", "mov", "avi"])
        
        if uploaded_video is not None:
            st.video(uploaded_video)
            
            user_desc = st.text_area(
                "剪辑中遇到了什么问题？（描述得越详细，AI 建议越准）",
                placeholder="例如：我觉得节奏太拖沓了，不知道怎么加转场，字幕出现的时间感觉不对。"
            )
            
            if st.button("🩺 获取 AI 专家修改建议", type="primary", key="btn_review"):
                with st.spinner("AI 专家正在分析你的剪辑痛点..."):
                    review_prompt = f"""
                    你是一个资深短视频编导。用户刚刚尝试剪辑了一个视频。
                    原始分镜脚本是：【{st.session_state.get('last_script', '用户未生成脚本')}】
                    用户的剪辑难点描述是：【{user_desc}】
                    
                    请你根据用户的描述，给出一份专业的修改建议：
                    1. 诊断痛点：指出用户描述的问题通常是因为什么导致的（如：没加关键帧、BGM没踩点）。
                    2. 剪映实操建议：告诉用户在剪映里点哪几个按钮可以解决这个问题。
                    3. 鼓励与优化：给出3条让视频看起来更高级的通用建议。
                    """
                    try:
                        review_response = client.chat.completions.create(
                            model="deepseek-flash",
                            messages=[{"role": "system", "content": review_prompt}, {"role": "user", "content": "请给我修改建议。"}],
                            temperature=0.6
                        )
                        st.success("🩺 诊断报告已生成！")
                        st.markdown(review_response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"诊断失败：{e}")
