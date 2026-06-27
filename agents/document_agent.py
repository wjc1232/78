"""
单证处理智能体
自动生成各类出口单证，智能校验数据一致性

作者：凉贸通团队
版本：v1.0
日期：2026年6月
"""

from .base_agent import BaseAgent
from typing import Dict, List
from datetime import datetime


class DocumentAgent(BaseAgent):
    """
    单证处理智能体
    负责单证生成、数据校验、格式转换
    """
    
    def __init__(self):
        super().__init__("单证处理智能体")
        self._init_templates()
    
    def _init_templates(self):
        """初始化单证模板"""
        self.templates = {
            "商业发票": self._invoice_template,
            "装箱单": self._packing_list_template,
            "原产地证": self._certificate_origin_template,
            "符合性声明": self._doc_template,
            "报关单": self._customs_declaration_template,
        }
    
    def generate(self, order_info: Dict, products: List[Dict], doc_types: List[str]) -> Dict:
        """
        生成单证
        
        Args:
            order_info: 订单信息
            products: 产品列表
            doc_types: 单证类型列表
            
        Returns:
            生成结果
        """
        documents = []
        validation_warnings = []
        
        # 数据校验
        validation_result = self._validate_data(order_info, products)
        if not validation_result['passed']:
            validation_warnings = validation_result['warnings']
        
        # 生成各类型单证
        for doc_type in doc_types:
            if doc_type in self.templates:
                doc_content = self.templates[doc_type](order_info, products)
                documents.append({
                    "name": doc_type,
                    "content": doc_content,
                    "filename": f"{doc_type}_{order_info['order_no']}.txt"
                })
        
        return {
            "documents": documents,
            "validation": {
                "passed": len(validation_warnings) == 0,
                "warnings": validation_warnings,
                "errors": []
            },
            "order_info": order_info
        }
    
    def _validate_data(self, order_info: Dict, products: List[Dict]) -> Dict:
        """数据校验"""
        warnings = []
        passed = True
        
        # 检查必填字段
        required_fields = ['order_no', 'buyer_name', 'seller_name']
        for field in required_fields:
            if not order_info.get(field):
                warnings.append(f"订单信息缺少必填字段：{field}")
                passed = False
        
        # 检查产品数据
        if not products:
            warnings.append("产品列表为空")
            passed = False
        else:
            for i, product in enumerate(products, 1):
                # 检查数量和单价
                qty = product.get('数量', 0)
                price = product.get('单价(USD)', 0)
                if qty <= 0:
                    warnings.append(f"第{i}个产品数量异常")
                if price <= 0:
                    warnings.append(f"第{i}个产品单价异常")
                
                # 检查HS编码格式
                hs_code = product.get('HS编码', '')
                if hs_code and len(hs_code) != 8:
                    warnings.append(f"第{i}个产品HS编码格式可能不正确（建议8位）")
        
        return {
            "passed": passed,
            "warnings": warnings
        }
    
    def _invoice_template(self, order_info: Dict, products: List[Dict]) -> str:
        """商业发票模板"""
        total_amount = sum(p.get('数量', 0) * p.get('单价(USD)', 0) for p in products)
        total_qty = sum(p.get('数量', 0) for p in products)
        
        products_table = ""
        for i, p in enumerate(products, 1):
            amount = p.get('数量', 0) * p.get('单价(USD)', 0)
            products_table += f"{i}. {p.get('产品名称', '')}\tHS: {p.get('HS编码', '')}\tQty: {p.get('数量', 0)}\tUnit Price: ${p.get('单价(USD)', 0):.2f}\tAmount: ${amount:.2f}\n"
        
        return f"""
================================================================================
                            COMMERCIAL INVOICE（商业发票）
================================================================================

Invoice No.（发票号）: {order_info.get('order_no', '')}
Date（日期）: {order_info.get('order_date', datetime.now().strftime('%Y-%m-%d'))}

Seller（卖方）:
{order_info.get('seller_name', '')}
Yiwu, Zhejiang, China
Tel: +86-xxx-xxxx-xxxx

Buyer（买方）:
{order_info.get('buyer_name', '')}
{order_info.get('buyer_country', '')}
Tel: xxx-xxxx-xxxx

Trade Term（贸易术语）: {order_info.get('trade_term', 'FOB')}

--------------------------------------------------------------------------------
序号  产品名称              HS编码      数量    单价(USD)    金额(USD)
--------------------------------------------------------------------------------
{products_table}
--------------------------------------------------------------------------------
Total（合计）: {total_qty} pcs                                          ${total_amount:.2f}

SAY TOTAL: U.S. DOLLARS {self._number_to_words(total_amount)} ONLY

--------------------------------------------------------------------------------
Remarks（备注）:
1. 原产地：中国
2. 付款方式：T/T

Authorized Signature（授权签字）:
_________________________
Date: _______________

================================================================================
"""
    
    def _packing_list_template(self, order_info: Dict, products: List[Dict]) -> str:
        """装箱单模板"""
        total_qty = sum(p.get('数量', 0) for p in products)
        total_weight = sum(p.get('数量', 0) * p.get('毛重(kg)', 0) for p in products)
        total_volume = sum(p.get('数量', 0) * p.get('体积(m³)', 0) for p in products)
        
        products_table = ""
        for i, p in enumerate(products, 1):
            products_table += f"{i}. {p.get('产品名称', '')}\tQty: {p.get('数量', 0)}pcs\tG.W.: {p.get('数量', 0) * p.get('毛重(kg)', 0):.2f}kg\tVol.: {p.get('数量', 0) * p.get('体积(m³)', 0):.4f}m³\n"
        
        return f"""
================================================================================
                            PACKING LIST（装箱单）
================================================================================

Invoice No.（发票号）: {order_info.get('order_no', '')}
Date（日期）: {order_info.get('order_date', datetime.now().strftime('%Y-%m-%d'))}

Seller（卖方）:
{order_info.get('seller_name', '')}

Buyer（买方）:
{order_info.get('buyer_name', '')}
{order_info.get('buyer_country', '')}

--------------------------------------------------------------------------------
序号  产品名称              数量       毛重           体积
--------------------------------------------------------------------------------
{products_table}
--------------------------------------------------------------------------------
Total（合计）: {total_qty} pcs    {total_weight:.2f} kg    {total_volume:.4f} m³

--------------------------------------------------------------------------------
Packing Details（包装明细）:
- 包装方式：标准出口纸箱
- 每箱数量：按产品规格
- 唛头：按买方要求

Remarks（备注）:
1. 以上数据仅供参考，以实际出货为准
2. 如需详细装箱明细，请联系我方

Authorized Signature（授权签字）:
_________________________
Date: _______________

================================================================================
"""
    
    def _certificate_origin_template(self, order_info: Dict, products: List[Dict]) -> str:
        """原产地证模板"""
        return f"""
================================================================================
                    CERTIFICATE OF ORIGIN（原产地证书）
================================================================================

Certificate No.（证书号）: C/O-{order_info.get('order_no', '')}
Date（日期）: {order_info.get('order_date', datetime.now().strftime('%Y-%m-%d'))}

Exporter（出口商）:
{order_info.get('seller_name', '')}
Yiwu, Zhejiang, China

Consignee（收货人）:
{order_info.get('buyer_name', '')}
{order_info.get('buyer_country', '')}

Means of transport and route（运输方式和路线）:
From Yiwu, China to {order_info.get('buyer_country', '')} by sea/air

Country / region of destination（目的国/地区）:
{order_info.get('buyer_country', '')}

--------------------------------------------------------------------------------
项号  产品名称              HS编码      数量       原产地标准
--------------------------------------------------------------------------------
1.   降温产品类             8414/6302   按发票     完全原产（P）
--------------------------------------------------------------------------------

Declaration by the exporter（出口商声明）:
The undersigned hereby declares that the above details and statements are correct,
that all the goods were produced in China and that they comply with the Rules of
Origin of the People's Republic of China.

Place and date, signature and stamp of authorized signatory:
Yiwu, {order_info.get('order_date', datetime.now().strftime('%Y-%m-%d'))}
_________________________
(Authorized Signatory)

Certification（证明）:
It is hereby certified, on the basis of control carried out, that the declaration
by the exporter is correct.

Place and date, signature and stamp of certifying authority:
_________________________
(Certifying Authority)

================================================================================
"""
    
    def _doc_template(self, order_info: Dict, products: List[Dict]) -> str:
        """符合性声明模板"""
        return f"""
================================================================================
                DECLARATION OF CONFORMITY（符合性声明）
================================================================================

Manufacturer（制造商）:
{order_info.get('seller_name', '')}
Yiwu, Zhejiang, China

Product Information（产品信息）:
- Product Category: Cooling Products
- Product Models: Various models (see invoice)
- Standard: EN 60335-1 / EN 60335-2-80

Declaration（声明）:
We hereby declare that the above-mentioned products are in conformity with the
following directives and standards:

- Low Voltage Directive (LVD) 2014/35/EU
- Electromagnetic Compatibility (EMC) Directive 2014/30/EU
- RoHS Directive 2011/65/EU
- REACH Regulation (EC) No 1907/2006

The products bear the CE marking in accordance with the provisions of the
above-mentioned directives.

Technical Documentation（技术文件）:
The technical documentation required by the directives is available at the
manufacturer's premises and can be provided upon request.

Place and Date（地点和日期）:
Yiwu, China, {order_info.get('order_date', datetime.now().strftime('%Y-%m-%d'))}

Authorized Representative（授权代表）:
_________________________
Name: [Authorized Person Name]
Title: [Title]
Signature: _________________

================================================================================
"""
    
    def _customs_declaration_template(self, order_info: Dict, products: List[Dict]) -> str:
        """报关单模板"""
        total_amount = sum(p.get('数量', 0) * p.get('单价(USD)', 0) for p in products)
        
        return f"""
================================================================================
                    EXPORT DECLARATION（出口报关单）
================================================================================

Declaration No.（报关单号）: DEC-{order_info.get('order_no', '')}
Date（日期）: {order_info.get('order_date', datetime.now().strftime('%Y-%m-%d'))}

Exporter（出口商）:
{order_info.get('seller_name', '')}
Yiwu, Zhejiang, China
Customs Code: 33XXXXXX

Consignee（收货人）:
{order_info.get('buyer_name', '')}
{order_info.get('buyer_country', '')}

Transport Information（运输信息）:
- Mode of Transport: Sea / Air
- Port of Loading: Ningbo / Shanghai
- Port of Destination: {order_info.get('buyer_country', '')}
- Trade Term: {order_info.get('trade_term', 'FOB')}

Goods Information（货物信息）:
- Total Value: USD {total_amount:.2f}
- Currency: USD
- Country of Origin: China
- Number of Packages: [Number]

Item Details（商品明细）:
(详见随附发票和装箱单)

Declaration（申报声明）:
We hereby declare that the above information is true and correct.

Declarant（申报人）:
_________________________
Name: [Declarant Name]
Customs Declaration Certificate No.: [Certificate No.]
Date: {order_info.get('order_date', datetime.now().strftime('%Y-%m-%d'))}

================================================================================
"""
    
    def _number_to_words(self, amount: float) -> str:
        """数字转英文（简化版）"""
        # 简化实现，实际项目中可以用更完整的库
        dollars = int(amount)
        cents = int((amount - dollars) * 100)
        
        if cents > 0:
            return f"{dollars} AND {cents}/100"
        else:
            return f"{dollars}"
    
    def process(self, input_data: Dict) -> Dict:
        """实现基类的process方法"""
        return self.generate(
            order_info=input_data.get('order_info', {}),
            products=input_data.get('products', []),
            doc_types=input_data.get('doc_types', ['商业发票', '装箱单'])
        )
