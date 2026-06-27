"""
凉贸通 - 义乌降温品类欧洲出海OPC智能体
Streamlit 轻量化演示网页主程序

作者：凉贸通团队
版本：v1.0
日期：2026年6月
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime


# 导入智能体模块
from agents.selection_agent import SelectionAgent
from agents.document_agent import DocumentAgent
from agents.marketing_agent import MarketingAgent
from agents.compliance_agent import ComplianceAgent
from agents.display_agent import DisplayAgent

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="凉贸通 - 义乌降温品类欧洲出海OPC智能体",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 样式定制 ====================
def custom_css():
    """自定义CSS样式"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .result-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 初始化智能体 ====================
@st.cache_resource
def init_agents():
    """初始化所有智能体（缓存以提高性能）"""
    return {
        'selection': SelectionAgent(),
        'document': DocumentAgent(),
        'marketing': MarketingAgent(),
        'compliance': ComplianceAgent(),
        'display': DisplayAgent()
    }

# ==================== 首页 ====================
def home_page():
    """首页展示"""
    st.markdown('<p class="main-header">❄️ 凉贸通</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">义乌降温品类欧洲出海OPC智能体 - 让跨境出海更简单</p>', unsafe_allow_html=True)
    
    # 项目介绍
    st.markdown("### 🎯 项目定位")
    st.write("""
    凉贸通聚焦义乌降温品类出海欧洲跨境垂直场景，针对中小跨境卖家出海流程繁琐、专业度不足、
    人力成本高、多环节效率低下等行业痛点，搭建轻量化、全链路自动化的OPC智能体系统。
    """)
    
    # 核心价值指标
    st.markdown("### 📊 核心价值")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">60%+</div>
            <div class="metric-label">成本降低</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">300%+</div>
            <div class="metric-label">效率提升</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">99%</div>
            <div class="metric-label">单证准确率</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">8种</div>
            <div class="metric-label">支持语言</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 五大功能模块入口
    st.markdown("### 🚀 五大核心功能")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 选品分析</h3>
            <p>智能推荐爆款产品，分析市场趋势，测算利润空间</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📄 单证处理</h3>
            <p>自动生成全套出口单证，智能校验数据一致性</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🌍 多语种营销</h3>
            <p>一键生成多语言营销文案，突破语言壁垒</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>✅ 合规校验</h3>
            <p>CE/ROHS/REACH合规校验，自动计算进口税费</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 智能展示</h3>
            <p>自动生成商品详情页，智能优化排版提升转化</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 空白占位
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 技术架构
    st.markdown("### 🏗️ 三层技术架构")
    st.markdown("""
    - **网页交互层**：Streamlit轻量化Web界面，简洁易用
    - **智能体调度层**：主控智能体 + 五大业务智能体，协同工作
    - **业务数据层**：产品库、市场库、单证库、合规库、语料库
    """)

# ==================== 选品分析页面 ====================
def selection_page():
    """选品分析页面"""
    st.markdown("## 📊 选品分析智能体")
    st.write("基于欧洲市场数据和义乌产业带数据，为您推荐最具潜力的降温产品")
    
    # 输入区域
    st.markdown("### 🔍 选品条件")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        target_country = st.selectbox(
            "目标国家",
            ["德国", "法国", "意大利", "西班牙", "英国", "荷兰", "波兰", "瑞典"],
            index=0
        )
    
    with col2:
        category = st.selectbox(
            "产品品类",
            ["全部", "风扇类", "制冰机类", "冷感家纺类", "冰垫类", "便携制冷类"],
            index=0
        )
    
    with col3:
        budget = st.slider(
            "采购预算范围（元）",
            min_value=1000,
            max_value=100000,
            value=(5000, 50000),
            step=1000
        )
    
    risk_preference = st.select_slider(
        "风险偏好",
        options=["保守", "稳健", "积极", "激进"],
        value="稳健"
    )
    
    # 分析按钮
    if st.button("🚀 开始选品分析", type="primary", use_container_width=True):
        with st.spinner("智能体正在分析市场数据..."):
            # 调用选品智能体
            agents = init_agents()
            result = agents['selection'].analyze(
                target_country=target_country,
                category=category,
                budget=budget,
                risk_preference=risk_preference
            )
        
        # 展示结果
        st.success("✅ 选品分析完成！")
        
        # 推荐产品列表
        st.markdown("### 🏆 推荐产品TOP5")
    if result['products']:
        st.write("第一个产品的字段:", list(result['products'][0].keys()))
        
        for i, product in enumerate(result['products'], 1):
            with st.expander(f"**TOP{i}: {product['name']}** - 综合评分: {product['score']}分", expanded=(i==1)):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("采购成本", f"¥{product['cost']}")
                with col2:
                    st.metric("预计售价", f"€{product['price']}")
                with col3:
                    st.metric("利润率", f"{product['profit_rate']}%")
                with col4:
                    st.metric("月销量预测", f"{product['sales_prediction']}件")
                
                st.markdown("**产品卖点：**")
                for selling_point in product['selling_points']:
                    st.write(f"- {selling_point}")
                
                st.markdown("**风险提示：**")
                for risk in product['risks']:
                    st.warning(f"⚠️ {risk}")
        
        # 趋势图表
        st.markdown("### 📈 市场趋势分析")
        trend_data = pd.DataFrame(result['trend_data'])
        fig = px.line(trend_data, x='月份', y='销量', title='目标市场降温产品销量趋势')
        st.plotly_chart(fig, use_container_width=True)
        
        # 选品建议
        st.markdown("### 💡 选品建议")
        st.markdown(f"""
        <div class="result-box">
        <strong>针对{target_country}市场的选品建议：</strong><br><br>
        {result['suggestion']}
        </div>
        """, unsafe_allow_html=True)
        
        # 导出报告
        st.download_button(
            "📥 导出选品分析报告",
            data=json.dumps(result, ensure_ascii=False, indent=2),
            file_name=f"选品分析报告_{target_country}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# ==================== 单证处理页面 ====================
def document_page():
    """单证处理页面"""
    st.markdown("## 📄 单证处理智能体")
    st.write("自动生成全套出口单证，智能校验数据一致性，大幅提升制单效率")
    
    # 输入方式选择
    input_mode = st.radio("数据输入方式", ["表单填写", "Excel批量导入"], horizontal=True)
    
    if input_mode == "表单填写":
        st.markdown("### 📝 订单信息")
        
        # 基本信息
        col1, col2 = st.columns(2)
        
        with col1:
            order_no = st.text_input("订单号", value="ORD20260627001")
            buyer_name = st.text_input("买方公司名称", value="Germany Cooling GmbH")
            buyer_country = st.selectbox("目的国", ["德国", "法国", "意大利", "西班牙", "英国"])
        
        with col2:
            order_date = st.date_input("订单日期", value=datetime.now())
            seller_name = st.text_input("卖方公司名称", value="义乌凉贸通进出口有限公司")
            trade_term = st.selectbox("贸易术语", ["FOB", "CIF", "CFR", "EXW"])
        
        # 产品明细
        st.markdown("### 📦 产品明细")
        
        # 示例产品数据
        default_products = pd.DataFrame([
            {"产品名称": "台式冷风扇", "HS编码": "84145990", "数量": 100, "单价(USD)": 25.50, "毛重(kg)": 2.5, "体积(m³)": 0.02},
            {"产品名称": "USB迷你风扇", "HS编码": "84145990", "数量": 500, "单价(USD)": 5.80, "毛重(kg)": 0.3, "体积(m³)": 0.002},
        ])
        
        edited_df = st.data_editor(default_products, num_rows="dynamic", use_container_width=True)
        
        # 单证类型选择
        st.markdown("### 📋 单证类型")
        doc_types = st.multiselect(
            "选择需要生成的单证",
            ["商业发票", "装箱单", "原产地证", "符合性声明", "报关单"],
            default=["商业发票", "装箱单"]
        )
        
        # 生成按钮
        if st.button("📄 生成单证", type="primary", use_container_width=True):
            with st.spinner("智能体正在生成单证..."):
                # 调用单证智能体
                agents = init_agents()
                result = agents['document'].generate(
                    order_info={
                        'order_no': order_no,
                        'buyer_name': buyer_name,
                        'buyer_country': buyer_country,
                        'seller_name': seller_name,
                        'trade_term': trade_term,
                        'order_date': order_date.strftime('%Y-%m-%d')
                    },
                    products=edited_df.to_dict('records'),
                    doc_types=doc_types
                )
            
            # 展示结果
            st.success("✅ 单证生成完成！")
            
            # 校验结果
            st.markdown("### ✅ 数据校验结果")
            
            if result['validation']['passed']:
                st.markdown(f"""
                <div class="success-box">
                <strong>校验通过！</strong> 所有数据检查无误，可以直接使用。
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-box">
                <strong>存在警告项：</strong><br>
                {''.join([f'- {w}<br>' for w in result['validation']['warnings']])}
                </div>
                """, unsafe_allow_html=True)
            
            # 单证预览
            st.markdown("### 📄 单证预览")
            
            for doc in result['documents']:
                with st.expander(f"📄 {doc['name']}", expanded=True):
                    st.markdown(f"```{doc['content']}```")
                    
                    # 下载按钮
                    st.download_button(
                        f"📥 下载{doc['name']}",
                        data=doc['content'],
                        file_name=doc['filename'],
                        mime="text/plain"
                    )
            
            # 批量下载
            if len(result['documents']) > 1:
                st.info("💡 提示：实际部署版本支持批量下载所有单证为ZIP压缩包")
    
    else:
        st.info("📁 Excel批量导入功能：上传包含产品明细的Excel文件，系统将自动解析并生成单证")
        uploaded_file = st.file_uploader("上传Excel文件", type=['xlsx', 'xls'])
        if uploaded_file:
            st.success("✅ 文件上传成功！点击生成单证按钮开始处理")

# ==================== 多语种营销页面 ====================
def marketing_page():
    """多语种营销页面"""
    st.markdown("## 🌍 多语种营销智能体")
    st.write("一键生成多语言、多平台营销文案，帮助您突破语言壁垒，开拓欧洲市场")
    
    # 产品信息输入
    st.markdown("### 📝 产品信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("产品名称", value="便携式冷风扇")
        product_category = st.selectbox("产品品类", ["风扇类", "制冰机类", "冷感家纺类", "冰垫类"])
        target_platform = st.selectbox("目标平台", ["亚马逊", "速卖通", "eBay", "独立站"])
    
    with col2:
        price = st.number_input("产品售价(€)", value=39.99, step=0.01)
        core_features = st.text_area(
            "核心卖点（每行一个）",
            value="""强劲风力，快速降温
静音设计，不打扰休息
便携轻巧，随处可用
节能省电，环保低碳
USB供电，多种供电方式"""
        )
    
    # 语言选择
    st.markdown("### 🌐 目标语言")
    
    languages = st.multiselect(
        "选择目标语言（可多选）",
        ["英语", "德语", "法语", "意大利语", "西班牙语", "荷兰语", "波兰语", "瑞典语"],
        default=["英语", "德语", "法语"]
    )
    
    # 生成按钮
    if st.button("✍️ 生成营销文案", type="primary", use_container_width=True):
        with st.spinner("智能体正在生成多语言文案..."):
            # 调用营销智能体
            agents = init_agents()
            result = agents['marketing'].generate(
                product_name=product_name,
                product_category=product_category,
                price=price,
                core_features=core_features.split('\n'),
                target_platform=target_platform,
                languages=languages
            )
        
        # 展示结果
        st.success("✅ 文案生成完成！")
        
        # 关键词
        st.markdown("### 🔑 推荐关键词")
        keywords_df = pd.DataFrame(result['keywords'])
        st.dataframe(keywords_df, use_container_width=True)
        
        # 各语言文案
        st.markdown("### 📄 多语言文案展示")
        
        for lang_copy in result['copies']:
            with st.expander(f"🌐 {lang_copy['language']}版本文案", expanded=(lang_copy['language'] == '英语')):
                st.markdown(f"**产品标题：**")
                st.info(lang_copy['title'])
                
                st.markdown(f"**五点描述：**")
                for i, point in enumerate(lang_copy['bullets'], 1):
                    st.write(f"{i}. {point}")
                
                st.markdown(f"**产品描述：**")
                st.write(lang_copy['description'])
                
                # 复制按钮（模拟）
                st.info(f"💡 提示：实际使用时可一键复制{lang_copy['language']}文案到平台后台")

# ==================== 合规校验页面 ====================
def compliance_page():
    """合规校验页面"""
    st.markdown("## ✅ 跨境合规校验智能体")
    st.write("自动检查欧盟合规标准，计算进口税费，帮助您规避合规风险")
    
    # 产品信息
    st.markdown("### 📝 产品信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("产品名称", value="USB充电小风扇")
        product_category = st.selectbox("产品类别", ["电子产品", "家用电器", "纺织用品", "塑料制品"])
        material = st.text_input("主要材质", value="ABS塑料 + 电子元件")
        has_battery = st.checkbox("含电池", value=True)
    
    with col2:
        target_country = st.selectbox("目标国家", ["德国", "法国", "意大利", "西班牙", "荷兰"])
        declared_value = st.number_input("申报价值(USD)", value=1500.00, step=100.0)
        hs_code = st.text_input("HS编码（选填，系统可自动匹配）", value="")
        
        st.markdown("**认证情况：**")
        ce_cert = st.checkbox("CE认证", value=True)
        rohs_cert = st.checkbox("ROHS认证", value=False)
        reach_cert = st.checkbox("REACH认证", value=False)
    
    # 校验按钮
    if st.button("🔍 开始合规校验", type="primary", use_container_width=True):
        with st.spinner("智能体正在进行合规校验..."):
            # 调用合规智能体
            agents = init_agents()
            result = agents['compliance'].check(
                product_name=product_name,
                product_category=product_category,
                material=material,
                has_battery=has_battery,
                target_country=target_country,
                declared_value=declared_value,
                hs_code=hs_code,
                certifications={
                    'CE': ce_cert,
                    'ROHS': rohs_cert,
                    'REACH': reach_cert
                }
            )
        
        # 展示结果
        st.success("✅ 合规校验完成！")
        
        # 合规评分
        st.markdown("### 📊 合规评分")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("综合合规评分", f"{result['score']}/100分")
        with col2:
            st.metric("高风险项", f"{result['high_risk_count']}项")
        with col3:
            st.metric("建议HS编码", result['hs_code_suggestion'])
        
        # 风险列表
        st.markdown("### ⚠️ 风险项列表")
        
        for risk in result['risks']:
            if risk['level'] == '高':
                st.error(f"🔴 【高风险】{risk['name']}：{risk['description']}")
                st.info(f"💡 整改建议：{risk['suggestion']}")
            elif risk['level'] == '中':
                st.warning(f"🟡 【中风险】{risk['name']}：{risk['description']}")
                st.info(f"💡 整改建议：{risk['suggestion']}")
            else:
                st.info(f"🟢 【低风险】{risk['name']}：{risk['description']}")
        
        # 税费计算
        st.markdown("### 💰 税费计算明细")
        
        tax_df = pd.DataFrame([
            {"税费项目": "进口关税", "税率": f"{result['tax']['duty_rate']}%", "金额(USD)": result['tax']['duty_amount']},
            {"税费项目": "VAT增值税", "税率": f"{result['tax']['vat_rate']}%", "金额(USD)": result['tax']['vat_amount']},
            {"税费项目": "其他费用", "税率": "-", "金额(USD)": result['tax']['other_fees']},
            {"税费项目": "**合计**", "税率": "-", "金额(USD)": f"**{result['tax']['total']}**"},
        ])
        
        st.table(tax_df)
        
        # 整改建议
        st.markdown("### 📋 整改建议汇总")
        st.markdown(f"""
        <div class="result-box">
        {result['summary_suggestion']}
        </div>
        """, unsafe_allow_html=True)

# ==================== 智能展示页面 ====================
def display_page():
    """商品智能展示页面"""
    st.markdown("## 🎨 商品智能展示智能体")
    st.write("自动生成专业的商品详情页方案，智能优化排版，帮助您提升转化率")
    
    # 输入区域
    st.markdown("### 📝 产品信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("产品名称", value="家用小型制冰机")
        product_type = st.selectbox("产品类型", ["功能型", "家居型", "科技型", "时尚型"])
        target_platform = st.selectbox("目标平台", ["亚马逊", "速卖通", "独立站"])
        target_language = st.selectbox("目标语言", ["英语", "德语", "法语", "意大利语"])
    
    with col2:
        st.markdown("产品图片（模拟上传）")
        st.info("📷 演示版本：模拟已上传5张产品图片")
        st.markdown("""
        - 主图：产品正面图
        - 细节图：产品细节特写
        - 场景图：使用场景展示
        - 参数图：规格参数说明
        - 包装图：包装展示
        """)
    
    # 核心卖点
    core_selling_points = st.text_area(
        "核心卖点",
        value="""快速制冰，6分钟出冰
大容量水箱，续航持久
静音运行，不打扰生活
自清洁功能，使用省心
小巧便携，不占空间"""
    )
    
    # 生成按钮
    if st.button("🎨 生成详情页方案", type="primary", use_container_width=True):
        with st.spinner("智能体正在生成详情页方案..."):
            # 调用展示智能体
            agents = init_agents()
            result = agents['display'].generate(
                product_name=product_name,
                product_type=product_type,
                target_platform=target_platform,
                target_language=target_language,
                core_selling_points=core_selling_points.split('\n')
            )
        
        # 展示结果
        st.success("✅ 详情页方案生成完成！")
        
        # 三套方案
        st.markdown("### 📄 三套详情页方案")
        
        for i, scheme in enumerate(result['schemes'], 1):
            with st.expander(f"方案{i}：{scheme['name']} - 预计转化率提升：{scheme['conversion_boost']}", expanded=(i==1)):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"**方案特点：**")
                    st.write(scheme['description'])
                    st.markdown(f"**适合场景：**")
                    st.write(scheme['suitable_for'])
                
                with col2:
                    st.markdown("**页面结构：**")
                    for j, section in enumerate(scheme['structure'], 1):
                        st.write(f"{j}. {section}")
                
                st.markdown("**文案示例：**")
                st.info(scheme['sample_copy'])
        
        # 方案对比
        st.markdown("### 📊 方案对比")
        
        comparison_df = pd.DataFrame([
            {"方案": "方案A", "风格": result['schemes'][0]['name'], "预计转化率提升": result['schemes'][0]['conversion_boost'], "制作难度": "简单"},
            {"方案": "方案B", "风格": result['schemes'][1]['name'], "预计转化率提升": result['schemes'][1]['conversion_boost'], "制作难度": "中等"},
            {"方案": "方案C", "风格": result['schemes'][2]['name'], "预计转化率提升": result['schemes'][2]['conversion_boost'], "制作难度": "较难"},
        ])
        
        st.table(comparison_df)
        
        # 推荐方案
        st.markdown("### 💡 智能推荐")
        st.markdown(f"""
        <div class="success-box">
        <strong>推荐方案：{result['recommendation']['scheme']}</strong><br><br>
        {result['recommendation']['reason']}
        </div>
        """, unsafe_allow_html=True)

# ==================== 主函数 ====================
def main():
    """主函数"""
    custom_css()
    
    # 侧边栏导航
    with st.sidebar:
        st.markdown("## ❄️ 凉贸通")
        st.markdown("义乌降温品类欧洲出海OPC智能体")
        st.markdown("---")
        
        page = st.radio(
            "功能导航",
            ["🏠 首页", "📊 选品分析", "📄 单证处理", "🌍 多语种营销", "✅ 合规校验", "🎨 智能展示"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 系统状态")
        st.info("✅ 所有智能体运行正常")
        st.info(f"🕐 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 页面路由
    if page == "🏠 首页":
        home_page()
    elif page == "📊 选品分析":
        selection_page()
    elif page == "📄 单证处理":
        document_page()
    elif page == "🌍 多语种营销":
        marketing_page()
    elif page == "✅ 合规校验":
        compliance_page()
    elif page == "🎨 智能展示":
        display_page()
    
    # 页脚
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #999; font-size: 0.8rem;'>"
        "凉贸通 © 2026 | 义乌降温品类欧洲出海OPC智能体 | 南京晓庄学院"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
