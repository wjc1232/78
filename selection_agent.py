"""
选品分析智能体
基于欧洲市场数据和义乌产业带数据，提供智能选品推荐

作者：凉贸通团队
版本：v1.0
日期：2026年6月
"""

from .base_agent import BaseAgent
from typing import Dict, List, Tuple
import random


class SelectionAgent(BaseAgent):
    """
    选品分析智能体
    负责市场数据分析、选品推荐、利润测算
    """
    
    def __init__(self):
        super().__init__("选品分析智能体")
        
        # 模拟产品数据库
        self._init_product_database()
    
    def _init_product_database(self):
        """初始化模拟产品数据库"""
        self.product_db = {
            "风扇类": [
                {
                    "name": "台式冷风扇",
                    "cost": 180,
                    "price_eu": 49.99,
                    "sales_prediction": 500,
                    "score": 92,
                    "selling_points": ["强劲风力，快速降温", "静音设计", "三档风速调节", "节能环保"],
                    "risks": ["竞争较激烈", "季节性明显"],
                    "category": "风扇类"
                },
                {
                    "name": "USB迷你风扇",
                    "cost": 25,
                    "price_eu": 12.99,
                    "sales_prediction": 2000,
                    "score": 88,
                    "selling_points": ["小巧便携", "USB供电", "多色可选", "价格亲民"],
                    "risks": ["利润空间小", "同质化严重"],
                    "category": "风扇类"
                },
                {
                    "name": "落地扇",
                    "cost": 280,
                    "price_eu": 79.99,
                    "sales_prediction": 300,
                    "score": 85,
                    "selling_points": ["大风量", "遥控操作", "定时功能", "高度可调"],
                    "risks": ["物流成本高", "体积大仓储成本高"],
                    "category": "风扇类"
                },
                {
                    "name": "无叶风扇",
                    "cost": 350,
                    "price_eu": 99.99,
                    "sales_prediction": 200,
                    "score": 82,
                    "selling_points": ["安全无叶", "设计时尚", "易清洁", "静音效果好"],
                    "risks": ["价格偏高", "市场接受度待验证"],
                    "category": "风扇类"
                },
                {
                    "name": "手持小风扇",
                    "cost": 15,
                    "price_eu": 8.99,
                    "sales_prediction": 3000,
                    "score": 86,
                    "selling_points": ["超便携", "续航持久", "颜值高", "适合送礼"],
                    "risks": ["利润薄", "需要走量"],
                    "category": "风扇类"
                },
            ],
            "制冰机类": [
                {
                    "name": "家用小型制冰机",
                    "cost": 680,
                    "price_eu": 199.99,
                    "sales_prediction": 150,
                    "score": 90,
                    "selling_points": ["6分钟快速制冰", "自清洁功能", "静音设计", "大容量水箱"],
                    "risks": ["单价高", "售后成本高"],
                    "category": "制冰机类"
                },
                {
                    "name": "便携车载制冰机",
                    "cost": 450,
                    "price_eu": 129.99,
                    "sales_prediction": 200,
                    "score": 87,
                    "selling_points": ["车载两用", "小巧便携", "快速制冷", "低功耗"],
                    "risks": ["市场认知度低", "需要教育市场"],
                    "category": "制冰机类"
                },
                {
                    "name": "商用制冰机",
                    "cost": 2500,
                    "price_eu": 699.99,
                    "sales_prediction": 30,
                    "score": 78,
                    "selling_points": ["大容量产冰", "商用级品质", "24小时连续工作", "智能控温"],
                    "risks": ["客单价高", "目标客户少"],
                    "category": "制冰机类"
                },
            ],
            "冷感家纺类": [
                {
                    "name": "冰丝凉席三件套",
                    "cost": 80,
                    "price_eu": 29.99,
                    "sales_prediction": 800,
                    "score": 89,
                    "selling_points": ["冰丝材质凉爽舒适", "可机洗易打理", "多尺寸可选", "防滑设计"],
                    "risks": ["季节性强", "退货率较高"],
                    "category": "冷感家纺类"
                },
                {
                    "name": "冷感枕套",
                    "cost": 20,
                    "price_eu": 9.99,
                    "sales_prediction": 2000,
                    "score": 85,
                    "selling_points": ["Q-max冷感技术", "亲肤透气", "标准尺寸通用", "性价比高"],
                    "risks": ["单价低利润薄", "竞争激烈"],
                    "category": "冷感家纺类"
                },
                {
                    "name": "冷感夏被",
                    "cost": 120,
                    "price_eu": 39.99,
                    "sales_prediction": 500,
                    "score": 86,
                    "selling_points": ["双面冷感", "轻盈透气", "可水洗", "多色可选"],
                    "risks": ["季节性明显", "仓储压力大"],
                    "category": "冷感家纺类"
                },
                {
                    "name": "冷感床垫",
                    "cost": 200,
                    "price_eu": 59.99,
                    "sales_prediction": 300,
                    "score": 83,
                    "selling_points": ["大面积冷感", "防滑固定", "易于收纳", "改善睡眠质量"],
                    "risks": ["体积大物流成本高", "退换货麻烦"],
                    "category": "冷感家纺类"
                },
            ],
            "冰垫类": [
                {
                    "name": "凝胶冰垫",
                    "cost": 35,
                    "price_eu": 15.99,
                    "sales_prediction": 1500,
                    "score": 87,
                    "selling_points": ["凝胶材质持久冰凉", "无需注水", "多用途使用", "安全无毒"],
                    "risks": ["同质化严重", "价格战激烈"],
                    "category": "冰垫类"
                },
                {
                    "name": "宠物冰垫",
                    "cost": 25,
                    "price_eu": 12.99,
                    "sales_prediction": 1000,
                    "score": 84,
                    "selling_points": ["专为宠物设计", "耐抓咬", "易清洁", "多尺寸"],
                    "risks": ["细分市场", "受众有限"],
                    "category": "冰垫类"
                },
                {
                    "name": "汽车坐垫冰垫",
                    "cost": 45,
                    "price_eu": 19.99,
                    "sales_prediction": 800,
                    "score": 82,
                    "selling_points": ["汽车专用", "透气散热", "安装简单", "通用尺寸"],
                    "risks": ["季节性强", "汽车用品竞争激烈"],
                    "category": "冰垫类"
                },
            ],
            "便携制冷类": [
                {
                    "name": "迷你冷风机",
                    "cost": 120,
                    "price_eu": 39.99,
                    "sales_prediction": 600,
                    "score": 88,
                    "selling_points": ["加湿制冷二合一", "小巧不占地", "USB供电", "静音设计"],
                    "risks": ["效果有限", "客户期望管理"],
                    "category": "便携制冷类"
                },
                {
                    "name": "桌面空调扇",
                    "cost": 150,
                    "price_eu": 49.99,
                    "sales_prediction": 400,
                    "score": 85,
                    "selling_points": ["桌面专用", "三档调节", "水箱大容量", "氛围灯设计"],
                    "risks": ["竞争激烈", "差异化不足"],
                    "category": "便携制冷类"
                },
                {
                    "name": "挂脖风扇",
                    "cost": 60,
                    "price_eu": 24.99,
                    "sales_prediction": 1200,
                    "score": 86,
                    "selling_points": ["解放双手", "360度送风", "长续航", "时尚外观"],
                    "risks": ["佩戴舒适度", "噪音问题"],
                    "category": "便携制冷类"
                },
            ]
        }
        
        # 各国市场偏好系数
        self.country_preferences = {
            "德国": {"风扇类": 1.1, "制冰机类": 1.2, "冷感家纺类": 0.9, "冰垫类": 0.8, "便携制冷类": 1.0},
            "法国": {"风扇类": 1.0, "制冰机类": 1.0, "冷感家纺类": 1.1, "冰垫类": 0.9, "便携制冷类": 1.1},
            "意大利": {"风扇类": 1.2, "制冰机类": 1.3, "冷感家纺类": 1.0, "冰垫类": 1.1, "便携制冷类": 1.2},
            "西班牙": {"风扇类": 1.3, "制冰机类": 1.2, "冷感家纺类": 0.9, "冰垫类": 1.2, "便携制冷类": 1.1},
            "英国": {"风扇类": 0.9, "制冰机类": 0.8, "冷感家纺类": 1.2, "冰垫类": 0.7, "便携制冷类": 0.9},
            "荷兰": {"风扇类": 1.0, "制冰机类": 0.9, "冷感家纺类": 1.1, "冰垫类": 0.8, "便携制冷类": 1.0},
            "波兰": {"风扇类": 1.1, "制冰机类": 0.7, "冷感家纺类": 0.8, "冰垫类": 1.0, "便携制冷类": 0.8},
            "瑞典": {"风扇类": 0.7, "制冰机类": 0.6, "冷感家纺类": 0.9, "冰垫类": 0.6, "便携制冷类": 0.7},
        }
    
    def analyze(self, target_country: str, category: str, budget: Tuple[int, int], 
                risk_preference: str) -> Dict:
        """
        选品分析主方法
        
        Args:
            target_country: 目标国家
            category: 产品品类
            budget: 预算范围 (min, max)
            risk_preference: 风险偏好
            
        Returns:
            选品分析结果
        """
        # 筛选产品
        products = self._filter_products(category, budget)
        
        # 根据国家偏好调整评分
        products = self._adjust_by_country(products, target_country)
        
        # 根据风险偏好调整
        products = self._adjust_by_risk(products, risk_preference)
        
        # 排序取Top5
        products = sorted(products, key=lambda x: x['score'], reverse=True)[:5]
        
        # 生成趋势数据
        trend_data = self._generate_trend_data(target_country)
        
        # 生成选品建议
        suggestion = self._generate_suggestion(target_country, category, products)
        
        return {
            "products": products,
            "trend_data": trend_data,
            "suggestion": suggestion,
            "target_country": target_country,
            "category": category
        }
    
    def _filter_products(self, category: str, budget: Tuple[int, int]) -> List[Dict]:
        """筛选产品"""
        filtered = []
        
        if category == "全部":
            categories = self.product_db.keys()
        else:
            categories = [category]
        
        for cat in categories:
            if cat in self.product_db:
                for product in self.product_db[cat]:
                    # 预算检查（按100件采购计算）
                    total_cost = product['cost'] * 100
                    if budget[0] <= total_cost <= budget[1]:
                        filtered.append(product.copy())
        
        return filtered
    
    def _adjust_by_country(self, products: List[Dict], country: str) -> List[Dict]:
        """根据国家偏好调整评分"""
        if country not in self.country_preferences:
            return products
        
        preferences = self.country_preferences[country]
        
        for product in products:
            cat = product['category']
            if cat in preferences:
                # 调整评分
                product['score'] = round(product['score'] * preferences[cat], 1)
                # 调整销量预测
                product['sales_prediction'] = int(product['sales_prediction'] * preferences[cat])
        
        return products
    
    def _adjust_by_risk(self, products: List[Dict], risk_preference: str) -> List[Dict]:
        """根据风险偏好调整"""
        risk_factors = {
            "保守": 0.8,
            "稳健": 1.0,
            "积极": 1.1,
            "激进": 1.2
        }
        
        factor = risk_factors.get(risk_preference, 1.0)
        
        for product in products:
            # 风险偏好影响销量预测和评分
            product['sales_prediction'] = int(product['sales_prediction'] * factor)
            if risk_preference in ["积极", "激进"]:
                product['score'] = min(100, product['score'] + 2)
            elif risk_preference == "保守":
                product['score'] = max(60, product['score'] - 2)
        
        return products
    
    def _generate_trend_data(self, country: str) -> List[Dict]:
        """生成趋势数据"""
        months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        
        # 基础销量（受国家影响）
        base_sales = {
            "德国": 5000,
            "法国": 4500,
            "意大利": 5500,
            "西班牙": 5200,
            "英国": 4000,
        }.get(country, 4000)
        
        trend_data = []
        for i, month in enumerate(months):
            # 季节性波动，夏季高峰
            season_factor = 1 + 0.5 * abs(i - 6) / 6  # 7月最高
            if i >= 5 and i <= 8:  # 6-9月是旺季
                season_factor = 1.5 + random.uniform(-0.1, 0.1)
            else:
                season_factor = 0.5 + random.uniform(-0.1, 0.1)
            
            sales = int(base_sales * season_factor)
            trend_data.append({
                "月份": month,
                "销量": sales
            })
        
        return trend_data
    
    def _generate_suggestion(self, country: str, category: str, products: List[Dict]) -> str:
        """生成选品建议"""
        if not products:
            return "当前预算范围内没有找到合适的产品，建议调整预算范围。"
        
        top_product = products[0]
        
        suggestions = [
            f"根据{country}市场数据分析，我们推荐您重点关注「{top_product['name']}」。",
            f"该产品综合评分{top_product['score']}分，预计月销量{top_product['sales_prediction']}件，利润率约{int((top_product['price_eu'] * 7.5 - top_product['cost']) / (top_product['price_eu'] * 7.5) * 100)}%。",
        ]
        
        # 国家特定建议
        country_tips = {
            "德国": "德国消费者注重品质和能效，建议突出产品的节能特性和耐用性。",
            "法国": "法国消费者注重设计和美学，建议在营销中强调产品的外观设计和生活方式属性。",
            "意大利": "意大利夏季炎热，制冷产品需求旺盛，建议提前备货，抓住夏季销售旺季。",
            "西班牙": "西班牙市场对价格敏感度较高，建议主打性价比产品，同时关注亚马逊西班牙站的促销活动。",
            "英国": "英国市场相对成熟，消费者品牌意识强，建议注重品牌建设和产品品质。",
        }
        
        if country in country_tips:
            suggestions.append(country_tips[country])
        
        # 风险提示
        suggestions.append("⚠️ 注意：降温产品季节性明显，建议合理控制库存，避免淡季积压。")
        
        return "\n\n".join(suggestions)
    
    def process(self, input_data: Dict) -> Dict:
        """
        实现基类的process方法
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果
        """
        return self.analyze(
            target_country=input_data.get('target_country', '德国'),
            category=input_data.get('category', '全部'),
            budget=input_data.get('budget', (5000, 50000)),
            risk_preference=input_data.get('risk_preference', '稳健')
        )
