"""
多语种营销智能体
一键生成多语言、多平台营销文案

作者：凉贸通团队
版本：v1.1
日期：2026年6月
"""

from .base_agent import BaseAgent
from typing import Dict, List


class MarketingAgent(BaseAgent):
    """
    多语种营销智能体
    负责文案生成、多语言翻译、关键词优化
    """

    # ==================== 8 语言文案模板 ====================
    LANG_TEMPLATES = {
        "英语": {
            "title": "{name} - Powerful Cooling Fan with Quiet Operation, Energy Efficient, Perfect for Home and Office",
            "bullets": [
                "【Powerful Cooling】{f0}",
                "【Ultra Quiet】{f1}",
                "【Energy Saving】{f2}",
                "【Portable Design】{f3}",
                "【Quality Guarantee】{f4}",
            ],
            "desc_header": "Experience ultimate cooling comfort with our premium {name}!",
            "desc_body": (
                "Perfect for hot summer days, this cooling fan delivers powerful airflow "
                "while maintaining whisper-quiet operation. Whether you're working, sleeping, "
                "or relaxing, it creates the perfect comfortable environment for you."
            ),
            "features_label": "Key Features:",
            "cta": "Don't let the heat slow you down. Get your {name} today and stay cool all summer long!",
            "price_label": "Price",
        },
        "德语": {
            "title": "{name} - Leistungsstarker Ventilator mit leisem Betrieb, energieeffizient, perfekt für Zuhause und Büro",
            "bullets": [
                "【Starke Kühlung】{f0}",
                "【Ultra-leise】{f1}",
                "【Energiesparend】{f2}",
                "【Tragbares Design】{f3}",
                "【Qualitätsgarantie】{f4}",
            ],
            "desc_header": "Erleben Sie ultimativen Kühlkomfort mit unserem Premium-{name}!",
            "desc_body": (
                "Perfekt für heiße Sommertage liefert dieser Ventilator starken Luftstrom "
                "bei flüsterleisem Betrieb. Egal ob Sie arbeiten, schlafen oder entspannen - "
                "er schafft die perfekte komfortable Umgebung für Sie."
            ),
            "features_label": "Hauptmerkmale:",
            "cta": "Lassen Sie sich von der Hitze nicht ausbremsen. Holen Sie sich noch heute Ihren {name} und bleiben Sie den ganzen Sommer über kühl!",
            "price_label": "Preis",
        },
        "法语": {
            "title": "{name} - Ventilateur Puissant avec Fonctionnement Silencieux, Économe en Énergie, Parfait pour la Maison et le Bureau",
            "bullets": [
                "【Refroidissement Puissant】{f0}",
                "【Ultra Silencieux】{f1}",
                "【Économe en Énergie】{f2}",
                "【Design Portable】{f3}",
                "【Garantie Qualité】{f4}",
            ],
            "desc_header": "Découvrez le confort de refroidissement ultime avec notre {name} premium !",
            "desc_body": (
                "Parfait pour les journées d'été chaudes, ce ventilateur délivre un flux d'air "
                "puissant tout en fonctionnant en silence. Que vous travailliez, dormiez ou vous "
                "détendiez, il crée l'environnement confortable parfait pour vous."
            ),
            "features_label": "Caractéristiques Clés :",
            "cta": "Ne laissez pas la chaleur vous ralentir. Procurez-vous votre {name} dès aujourd'hui et restez au frais tout l'été !",
            "price_label": "Prix",
        },
        "意大利语": {
            "title": "{name} - Ventilatore Potente con Funzionamento Silenzioso, Energeticamente Efficiente, Perfetto per Casa e Ufficio",
            "bullets": [
                "【Raffreddamento Potente】{f0}",
                "【Ultra Silenzioso】{f1}",
                "【Risparmio Energetico】{f2}",
                "【Design Portatile】{f3}",
                "【Garanzia di Qualità】{f4}",
            ],
            "desc_header": "Scopri il massimo comfort con il nostro {name} premium!",
            "desc_body": (
                "Perfetto per le calde giornate estive, questo ventilatore offre un flusso d'aria "
                "potente mantenendo un funzionamento silenzioso. Che tu stia lavorando, dormendo "
                "o rilassandoti, crea l'ambiente confortevole ideale per te."
            ),
            "features_label": "Caratteristiche Principali:",
            "cta": "Non lasciare che il caldo ti rallenti. Acquista oggi il tuo {name} e rimani fresco tutta l'estate!",
            "price_label": "Prezzo",
        },
        "西班牙语": {
            "title": "{name} - Ventilador Potente con Funcionamiento Silencioso, Eficiente Energéticamente, Perfecto para Hogar y Oficina",
            "bullets": [
                "【Enfriamiento Potente】{f0}",
                "【Ultra Silencioso】{f1}",
                "【Ahorro de Energía】{f2}",
                "【Diseño Portátil】{f3}",
                "【Garantía de Calidad】{f4}",
            ],
            "desc_header": "¡Experimenta el máximo confort de enfriamiento con nuestro {name} premium!",
            "desc_body": (
                "Perfecto para los calurosos días de verano, este ventilador ofrece un potente "
                "flujo de aire manteniendo un funcionamiento ultrasilencioso. Ya sea que estés "
                "trabajando, durmiendo o relajándote, crea el ambiente perfecto para ti."
            ),
            "features_label": "Características Principales:",
            "cta": "¡No dejes que el calor te detenga. Consigue tu {name} hoy y mantente fresco todo el verano!",
            "price_label": "Precio",
        },
        "荷兰语": {
            "title": "{name} - Krachtige Ventilator met Stille Werking, Energiezuinig, Perfect voor Thuis en Kantoor",
            "bullets": [
                "【Krachtige Koeling】{f0}",
                "【Ultra Stil】{f1}",
                "【Energiebesparend】{f2}",
                "【Draagbaar Ontwerp】{f3}",
                "【Kwaliteitsgarantie】{f4}",
            ],
            "desc_header": "Ervaar ultiem koelcomfort met onze premium {name}!",
            "desc_body": (
                "Perfect voor hete zomerdagen levert deze ventilator een krachtige luchtstroom "
                "terwijl hij fluisterstil werkt. Of u nu werkt, slaapt of ontspant, hij creëert "
                "de perfecte comfortabele omgeving voor u."
            ),
            "features_label": "Belangrijkste Kenmerken:",
            "cta": "Laat de hitte u niet vertragen. Haal vandaag nog uw {name} en blijf de hele zomer koel!",
            "price_label": "Prijs",
        },
        "波兰语": {
            "title": "{name} - Mocny Wentylator z Cichą Pracą, Energooszczędny, Idealny do Domu i Biura",
            "bullets": [
                "【Mocne Chłodzenie】{f0}",
                "【Ultra Cichy】{f1}",
                "【Oszczędność Energii】{f2}",
                "【Przenośny Design】{f3}",
                "【Gwarancja Jakości】{f4}",
            ],
            "desc_header": "Odkryj najwyższy komfort chłodzenia z naszym premium {name}!",
            "desc_body": (
                "Idealny na gorące letnie dni, ten wentylator zapewnia mocny przepływ powietrza, "
                "zachowując cichą pracę. Niezależnie od tego, czy pracujesz, śpisz czy odpoczywasz, "
                "tworzy idealne komfortowe środowisko dla Ciebie."
            ),
            "features_label": "Kluczowe Cechy:",
            "cta": "Nie pozwól, aby upał Cię spowolnił. Kup swój {name} już dziś i pozostań chłodny przez całe lato!",
            "price_label": "Cena",
        },
        "瑞典语": {
            "title": "{name} - Kraftfull Fläkt med Tyst Drift, Energieffektiv, Perfekt för Hem och Kontor",
            "bullets": [
                "【Kraftfull Kylning】{f0}",
                "【Ultra Tyst】{f1}",
                "【Energieffektiv】{f2}",
                "【Bärbar Design】{f3}",
                "【Kvalitetsgaranti】{f4}",
            ],
            "desc_header": "Upplev ultimat kylkomfort med vår premium {name}!",
            "desc_body": (
                "Perfekt för varma sommardagar levererar denna fläkt ett kraftfullt luftflöde "
                "samtidigt som den är knäpptyst. Oavsett om du arbetar, sover eller kopplar av "
                "skapar den den perfekta bekväma miljön för dig."
            ),
            "features_label": "Viktiga Egenskaper:",
            "cta": "Låt inte värmen sakta ner dig. Skaffa din {name} idag och håll dig sval hela sommaren!",
            "price_label": "Pris",
        },
    }

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
        """初始化平台文案模板"""
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
        """生成多语言营销文案"""
        keywords = self._get_keywords(product_category, languages)

        copies = []
        for lang in languages:
            copy = self._generate_copy(product_name, price, core_features, target_platform, lang)
            copies.append(copy)

        return {
            "keywords": keywords,
            "copies": copies,
            "product_name": product_name,
            "target_platform": target_platform,
        }

    def _get_keywords(self, category: str, languages: List[str]) -> List[Dict]:
        """获取关键词"""
        result = []

        if category not in self.keyword_db:
            category = "风扇类"

        for lang in languages:
            if lang in self.keyword_db[category]:
                kws = self.keyword_db[category][lang]
                result.append({
                    "语言": lang,
                    "核心关键词": ", ".join(kws[:3]),
                    "长尾关键词": ", ".join(kws[3:]),
                })

        return result

    def _generate_copy(self, product_name: str, price: float, core_features: List[str],
                       platform: str, language: str) -> Dict:
        """生成单语言文案（基于模板，支持 8 种语言）"""
        tpl = self.LANG_TEMPLATES.get(language)

        if not tpl:
            return {
                "language": language,
                "title": f"[{language}] 暂不支持该语言",
                "bullets": [f"[{language}] 该语言模板尚未实现"],
                "description": (
                    f"[{language}] 当前版本尚未提供 {language} 的正式文案模板。\n"
                    f"产品：{product_name}\n售价：€{price:.2f}\n"
                    f"卖点：{'; '.join(core_features) if core_features else '（无）'}"
                ),
            }

        defaults = [
            "Powerful cooling performance",
            "Quiet operation",
            "Energy efficient design",
            "Portable and lightweight",
            "High quality construction",
        ]
        f = list(core_features[:5]) + [""] * 5
        f = [f[i] if f[i] else defaults[i] for i in range(5)]

        fmt = {
            "name": product_name,
            "price": f"{price:.2f}",
            "f0": f[0], "f1": f[1], "f2": f[2], "f3": f[3], "f4": f[4],
        }

        title = tpl["title"].format(**fmt)
        bullets = [b.format(**fmt) for b in tpl["bullets"]]

        description = (
            tpl["desc_header"].format(**fmt)
            + "\n\n"
            + tpl["desc_body"]
            + "\n\n"
            + tpl["features_label"]
            + "\n"
            + "\n".join(f"• {x}" for x in f)
            + "\n\n"
            + tpl["cta"].format(**fmt)
            + f"\n\n{tpl['price_label']}: €{fmt['price']}"
        )

        return {
            "language": language,
            "title": title,
            "bullets": bullets,
            "description": description,
        }

    def process(self, input_data: Dict) -> Dict:
        """实现基类的 process 方法"""
        return self.generate(
            product_name=input_data.get('product_name', '产品'),
            product_category=input_data.get('product_category', '风扇类'),
            price=input_data.get('price', 29.99),
            core_features=input_data.get('core_features', []),
            target_platform=input_data.get('target_platform', '亚马逊'),
            languages=input_data.get('languages', ['英语'])
        )
