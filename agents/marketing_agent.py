"""
多语种营销智能体
一键生成多语言、多平台营销文案

作者：凉贸通团队
版本：v1.0
日期：2026年6月
"""

from .base_agent import BaseAgent
from typing import Dict, List


class MarketingAgent(BaseAgent):
    """
    多语种营销智能体
    负责文案生成、多语言翻译、关键词优化
    """
    
    def __init__(self):
        super().__init__("多语种营销智能体")
        self._init_keyword_db()
        self._init_copy_templates()
    
    def _init_keyword_db(self):
        """初始化关键词库"""
        self.keyword_db = {
            "风扇类": {
                "英语": ["fan", "cooling fan", "electric fan", "portable fan", "quiet fan", "energy saving fan"],
                "德语": ["Lüfter", "Ventilator", "Kühlventilator", "leiser Lüfter", "Tischventilator"],
                "法语": ["ventilateur", "ventilateur de refroidissement", "ventilateur silencieux"],
                "意大利语": ["ventilatore", "ventola", "ventilatore raffreddante"],
                "西班牙语": ["ventilador", "ventilador de enfriamiento", "ventilador portátil"],
                "荷兰语": ["ventilator", "koelventilator", "stille ventilator"],
                "波兰语": ["wentylator", "wentylator chłodzący", "cichy wentylator"],
                "瑞典语": ["fläkt", "kylfläkt", "tystlös fläkt"],
            },
            "制冰机类": {
                "英语": ["ice maker", "ice machine", "portable ice maker", "countertop ice maker"],
                "德语": ["Eismaschine", "Eiswürfelmaschine", "tragbare Eismaschine"],
                "法语": ["machine à glaçons", "fabricant de glace", "machine à glace portable"],
                "意大利语": ["macchina del ghiaccio", "fabbricatore di ghiaccio"],
                "西班牙语": ["máquina de hielo", "fabricadora de hielo"],
                "荷兰语": ["ijsmachine", "ijsklontjesmachine"],
                "波兰语": ["maszyna do lodu", "kostkarka do lodu"],
                "瑞典语": ["ismaskin", "bärbar ismaskin"],
            },
            "冷感家纺类": {
                "英语": ["cooling blanket", "cooling pillowcase", "bamboo sheets", "cooling mattress"],
                "德语": ["Kühldecke", "Kühlkissenbezug", "Bambusbettwäsche"],
                "法语": ["couverture rafraîchissante", "taie d'oreiller rafraîchissante"],
                "意大利语": ["coperta rinfrescante", "federa rinfrescante"],
                "西班牙语": ["manta refrescante", "fundas de almohada refrescantes"],
                "荷兰语": ["koeldeken", "koel kussensloop"],
                "波兰语": ["koc chłodzący", "poszewka chłodząca"],
                "瑞典语": ["kylfilt", "kylkuddfodral"],
            },
            "冰垫类": {
                "英语": ["cooling mat", "gel cooling pad", "ice mat", "cooling pillow"],
                "德语": ["Kühlmatte", "Gel-Kühlkissen", "Eismatte"],
                "法语": ["tapis rafraîchissant", "coussin de refroidissement en gel"],
                "意大利语": ["tappetino rinfrescante", "cuscinetto di raffreddamento in gel"],
                "西班牙语": ["alfombrilla refrescante", "almohadilla de gel refrescante"],
                "荷兰语": ["koelmat", "gel koelkussen"],
                "波兰语": ["mata chłodząca", "poduszka chłodząca żelowa"],
                "瑞典语": ["kylmatta", "gelkylkudde"],
            },
        }
    
    def _init_copy_templates(self):
        """初始化文案模板"""
        self.copy_templates = {
            "亚马逊": {
                "title_length": 200,
                "bullets_count": 5,
                "description_length": 2000,
                "style": "专业、功能导向"
            },
            "速卖通": {
                "title_length": 128,
                "bullets_count": 3,
                "description_length": 1000,
                "style": "促销、性价比导向"
            },
            "eBay": {
                "title_length": 80,
                "bullets_count": 4,
                "description_length": 1500,
                "style": "简洁、拍卖风格"
            },
            "独立站": {
                "title_length": 60,
                "bullets_count": 6,
                "description_length": 3000,
                "style": "品牌化、故事性"
            },
        }
    
    def generate(self, product_name: str, product_category: str, price: float,
                 core_features: List[str], target_platform: str, languages: List[str]) -> Dict:
        """
        生成多语言营销文案
        
        Args:
            product_name: 产品名称
            product_category: 产品品类
            price: 产品售价
            core_features: 核心卖点列表
            target_platform: 目标平台
            languages: 目标语言列表
            
        Returns:
            生成结果
        """
        # 获取关键词
        keywords = self._get_keywords(product_category, languages)
        
        # 生成各语言文案
        copies = []
        for lang in languages:
            copy = self._generate_copy(product_name, price, core_features, target_platform, lang)
            copies.append(copy)
        
        return {
            "keywords": keywords,
            "copies": copies,
            "product_name": product_name,
            "target_platform": target_platform
        }
    
    def _get_keywords(self, category: str, languages: List[str]) -> List[Dict]:
        """获取关键词"""
        result = []
        
        if category not in self.keyword_db:
            category = "风扇类"  # 默认
        
        for lang in languages:
            if lang in self.keyword_db[category]:
                result.append({
                    "语言": lang,
                    "核心关键词": ", ".join(self.keyword_db[category][lang][:3]),
                    "长尾关键词": ", ".join(self.keyword_db[category][lang][3:])
                })
        
        return result
    
    def _generate_copy(self, product_name: str, price: float, core_features: List[str],
                       platform: str, language: str) -> Dict:
        """生成单语言文案"""
        
        # 根据语言生成不同的文案
        if language == "英语":
            title = f"{product_name.title()} - Powerful Cooling Fan with Quiet Operation, Energy Efficient, Perfect for Home and Office"
            bullets = [
                f"【Powerful Cooling】{core_features[0] if len(core_features) > 0 else 'Strong airflow for instant cooling'}",
                f"【Ultra Quiet】{core_features[1] if len(core_features) > 1 else 'Noise reduction technology for peaceful environment'}",
                f"【Energy Saving】{core_features[2] if len(core_features) > 2 else 'Low power consumption saves your electricity bill'}",
                f"【Portable Design】{core_features[3] if len(core_features) > 3 else 'Lightweight and easy to move anywhere'}",
                f"【Quality Guarantee】{core_features[4] if len(core_features) > 4 else 'High quality materials ensure long service life'}",
            ]
            description = f"""Experience ultimate cooling comfort with our premium {product_name}!

Perfect for hot summer days, this cooling fan delivers powerful airflow while maintaining whisper-quiet operation. Whether you're working, sleeping, or relaxing, it creates the perfect comfortable environment for you.

Key Features:
• {core_features[0] if len(core_features) > 0 else 'Powerful airflow'}
• {core_features[1] if len(core_features) > 1 else 'Ultra quiet operation'}
• {core_features[2] if len(core_features) > 2 else 'Energy efficient design'}
• {core_features[3] if len(core_features) > 3 else 'Portable and lightweight'}
• {core_features[4] if len(core_features) > 4 else 'High quality construction'}

Don't let the heat slow you down. Get your {product_name} today and stay cool all summer long!

Price: €{price:.2f}"""
        
        elif language == "德语":
            title = f"{product_name} - Leistungsstarker Ventilator mit leisem Betrieb, energieeffizient, perfekt für Zuhause und Büro"
            bullets = [
                f"【Starke Kühlung】{core_features[0] if len(core_features) > 0 else 'Starker Luftstrom für sofortige Kühlung'}",
                f"【Ultra-leise】{core_features[1] if len(core_features) > 1 else 'Geräuschreduzierungstechnologie für ruhige Umgebung'}",
                f"【Energiesparend】{core_features[2] if len(core_features) > 2 else 'Niedriger Stromverbrauch spart Ihre Stromrechnung'}",
                f"【Tragbares Design】{core_features[3] if len(core_features) > 3 else 'Leicht und einfach überall hin zu bewegen'}",
                f"【Qualitätsgarantie】{core_features[4] if len(core_features) > 4 else 'Hochwertige Materialien gewährleisten lange Lebensdauer'}",
            ]
            description = f"""Erleben Sie ultimativen Kühlkomfort mit unserem Premium-{product_name}!

Perfekt für heiße Sommertage liefert dieser Ventilator starken Luftstrom bei flüsterleisem Betrieb. Egal ob Sie arbeiten, schlafen oder entspannen - er schafft die perfekte komfortable Umgebung für Sie.

Hauptmerkmale:
• {core_features[0] if len(core_features) > 0 else 'Starker Luftstrom'}
• {core_features[1] if len(core_features) > 1 else 'Ultra-leiser Betrieb'}
• {core_features[2] if len(core_features) > 2 else 'Energieeffizientes Design'}
• {core_features[3] if len(core_features) > 3 else 'Tragbar und leicht'}
• {core_features[4] if len(core_features) > 4 else 'Hochwertige Verarbeitung'}

Lassen Sie sich von der Hitze nicht ausbremsen. Holen Sie sich noch heute Ihren {product_name} und bleiben Sie den ganzen Sommer über kühl!

Preis: €{price:.2f}"""
        
        elif language == "法语":
            title = f"{product_name} - Ventilateur Puissant avec Fonctionnement Silencieux, Économe en Énergie, Parfait pour la Maison et le Bureau"
            bullets = [
                f"【Refroidissement Puissant】{core_features[0] if len(core_features) > 0 else 'Flux d air puissant pour un refroidissement instantané'}",
                f"【Ultra Silencieux】{core_features[1] if len(core_features) > 1 else 'Technologie de réduction du bruit pour un environnement paisible'}",
                f"【Économe en Énergie】{core_features[2] if len(core_features) > 2 else 'Basse consommation électrique pour économiser sur votre facture'}",
                f"【Design Portable】{core_features[3] if len(core_features) > 3 else 'Léger et facile à déplacer partout'}",
                f"【Garantie Qualité】{core_features[4] if len(core_features) > 4 else 'Matériaux de haute qualité pour une longue durée de vie'}",
            ]
            description = f"""Découvrez le confort de refroidissement ultime avec notre {product_name} premium !

Parfait pour les journées d'été chaudes, ce ventilateur délivre un flux d'air puissant tout en fonctionnant en silence. Que vous travailliez, dormiez ou vous détendiez, il crée l'environnement confortable parfait pour vous.

Caractéristiques Clés :
• {core_features[0] if len(core_features) > 0 else 'Flux d air puissant'}
• {core_features[1] if len(core_features) > 1 else 'Fonctionnement ultra silencieux'}
• {core_features[2] if len(core_features) > 2 else 'Design économe en énergie'}
• {core_features[3] if len(core_features) > 3 else 'Portable et léger'}
• {core_features[4] if len(core_features) > 4 else 'Construction de haute qualité'}

Ne laissez pas la chaleur vous ralentir. Procurez-vous votre {product_name} dès aujourd'hui et restez au frais tout l'été !

Prix : €{price:.2f}"""

                    elif language == "意大利语":
            title = f"{product_name} - Ventilatore Potente con Funzionamento Silenzioso, Energeticamente Efficiente, Perfetto per Casa e Ufficio"
            bullets = [
                f"【Raffreddamento Potente】{core_features[0] if len(core_features) > 0 else 'Flusso d\'aria potente per un raffreddamento istantaneo'}",
                f"【Ultra Silenzioso】{core_features[1] if len(core_features) > 1 else 'Tecnologia di riduzione del rumore per un ambiente tranquillo'}",
                f"【Risparmio Energetico】{core_features[2] if len(core_features) > 2 else 'Basso consumo energetico che riduce la bolletta'}",
                f"【Design Portatile】{core_features[3] if len(core_features) > 3 else 'Leggero e facile da spostare ovunque'}",
                f"【Garanzia di Qualità】{core_features[4] if len(core_features) > 4 else 'Materiali di alta qualità per una lunga durata'}",
            ]
            description = f"""Scopri il massimo comfort con il nostro {product_name} premium!

Perfetto per le calde giornate estive, questo ventilatore offre un flusso d'aria potente mantenendo un funzionamento silenzioso. Che tu stia lavorando, dormendo o rilassandoti, crea l'ambiente confortevole ideale per te.

Caratteristiche Principali:
• {core_features[0] if len(core_features) > 0 else 'Flusso d\'aria potente'}
• {core_features[1] if len(core_features) > 1 else 'Funzionamento ultra silenzioso'}
• {core_features[2] if len(core_features) > 2 else 'Design a risparmio energetico'}
• {core_features[3] if len(core_features) > 3 else 'Portatile e leggero'}
• {core_features[4] if len(core_features) > 4 else 'Costruzione di alta qualità'}

Non lasciare che il caldo ti rallenti. Acquista oggi il tuo {product_name} e rimani fresco tutta l'estate!

Prezzo: €{price:.2f}"""

        elif language == "西班牙语":
            title = f"{product_name} - Ventilador Potente con Funcionamiento Silencioso, Eficiente Energéticamente, Perfecto para Hogar y Oficina"
            bullets = [
                f"【Enfriamiento Potente】{core_features[0] if len(core_features) > 0 else 'Flujo de aire potente para un enfriamiento instantáneo'}",
                f"【Ultra Silencioso】{core_features[1] if len(core_features) > 1 else 'Tecnología de reducción de ruido para un ambiente tranquilo'}",
                f"【Ahorro de Energía】{core_features[2] if len(core_features) > 2 else 'Bajo consumo eléctrico que reduce tu factura'}",
                f"【Diseño Portátil】{core_features[3] if len(core_features) > 3 else 'Ligero y fácil de mover a cualquier lugar'}",
                f"【Garantía de Calidad】{core_features[4] if len(core_features) > 4 else 'Materiales de alta calidad para una larga vida útil'}",
            ]
            description = f"""¡Experimenta el máximo confort de enfriamiento con nuestro {product_name} premium!

Perfecto para los calurosos días de verano, este ventilador ofrece un potente flujo de aire manteniendo un funcionamiento ultrasilencioso. Ya sea que estés trabajando, durmiendo o relajándote, crea el ambiente perfecto para ti.

Características Principales:
• {core_features[0] if len(core_features) > 0 else 'Flujo de aire potente'}
• {core_features[1] if len(core_features) > 1 else 'Funcionamiento ultrasilencioso'}
• {core_features[2] if len(core_features) > 2 else 'Diseño de bajo consumo'}
• {core_features[3] if len(core_features) > 3 else 'Portátil y ligero'}
• {core_features[4] if len(core_features) > 4 else 'Construcción de alta calidad'}

¡No dejes que el calor te detenga. Consigue tu {product_name} hoy y mantente fresco todo el verano!

Precio: €{price:.2f}"""

        elif language == "荷兰语":
            title = f"{product_name} - Krachtige Ventilator met Stille Werking, Energiezuinig, Perfect voor Thuis en Kantoor"
            bullets = [
                f"【Krachtige Koeling】{core_features[0] if len(core_features) > 0 else 'Krachtige luchtstroom voor directe verkoeling'}",
                f"【Ultra Stil】{core_features[1] if len(core_features) > 1 else 'Geluidreductietechnologie voor een rustige omgeving'}",
                f"【Energiebesparend】{core_features[2] if len(core_features) > 2 else 'Laag stroomverbruik verlaagt uw energierekening'}",
                f"【Draagbaar Ontwerp】{core_features[3] if len(core_features) > 3 else 'Licht en gemakkelijk overal mee naartoe te nemen'}",
                f"【Kwaliteitsgarantie】{core_features[4] if len(core_features) > 4 else 'Hoogwaardige materialen voor een lange levensduur'}",
            ]
            description = f"""Ervaar ultiem koelcomfort met onze premium {product_name}!

Perfect voor hete zomerdagen levert deze ventilator een krachtige luchtstroom terwijl hij fluisterstil werkt. Of u nu werkt, slaapt of ontspant, hij creëert de perfecte comfortabele omgeving voor u.

Belangrijkste Kenmerken:
• {core_features[0] if len(core_features) > 0 else 'Krachtige luchtstroom'}
• {core_features[1] if len(core_features) > 1 else 'Ultra stille werking'}
• {core_features[2] if len(core_features) > 2 else 'Energiezuinig ontwerp'}
• {core_features[3] if len(core_features) > 3 else 'Draagbaar en licht'}
• {core_features[4] if len(core_features) > 4 else 'Hoogwaardige constructie'}

Laat de hitte u niet vertragen. Haal vandaag nog uw {product_name} en blijf de hele zomer koel!

Prijs: €{price:.2f}"""

        elif language == "波兰语":
            title = f"{product_name} - Mocny Wentylator z Cichą Pracą, Energooszczędny, Idealny do Domu i Biura"
            bullets = [
                f"【Mocne Chłodzenie】{core_features[0] if len(core_features) > 0 else 'Mocny przepływ powietrza dla natychmiastowego chłodzenia'}",
                f"【Ultra Cichy】{core_features[1] if len(core_features) > 1 else 'Technologia redukcji hałasu dla spokojnego otoczenia'}",
                f"【Oszczędność Energii】{core_features[2] if len(core_features) > 2 else 'Niskie zużycie energii obniża rachunki za prąd'}",
                f"【Przenośny Design】{core_features[3] if len(core_features) > 3 else 'Lekki i łatwy do przenoszenia wszędzie'}",
                f"【Gwarancja Jakości】{core_features[4] if len(core_features) > 4 else 'Materiały wysokiej jakości zapewniają długą żywotność'}",
            ]
            description = f"""Odkryj najwyższy komfort chłodzenia z naszym premium {product_name}!

Idealny na gorące letnie dni, ten wentylator zapewnia mocny przepływ powietrza, zachowując cichą pracę. Niezależnie od tego, czy pracujesz, śpisz czy odpoczywasz, tworzy idealne komfortowe środowisko dla Ciebie.

Kluczowe Cechy:
• {core_features[0] if len(core_features) > 0 else 'Mocny przepływ powietrza'}
• {core_features[1] if len(core_features) > 1 else 'Ultra cicha praca'}
• {core_features[2] if len(core_features) > 2 else 'Energooszczędny design'}
• {core_features[3] if len(core_features) > 3 else 'Przenośny i lekki'}
• {core_features[4] if len(core_features) > 4 else 'Wysokiej jakości wykonanie'}

Nie pozwól, aby upał Cię spowolnił. Kup swój {product_name} już dziś i pozostań chłodny przez całe lato!

Cena: €{price:.2f}"""

        elif language == "瑞典语":
            title = f"{product_name} - Kraftfull Fläkt med Tyst Drift, Energieffektiv, Perfekt för Hem och Kontor"
            bullets = [
                f"【Kraftfull Kylning】{core_features[0] if len(core_features) > 0 else 'Kraftfullt luftflöde för omedelbar kylning'}",
                f"【Ultra Tyst】{core_features[1] if len(core_features) > 1 else 'Bullerreduktionsteknik för en lugn miljö'}",
                f"【Energieffektiv】{core_features[2] if len(core_features) > 2 else 'Låg energiförbrukning sänker din elräkning'}",
                f"【Bärbar Design】{core_features[3] if len(core_features) > 3 else 'Lätt och enkel att flytta överallt'}",
                f"【Kvalitetsgaranti】{core_features[4] if len(core_features) > 4 else 'Högkvalitativa material säkerställer lång livslängd'}",
            ]
            description = f"""Upplev ultimat kylkomfort med vår premium {product_name}!

Perfekt för varma sommardagar levererar denna fläkt ett kraftfullt luftflöde samtidigt som den är knäpptyst. Oavsett om du arbetar, sover eller kopplar av skapar den den perfekta bekväma miljön för dig.

Viktiga Egenskaper:
• {core_features[0] if len(core_features) > 0 else 'Kraftfullt luftflöde'}
• {core_features[1] if len(core_features) > 1 else 'Ultra tyst drift'}
• {core_features[2] if len(core_features) > 2 else 'Energieffektiv design'}
• {core_features[3] if len(core_features) > 3 else 'Bärbar och lätt'}
• {core_features[4] if len(core_features) > 4 else 'Högkvalitativ konstruktion'}

Låt inte värmen sakta ner dig. Skaffa din {product_name} idag och håll dig sval hela sommaren!

Pris: €{price:.2f}"""


                           
        else:
            # 未实现的语言：明确标记，而不是用英文冒充
            title = f"[{language}] 暂未提供地道文案，请选择英语/德语/法语/意大利语/西班牙语/荷兰语/波兰语/瑞典语"
            bullets = [
                f"[{language}] 该语言模板尚未实现",
                "请在 marketing_agent.py 中补充对应语言的 elif 分支",
            ]
            description = (
                f"[{language}] 当前版本尚未提供 {language} 的正式文案模板。\n"
                f"产品：{product_name}\n售价：€{price:.2f}\n"
                f"卖点：{'; '.join(core_features) if core_features else '（无）'}"
            )
        return {
            "language": language,
            "title": title,
            "bullets": bullets,
            "description": description
        }
    
    def process(self, input_data: Dict) -> Dict:
        """实现基类的process方法"""
        return self.generate(
            product_name=input_data.get('product_name', '产品'),
            product_category=input_data.get('product_category', '风扇类'),
            price=input_data.get('price', 29.99),
            core_features=input_data.get('core_features', []),
            target_platform=input_data.get('target_platform', '亚马逊'),
            languages=input_data.get('languages', ['英语'])
        )
