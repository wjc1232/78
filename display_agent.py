"""
商品智能展示智能体
自动生成商品详情页方案，智能优化排版

作者：凉贸通团队
版本：v1.0
日期：2026年6月
"""

from .base_agent import BaseAgent
from typing import Dict, List


class DisplayAgent(BaseAgent):
    """
    商品智能展示智能体
    负责详情页方案生成、排版优化、效果预测
    """
    
    def __init__(self):
        super().__init__("商品智能展示智能体")
        self._init_templates()
    
    def _init_templates(self):
        """初始化详情页模板"""
        self.templates = {
            "功能突出型": {
                "description": "以产品功能和参数为核心，适合科技感强的产品",
                "suitable_for": "电子产品、功能型产品、技术导向产品",
                "structure": [
                    "主图 + 核心卖点横幅",
                    "产品参数对比表",
                    "核心功能详解（配细节图）",
                    "使用场景展示",
                    "规格参数表",
                    "包装清单",
                    "售后保障"
                ],
                "conversion_boost": "+15-20%"
            },
            "场景氛围型": {
                "description": "以生活场景和情感共鸣为核心，适合家居类产品",
                "suitable_for": "家居用品、家纺、生活方式产品",
                "structure": [
                    "场景主图 + 情感化标题",
                    "痛点解决方案",
                    "生活场景展示（多图）",
                    "产品亮点提炼",
                    "用户评价/口碑",
                    "产品细节展示",
                    "品牌故事"
                ],
                "conversion_boost": "+20-25%"
            },
            "参数对比型": {
                "description": "以数据和对比为核心，适合功能性强的产品",
                "suitable_for": "家电、工具、性能导向产品",
                "structure": [
                    "主图 + 核心数据指标",
                    "vs 传统产品对比表",
                    "核心技术解析",
                    "性能测试数据",
                    "规格参数详表",
                    "适用场景说明",
                    "常见问题FAQ"
                ],
                "conversion_boost": "+10-15%"
            }
        }
    
    def generate(self, product_name: str, product_type: str, target_platform: str,
                 target_language: str, core_selling_points: List[str]) -> Dict:
        """
        生成详情页方案
        
        Args:
            product_name: 产品名称
            product_type: 产品类型
            target_platform: 目标平台
            target_language: 目标语言
            core_selling_points: 核心卖点
            
        Returns:
            生成结果
        """
        # 生成三套方案
        schemes = []
        for scheme_name, template in self.templates.items():
            scheme = self._generate_scheme(product_name, scheme_name, template, 
                                          core_selling_points, target_language)
            schemes.append(scheme)
        
        # 推荐方案
        recommendation = self._recommend_scheme(schemes, product_type)
        
        return {
            "schemes": schemes,
            "recommendation": recommendation,
            "product_name": product_name,
            "target_platform": target_platform
        }
    
    def _generate_scheme(self, product_name: str, scheme_name: str, 
                         template: Dict, selling_points: List[str], 
                         language: str) -> Dict:
        """生成单套方案"""
        
        # 根据语言生成示例文案
        if language == "英语":
            sample_copy = f"""Introducing our {product_name} - the perfect solution for your cooling needs!

{chr(10).join([f"✓ {sp}" for sp in selling_points[:3]])}

Experience the difference with our premium quality and innovative design. 
Order now and enjoy a cool and comfortable summer!"""
        elif language == "德语":
            sample_copy = f"""Entdecken Sie unseren {product_name} - die perfekte Lösung für Ihre Kühlbedürfnisse!

{chr(10).join([f"✓ {sp}" for sp in selling_points[:3]])}

Erleben Sie den Unterschied mit unserer Premium-Qualität und unserem innovativen Design.
Bestellen Sie jetzt und genießen Sie einen kühlen und komfortablen Sommer!"""
        elif language == "法语":
            sample_copy = f"""Découvrez notre {product_name} - la solution parfaite pour vos besoins de refroidissement !

{chr(10).join([f"✓ {sp}" for sp in selling_points[:3]])}

Découvrez la différence avec notre qualité premium et notre design innovant.
Commandez maintenant et profitez d'un été frais et confortable !"""
        else:
            sample_copy = f"{product_name}\n\n" + "\n".join([f"- {sp}" for sp in selling_points])
        
        return {
            "name": scheme_name,
            "description": template['description'],
            "suitable_for": template['suitable_for'],
            "structure": template['structure'],
            "conversion_boost": template['conversion_boost'],
            "sample_copy": sample_copy
        }
    
    def _recommend_scheme(self, schemes: List[Dict], product_type: str) -> Dict:
        """推荐方案"""
        
        # 根据产品类型推荐
        type_mapping = {
            "功能型": "功能突出型",
            "科技型": "功能突出型",
            "家居型": "场景氛围型",
            "时尚型": "场景氛围型",
        }
        
        recommended_name = type_mapping.get(product_type, "场景氛围型")
        
        # 找到推荐的方案
        recommended_scheme = next((s for s in schemes if s['name'] == recommended_name), schemes[0])
        
        reasons = [
            f"根据您的产品类型「{product_type}」，我们推荐使用「{recommended_name}」方案。",
            f"该方案{recommended_scheme['description']}",
            f"预计可提升转化率约{recommended_scheme['conversion_boost']}。",
            "建议根据实际产品图片和文案进行微调，以达到最佳效果。"
        ]
        
        return {
            "scheme": recommended_name,
            "reason": "\n\n".join(reasons)
        }
    
    def process(self, input_data: Dict) -> Dict:
        """实现基类的process方法"""
        return self.generate(
            product_name=input_data.get('product_name', '产品'),
            product_type=input_data.get('product_type', '功能型'),
            target_platform=input_data.get('target_platform', '亚马逊'),
            target_language=input_data.get('target_language', '英语'),
            core_selling_points=input_data.get('core_selling_points', [])
        )
