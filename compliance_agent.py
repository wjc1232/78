"""
跨境合规校验智能体
自动检查欧盟合规标准，计算进口税费

作者：凉贸通团队
版本：v1.0
日期：2026年6月
"""

from .base_agent import BaseAgent
from typing import Dict, List


class ComplianceAgent(BaseAgent):
    """
    跨境合规校验智能体
    负责合规检查、HS编码匹配、税费计算
    """
    
    def __init__(self):
        super().__init__("跨境合规校验智能体")
        self._init_compliance_db()
        self._init_tax_db()
    
    def _init_compliance_db(self):
        """初始化合规标准库"""
        self.compliance_standards = {
            "电子产品": [
                {"name": "CE认证", "required": True, "description": "欧盟强制安全认证", "level": "高"},
                {"name": "ROHS指令", "required": True, "description": "限制有害物质使用", "level": "高"},
                {"name": "REACH法规", "required": True, "description": "化学品注册评估授权", "level": "中"},
                {"name": "WEEE指令", "required": True, "description": "电子废弃物回收", "level": "中"},
                {"name": "ERP指令", "required": False, "description": "能效要求", "level": "中"},
                {"name": "电池指令", "required": False, "description": "电池环保要求（含电池产品）", "level": "高"},
            ],
            "家用电器": [
                {"name": "CE认证", "required": True, "description": "欧盟强制安全认证", "level": "高"},
                {"name": "ROHS指令", "required": True, "description": "限制有害物质使用", "level": "高"},
                {"name": "ERP指令", "required": True, "description": "能效标签要求", "level": "中"},
                {"name": "噪音指令", "required": False, "description": "噪音排放标准", "level": "低"},
            ],
            "纺织用品": [
                {"name": "REACH法规", "required": True, "description": "化学品限制要求", "level": "中"},
                {"name": "纺织品标签", "required": True, "description": "成分标签和护理标签", "level": "低"},
                {"name": "阻燃标准", "required": False, "description": "防火安全标准", "level": "中"},
                {"name": "OEKO-TEX认证", "required": False, "description": "生态纺织品认证", "level": "低"},
            ],
            "塑料制品": [
                {"name": "REACH法规", "required": True, "description": "化学品限制要求", "level": "中"},
                {"name": "食品接触材料", "required": False, "description": "食品接触安全标准", "level": "高"},
                {"name": "塑料指令", "required": True, "description": "塑料环保要求", "level": "低"},
            ],
        }
        
        # HS编码匹配规则
        self.hs_code_rules = {
            "风扇类": "84145990",
            "制冰机类": "84186990",
            "冷感家纺类": "63022290",
            "冰垫类": "39269090",
            "便携制冷类": "84186990",
        }
    
    def _init_tax_db(self):
        """初始化税费数据库"""
        self.tax_rates = {
            "德国": {"vat_rate": 19, "duty_rates": {"84145990": 2.7, "84186990": 2.0, "63022290": 12.0, "39269090": 6.5}},
            "法国": {"vat_rate": 20, "duty_rates": {"84145990": 2.7, "84186990": 2.0, "63022290": 12.0, "39269090": 6.5}},
            "意大利": {"vat_rate": 22, "duty_rates": {"84145990": 2.7, "84186990": 2.0, "63022290": 12.0, "39269090": 6.5}},
            "西班牙": {"vat_rate": 21, "duty_rates": {"84145990": 2.7, "84186990": 2.0, "63022290": 12.0, "39269090": 6.5}},
            "荷兰": {"vat_rate": 21, "duty_rates": {"84145990": 2.7, "84186990": 2.0, "63022290": 12.0, "39269090": 6.5}},
            "英国": {"vat_rate": 20, "duty_rates": {"84145990": 2.5, "84186990": 1.7, "63022290": 12.0, "39269090": 6.0}},
        }
    
    def check(self, product_name: str, product_category: str, material: str,
              has_battery: bool, target_country: str, declared_value: float,
              hs_code: str, certifications: Dict[str, bool]) -> Dict:
        """
        合规校验主方法
        
        Args:
            product_name: 产品名称
            product_category: 产品类别
            material: 主要材质
            has_battery: 是否含电池
            target_country: 目标国家
            declared_value: 申报价值
            hs_code: HS编码（可选）
            certifications: 认证情况
            
        Returns:
            合规校验结果
        """
        # HS编码匹配
        hs_code_suggestion = self._match_hs_code(product_category, hs_code)
        
        # 合规检查
        risks = self._check_compliance(product_category, has_battery, certifications)
        
        # 税费计算
        tax = self._calculate_tax(target_country, hs_code_suggestion, declared_value)
        
        # 计算合规评分
        score = self._calculate_score(risks)
        
        # 统计高风险项
        high_risk_count = sum(1 for r in risks if r['level'] == '高')
        
        # 生成整改建议
        summary_suggestion = self._generate_suggestion(risks, target_country)
        
        return {
            "score": score,
            "high_risk_count": high_risk_count,
            "hs_code_suggestion": hs_code_suggestion,
            "risks": risks,
            "tax": tax,
            "summary_suggestion": summary_suggestion,
            "product_name": product_name,
            "target_country": target_country
        }
    
    def _match_hs_code(self, category: str, user_hs_code: str) -> str:
        """匹配HS编码"""
        if user_hs_code:
            return user_hs_code
        
        # 根据品类匹配
        for cat, code in self.hs_code_rules.items():
            if cat in category or category in cat:
                return code
        
        return "84798999"  # 默认编码
    
    def _check_compliance(self, category: str, has_battery: bool, 
                          certifications: Dict[str, bool]) -> List[Dict]:
        """检查合规性"""
        risks = []
        
        # 获取适用的合规标准
        standards = self.compliance_standards.get(category, self.compliance_standards["电子产品"])
        
        for standard in standards:
            # 电池产品额外检查
            if standard['name'] == "电池指令" and not has_battery:
                continue
            
            cert_name = standard['name'].split('认证')[0].split('指令')[0].split('法规')[0]
            
            # 检查是否有认证
            has_cert = False
            for key in certifications:
                if cert_name in key or key in cert_name:
                    has_cert = certifications[key]
                    break
            
            if standard['required'] and not has_cert:
                risks.append({
                    "name": standard['name'],
                    "level": standard['level'],
                    "description": f"缺少{standard['name']}：{standard['description']}",
                    "suggestion": f"建议尽快办理{standard['name']}，可联系第三方认证机构办理，周期约4-8周，费用约5000-20000元。"
                })
            elif not standard['required'] and not has_cert:
                risks.append({
                    "name": standard['name'],
                    "level": "低",
                    "description": f"建议办理{standard['name']}：{standard['description']}",
                    "suggestion": f"虽然{standard['name']}非强制要求，但办理后可提升产品竞争力和消费者信任度。"
                })
        
        # 如果含电池但没有电池指令相关认证
        if has_battery:
            has_battery_cert = any('电池' in k for k, v in certifications.items() if v)
            if not has_battery_cert:
                risks.append({
                    "name": "电池指令",
                    "level": "高",
                    "description": "产品含电池，但未提供电池相关合规认证",
                    "suggestion": "含电池产品必须符合欧盟电池指令要求，建议提供电池的UN38.3测试报告和CE认证。"
                })
        
        return risks
    
    def _calculate_tax(self, country: str, hs_code: str, declared_value: float) -> Dict:
        """计算税费"""
        if country not in self.tax_rates:
            country = "德国"  # 默认
        
        tax_info = self.tax_rates[country]
        vat_rate = tax_info['vat_rate']
        
        # 获取关税率
        duty_rate = tax_info['duty_rates'].get(hs_code, 5.0)  # 默认5%
        
        # 计算关税
        duty_amount = round(declared_value * duty_rate / 100, 2)
        
        # 计算VAT（基于CIF价值+关税）
        cif_value = declared_value + duty_amount + 50  # 假设运费保险50USD
        vat_amount = round(cif_value * vat_rate / 100, 2)
        
        # 其他费用
        other_fees = round(declared_value * 0.02, 2)  # 清关费等
        
        total = round(duty_amount + vat_amount + other_fees, 2)
        
        return {
            "duty_rate": duty_rate,
            "duty_amount": duty_amount,
            "vat_rate": vat_rate,
            "vat_amount": vat_amount,
            "other_fees": other_fees,
            "total": total
        }
    
    def _calculate_score(self, risks: List[Dict]) -> int:
        """计算合规评分"""
        score = 100
        
        for risk in risks:
            if risk['level'] == '高':
                score -= 15
            elif risk['level'] == '中':
                score -= 8
            else:
                score -= 3
        
        return max(0, min(100, score))
    
    def _generate_suggestion(self, risks: List[Dict], country: str) -> str:
        """生成整改建议"""
        high_risks = [r for r in risks if r['level'] == '高']
        mid_risks = [r for r in risks if r['level'] == '中']
        
        suggestions = []
        
        if high_risks:
            suggestions.append(f"🔴 **高风险项（{len(high_risks)}项）：** 建议优先处理，这些是欧盟强制要求，缺失可能导致产品被扣、罚款甚至禁止入境。")
            for r in high_risks:
                suggestions.append(f"   - {r['name']}：{r['suggestion']}")
        
        if mid_risks:
            suggestions.append(f"\n🟡 **中风险项（{len(mid_risks)}项）：** 建议尽快完善，这些会影响产品竞争力和用户信任度。")
            for r in mid_risks:
                suggestions.append(f"   - {r['name']}：{r['suggestion']}")
        
        suggestions.append(f"\n💡 **总体建议：**")
        suggestions.append(f"1. 建议优先办理高风险项的认证，确保产品能够顺利清关")
        suggestions.append(f"2. 出口{country}前建议咨询专业的合规顾问，确保符合当地最新法规")
        suggestions.append(f"3. 建议在产品包装和说明书上标注CE标识和相关合规信息")
        suggestions.append(f"4. 税费方面，预计总税费约为申报价值的15-25%，请在定价时充分考虑")
        
        return "\n".join(suggestions)
    
    def process(self, input_data: Dict) -> Dict:
        """实现基类的process方法"""
        return self.check(
            product_name=input_data.get('product_name', '产品'),
            product_category=input_data.get('product_category', '电子产品'),
            material=input_data.get('material', ''),
            has_battery=input_data.get('has_battery', False),
            target_country=input_data.get('target_country', '德国'),
            declared_value=input_data.get('declared_value', 1000.0),
            hs_code=input_data.get('hs_code', ''),
            certifications=input_data.get('certifications', {})
        )
