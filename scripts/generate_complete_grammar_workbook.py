import hashlib
import random
import re
from pathlib import Path

import pdfplumber
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


OUTLINE_PDF = "English_Grammar_Knowledge_Outline_CN.pdf"
OUT_DIR = Path("英语语法题库PDF")
QUESTIONS_PDF = OUT_DIR / "完整语法题库_第001-286知识点_worksheet.pdf"
ANSWERS_PDF = OUT_DIR / "完整语法题库_第001-286知识点_答案.pdf"

FONT = "Songti"
pdfmetrics.registerFont(TTFont(FONT, "/System/Library/Fonts/Supplemental/Songti.ttc", subfontIndex=0))

PAGE_W, PAGE_H = A4
MARGIN_X = 42
TOP = PAGE_H - 40
BOTTOM = 38
LETTERS = ["A", "B", "C", "D"]
BLANK_OPTION = "leave blank"


FIRST_FIVE = {
    "普通名词与专有名词识别": [
        ("Which word is a proper noun? 下面哪一个是专有名词？", ["city", "teacher", "London", "river"], "C"),
        ("In the sentence 'Emma reads a book.', which word is a proper noun? 句中哪个词是专有名词？", ["Emma", "reads", "book", "a"], "A"),
        ("Which word is a common noun? 下面哪一个是普通名词？", ["China", "Monday", "school", "Tom"], "C"),
        ("Choose the proper noun. 选择专有名词。", ["mountain", "Mr. Smith", "restaurant", "student"], "B"),
        ("In 'We visited the museum in Paris.', which word is a proper noun? 哪个词是专有名词？", ["visited", "museum", "Paris", "the"], "C"),
        ("Which pair has one common noun and one proper noun? 哪组包含一个普通名词和一个专有名词？", ["apple / banana", "Sarah / Alice", "country / Japan", "quick / slowly"], "C"),
        ("Which sentence uses a proper noun correctly? 哪句正确使用了专有名词？", ["My friend is a doctor.", "We live near the river.", "David plays tennis.", "A cat is sleeping."], "C"),
        ("Which word usually needs a capital letter because it is a proper noun? 哪个词通常因是专有名词而首字母大写？", ["january", "desk", "woman", "flower"], "A"),
        ("In 'The Nile is a long river.', which named place word should be treated as a proper noun? 句中哪个地名词应视为专有名词？", ["Nile", "long", "river", "The"], "A"),
        ("Which option contains only common nouns? 哪个选项全是普通名词？", ["Beijing, city", "doctor, classroom", "Anna, girl", "Sunday, day"], "B"),
    ],
    "可数名词、不可数名词识别": [
        ("Which noun is countable? 哪个名词是可数名词？", ["water", "rice", "apple", "music"], "C"),
        ("Which noun is uncountable? 哪个名词是不可数名词？", ["chair", "idea", "furniture", "student"], "C"),
        ("Choose the correct phrase. 选择正确短语。", ["many water", "much water", "a water", "two water"], "B"),
        ("Which phrase is correct? 哪个短语正确？", ["an advice", "two advices", "some advice", "many advice"], "C"),
        ("Which noun can normally take a/an? 哪个名词通常可以直接加 a/an？", ["information", "bread", "orange", "homework"], "C"),
        ("Complete: There are three ___. 补全句子。", ["cup", "cups", "water", "rice"], "B"),
        ("Complete: I need some ___. 补全句子。", ["informations", "information", "an information", "many information"], "B"),
        ("Which set contains only uncountable nouns? 哪组全是不可数名词？", ["milk, sugar, air", "book, pen, desk", "child, dog, song", "city, road, car"], "A"),
        ("Which question is correct? 哪个问句正确？", ["How many money do you have?", "How much money do you have?", "How many milk do you need?", "How much apples are there?"], "B"),
        ("Which noun is countable in ordinary use? 哪个名词在通常用法中可数？", ["news", "homework", "bottle", "traffic"], "C"),
    ],
    "集合名词（family / class 等）用法": [
        ("Choose the best sentence when the group acts as one. 当群体作为整体行动时，选最佳句。", ["The team are winning the cup as one unit.", "The team is winning the cup.", "The team be winning.", "The team have a name is Tigers."], "B"),
        ("Complete: My family ___ small. 补全句子。", ["is", "are", "be", "were being"], "A"),
        ("Which word is a collective noun? 哪个词是集合名词？", ["class", "desk", "water", "honesty"], "A"),
        ("Complete: The class ___ listening to the teacher. 补全句子。", ["is", "are", "am", "be"], "A"),
        ("Which sentence emphasizes the members of a family? 哪句强调家庭成员各自的行动？", ["My family is a happy group.", "My family are all wearing different coats.", "My family has a small house.", "My family is large."], "B"),
        ("Which option is NOT usually a collective noun? 哪个通常不是集合名词？", ["team", "committee", "water", "audience"], "C"),
        ("Complete: The committee ___ made one decision. 补全句子。", ["has", "have are", "be", "were has"], "A"),
        ("Which sentence treats 'audience' as one group? 哪句把 audience 当作一个整体？", ["The audience is quiet.", "The audience are taking their seats one by one.", "The audience were looking for their phones.", "The audience have different opinions."], "A"),
        ("Complete: Our class ___ twenty students. 补全句子。", ["has", "have are", "be", "am"], "A"),
        ("Which sentence is most natural for one group name? 哪句最自然地表示一个群体名称？", ["The family are called the Lees.", "The family is called the Lees.", "The family be called the Lees.", "The family have called the Lees."], "B"),
    ],
    "物质名词、抽象名词识别": [
        ("Which is a material noun? 哪个是物质名词？", ["gold", "kindness", "idea", "beauty"], "A"),
        ("Which is an abstract noun? 哪个是抽象名词？", ["wood", "milk", "freedom", "cotton"], "C"),
        ("In 'The ring is made of silver.', what type of noun is 'silver'? silver 属于哪类名词？", ["proper noun", "material noun", "collective noun", "verb"], "B"),
        ("The word 'honesty' names an idea or quality. What type of noun is it?", ["abstract noun", "material noun", "proper noun", "countable place noun"], "A"),
        ("Which pair contains one material noun and one abstract noun? 哪组包含一个物质名词和一个抽象名词？", ["iron / courage", "teacher / student", "London / China", "family / class"], "A"),
        ("Which word names a feeling or quality, not a physical material? 哪个词表示情感或品质，而不是物质？", ["plastic", "anger", "water", "wool"], "B"),
        ("Which word names a substance? 哪个词表示一种物质？", ["happiness", "sand", "truth", "peace"], "B"),
        ("Choose the abstract noun. 选择抽象名词。", ["glass", "patience", "paper", "steel"], "B"),
        ("Choose the material noun. 选择物质名词。", ["love", "oil", "wisdom", "success"], "B"),
        ("Which sentence contains an abstract noun? 哪句含有抽象名词？", ["The table is made of wood.", "She showed great courage.", "The bottle is full of water.", "They bought cotton shirts."], "B"),
    ],
    "一般情况直接加 -s": [
        ("What is the plural of 'book'? book 的复数是什么？", ["bookes", "books", "bookies", "book"], "B"),
        ("Choose the correct plural. 选择正确复数。", ["pens", "penes", "penies", "pen"], "A"),
        ("Complete: two ___. 补全短语。", ["cats", "cat", "cates", "caties"], "A"),
        ("What is the plural of 'desk'? desk 的复数是什么？", ["desk", "deskes", "desks", "deskies"], "C"),
        ("Choose the correct sentence. 选择正确句子。", ["I have three notebook.", "I have three notebooks.", "I have three notebookes.", "I have three notebookies."], "B"),
        ("What is the plural of 'girl'? girl 的复数是什么？", ["girls", "girles", "girlies", "girl"], "A"),
        ("Complete: four ___. 补全短语。", ["car", "cares", "cars", "caries"], "C"),
        ("Which noun forms its plural by only adding -s? 哪个名词复数只需加 -s？", ["box", "baby", "bus", "map"], "D"),
        ("What is the plural of 'teacher'? teacher 的复数是什么？", ["teacher", "teacheres", "teachers", "teacheries"], "C"),
        ("Choose the correct phrase. 选择正确短语。", ["five dogs", "five dog", "five doges", "five dogies"], "A"),
    ],
}


CN_TO_EN = [
    ("普通名词与专有名词识别", "recognizing common nouns and proper nouns"),
    ("可数名词、不可数名词识别", "recognizing countable and uncountable nouns"),
    ("集合名词", "collective nouns"),
    ("物质名词、抽象名词识别", "recognizing material nouns and abstract nouns"),
    ("一般情况直接加 -s", "forming regular plurals by adding -s"),
    ("s / x / ch / sh 结尾加 -es", "adding -es after nouns ending in s, x, ch, or sh"),
    ("辅音字母 + y 结尾，变 y 为 i 加 -es", "changing consonant + y to -ies"),
    ("元音字母 + y 结尾，直接加 -s", "adding -s after vowel + y"),
    ("f / fe 结尾，变 f / fe 为 v 加 -es", "changing f or fe to -ves"),
    ("f 结尾直接加 -s 的特殊名词", "special f-ending nouns that take only -s"),
    ("o 结尾有生命名词加 -es", "adding -es to some animate o-ending nouns"),
    ("o 结尾无生命名词直接加 -s", "adding -s to many inanimate o-ending nouns"),
    ("不规则复数", "irregular plural nouns"),
    ("单复数同形", "singular and plural forms that are the same"),
    ("只有复数形式的名词", "nouns used only in plural form"),
    ("复合名词变复数", "forming plurals of compound nouns"),
    ("所有格", "noun possessives"),
    ("人称代词主格", "subject forms of personal pronouns"),
    ("人称代词宾格", "object forms of personal pronouns"),
    ("主格、宾格混合", "subject and object pronoun contrast"),
    ("形容词性物主代词", "possessive adjectives"),
    ("名词性物主代词", "possessive pronouns"),
    ("反身代词", "reflexive pronouns"),
    ("指示代词", "demonstrative pronouns"),
    ("不定代词", "indefinite pronouns"),
    ("疑问代词", "interrogative pronouns"),
    ("关系代词", "relative pronouns"),
    ("连接代词", "conjunctive pronouns in noun clauses"),
    ("不定冠词 a", "the indefinite article a"),
    ("不定冠词 an", "the indefinite article an"),
    ("定冠词 the", "the definite article the"),
    ("零冠词", "zero article usage"),
    ("冠词固定搭配", "fixed expressions with or without articles"),
    ("基数词", "cardinal numbers"),
    ("序数词", "ordinal numbers"),
    ("分数表达", "fraction expressions"),
    ("小数表达", "decimal expressions"),
    ("百分数", "percent expressions"),
    ("时间表达", "time expressions"),
    ("日期表达", "date expressions"),
    ("年代表达", "decade expressions"),
    ("形容词作定语", "adjectives used before nouns as modifiers"),
    ("形容词作表语", "adjectives used after linking verbs as complements"),
    ("形容词作宾语补足语", "adjectives used as object complements"),
    ("多个形容词并列排序", "the order of multiple adjectives"),
    ("-ing 形容词与 -ed 形容词", "-ing and -ed adjectives"),
    ("形容词变副词", "changing adjectives into adverbs"),
    ("不规则副词", "irregular adverbs"),
    ("副词位置", "adverb position"),
    ("enough 修饰", "the position of enough"),
    ("比较级", "comparatives"),
    ("最高级", "superlatives"),
    ("时间介词", "prepositions of time"),
    ("地点辨析", "prepositions of place"),
    ("方位介词", "prepositions of position"),
    ("方式手段介词", "prepositions of means and manner"),
    ("固定介词", "fixed preposition patterns"),
    ("系动词", "linking verbs"),
    ("实义动词", "main verbs"),
    ("助动词", "auxiliary verbs"),
    ("情态动词 + have done", "modal + have + past participle for past speculation or unreal past meaning"),
    ("情态动词", "modal verbs"),
    ("一般现在时", "the simple present tense"),
    ("现在进行时", "the present continuous tense"),
    ("一般过去时", "the simple past tense"),
    ("过去进行时", "the past continuous tense"),
    ("一般将来时", "the simple future tense"),
    ("现在完成时", "the present perfect tense"),
    ("过去完成时", "the past perfect tense"),
    ("将来进行时", "the future continuous tense"),
    ("将来完成时", "the future perfect tense"),
    ("被动", "the passive voice"),
    ("不定式", "infinitives"),
    ("动名词", "gerunds"),
    ("现在分词", "present participles"),
    ("过去分词", "past participles"),
    ("非谓语", "non-finite verbs"),
    ("句子成分", "sentence elements"),
    ("识别主语", "identifying the subject"),
    ("识别谓语", "identifying the predicate"),
    ("识别宾语", "identifying the object"),
    ("识别表语", "identifying the predicative complement"),
    ("识别定语", "identifying the attributive modifier"),
    ("识别状语", "identifying adverbials"),
    ("识别宾语补足语", "identifying object complements"),
    ("识别同位语", "identifying appositives"),
    ("简单句基本句型", "basic simple sentence patterns"),
    ("陈述句", "declarative sentences"),
    ("疑问句", "questions"),
    ("特殊疑问句", "wh-questions"),
    ("选择疑问句", "alternative questions"),
    ("反意疑问句", "tag questions"),
    ("祈使句", "imperatives"),
    ("感叹句", "exclamatory sentences"),
    ("There be", "there be sentences"),
    ("并列句", "compound sentences"),
    ("定语从句", "relative clauses"),
    ("宾语从句", "object clauses"),
    ("主语从句", "subject clauses"),
    ("表语从句", "predicative clauses"),
    ("同位语从句", "appositive clauses"),
    ("状语从句", "adverbial clauses"),
    ("倒装", "inversion"),
    ("强调句型", "cleft sentences"),
    ("省略", "ellipsis"),
    ("形式宾语", "formal object it"),
    ("形式主语", "formal subject it"),
    ("虚拟语气", "the subjunctive mood"),
]


def english_gloss(topic):
    for cn, en in CN_TO_EN:
        if cn in topic:
            return en
    if "辨析" in topic and "/" in topic:
        terms = re.findall(r"[A-Za-z]+(?:\s*/\s*[A-Za-z]+)+", topic)
        if terms:
            return "distinguishing " + terms[0].replace("/", " and ")
    if "/" in topic or "+" in topic or "..." in topic:
        return "using the pattern " + re.sub(r"[：；，。、“”（）]", " ", topic)
    return "recognizing and using this English grammar rule"


def chinese_intro(topic):
    return f"本页测试语法点：{topic}。请根据规则、结构和语境选择唯一正确答案。"


def english_intro(topic):
    return f"This worksheet tests {english_gloss(topic)}. Choose the only correct answer according to form, meaning, and context."


def answer_explanation(topic):
    if "普通名词与专有名词" in topic:
        return "解析：普通名词表示一类人或事物；专有名词表示特定名称，通常首字母大写。"
    if "可数名词、不可数" in topic:
        return "解析：可数名词能直接计数并有复数形式；不可数名词通常不直接加 a/an 或复数 -s。"
    if "集合名词" in topic:
        return "解析：集合名词表示一个群体；强调整体时多按单数，强调成员时看具体语境。"
    if "物质名词、抽象名词" in topic:
        return "解析：物质名词表示材料或物质；抽象名词表示品质、情感、状态或概念。"
    if "复数" in topic or "加 -s" in topic or "加 -es" in topic or "变 y" in topic or "变 f" in topic:
        return "解析：先看名词词尾和是否规则变化，再选择对应复数形式；特殊词需按固定变化记忆。"
    if "所有格" in topic:
        return "解析：根据名词单复数和是否共同拥有判断 's、单独撇号、of 结构或双重所有格。"
    if "情态动词 + have done" in topic:
        return "解析：情态动词 + have done 用于对过去的推测、遗憾或虚拟，后面必须接过去分词。"
    if "虚拟语气" in topic:
        return "解析：虚拟语气表达非真实、愿望、建议或假设，关键是时态后移和固定动词后的原形结构。"
    if "倒装" in topic:
        return "解析：倒装题注意否定词、only 状语、so/neither/nor 等置于句首时的助动词提前。"
    if "强调句型" in topic:
        return "解析：强调句基本结构是 It is/was + 被强调部分 + that/who + 其余部分。"
    if "省略" in topic:
        return "解析：省略题要确认省略后主语和 be 动词能从上下文恢复，句意仍清楚。"
    if "形式主语" in topic:
        return "解析：it 作形式主语时，真正主语通常是不定式、动名词或 that 从句。"
    if "形式宾语" in topic:
        return "解析：it 作形式宾语时，真正宾语常放在后面，如 to do 或 that 从句。"
    if "从句" in topic or any(x in topic for x in ["who 指代", "whom 指代", "whose 作", "which 指代", "that 用于限定", "只用 that", "只用 which", "as 引导", "when 引导", "where 引导", "why 引导", "if / whether", "because", "although", "unless", "so ... that", "so that"]):
        return "解析：从句题先判断从句类型和缺少的成分，再选择关系词、连接词或从属连词。"
    if "比较级" in topic or any(x in topic for x in ["加 -er", "加 -r", "more", "than 引导", "越来越", "越……越"]):
        return "解析：比较级用于两者比较，注意 -er、more、不规则变化、than 以及固定比较结构。"
    if "最高级" in topic or any(x in topic for x in ["加 -est", "加 -st", "most", "best", "worst"]):
        return "解析：最高级用于三者及以上范围，常与 the、in/of 范围短语和 -est/most 搭配。"
    if "代词" in topic or any(x in topic for x in ["this", "that", "these", "those", "some", "any", "few", "little", "both", "either", "neither", "each", "every", "one / ones", "other"]):
        return "解析：代词题要看所指对象、单复数、主宾格、所属关系以及句中位置。"
    if "冠词" in topic or "the" in topic or "a / an" in topic or "零冠词" in topic:
        return "解析：冠词题主要判断泛指或特指、音素开头、固定搭配，以及是否需要零冠词。"
    if any(x in topic for x in ["基数词", "序数词", "分数", "小数", "百分", "整点", "半点", "日期", "年代", "past 表达", "to 表达", "hundred", "thousand", "million"]):
        return "解析：数词和时间题重在固定表达形式；注意拼写、序数词变化、percent 不加复数，以及时间读法。"
    if "形容词" in topic or "副词" in topic or "-ly" in topic or "enough" in topic:
        return "解析：形容词多修饰名词或作表语；副词多修饰动词、形容词或全句，注意词形和位置。"
    if "比较级" in topic:
        return "解析：比较级用于两者比较，注意 -er、more、不规则变化、than 以及固定比较结构。"
    if "最高级" in topic:
        return "解析：最高级用于三者及以上范围，常与 the、in/of 范围短语和 -est/most 搭配。"
    if "介词" in topic or any(x in topic for x in ["between / among", "through / across", "since / for", "before / after", "during 用法"]):
        return "解析：介词要结合时间、地点、方向、工具、方式或固定搭配来判断。"
    if "被动" in topic:
        return "解析：被动语态核心是 be + 过去分词；be 的形式随时态、主语和情态动词变化。"
    if any(x in topic for x in ["一般现在", "现在进行", "一般过去", "过去进行", "一般将来", "现在完成", "过去完成", "将来进行", "将来完成"]):
        return "解析：时态题先看时间线索和句意，再确定助动词、be 动词或动词形式。"
    if "情态动词 + have done" in topic:
        return "解析：情态动词 + have done 用于对过去的推测、遗憾或虚拟，后面必须接过去分词。"
    if "情态动词" in topic or any(x in topic for x in ["can / could", "may / might", "must", "should", "need 作"]):
        return "解析：情态动词后接动词原形；不同情态动词表达能力、许可、推测、建议或必要性。"
    if any(x in topic for x in ["不定式", "动名词", "现在分词", "过去分词", "非谓语", "to do", "doing", "done"]):
        return "解析：非谓语题要看前面动词或介词要求，以及该结构在句中作宾语、定语、状语等功能。"
    if "从句" in topic or any(x in topic for x in ["who", "whom", "whose", "which", "that", "when", "where", "why", "because", "although", "unless", "so that"]):
        return "解析：从句题先判断从句类型和缺少的成分，再选择关系词、连接词或从属连词。"
    if any(x in topic for x in ["识别主语", "识别谓语", "识别宾语", "识别表语", "识别定语", "识别状语", "识别宾语补足语", "识别同位语"]):
        return "解析：句子成分题要根据词组在句中的功能判断，而不是只看词性。"
    if "S + V" in topic:
        return "解析：五大基本句型要看动词性质及其后是否接表语、宾语、双宾语或宾补。"
    if "疑问句" in topic or "反意疑问句" in topic:
        return "解析：疑问句重点看助动词、be 动词或情态动词的位置，以及简答和反意疑问的前后呼应。"
    if "祈使句" in topic:
        return "解析：祈使句通常以动词原形开头；否定形式常用 Don't + 动词原形。"
    if "感叹句" in topic:
        return "解析：What 强调名词短语，How 强调形容词或副词，注意可数名词单数前的 a/an。"
    if "There be" in topic:
        return "解析：There be 表示某处有某物，be 的形式通常遵循就近原则，不能与 have 混用。"
    if "并列句" in topic or any(x in topic for x in ["and 表", "but 表", "so 表", "or 表"]):
        return "解析：并列连词要根据前后分句关系选择：顺承、转折、结果、选择或否则。"
    if "倒装" in topic:
        return "解析：倒装题注意否定词、only 状语、so/neither/nor 等置于句首时的助动词提前。"
    if "强调句型" in topic:
        return "解析：强调句基本结构是 It is/was + 被强调部分 + that/who + 其余部分。"
    if "省略" in topic:
        return "解析：省略题要确认省略后主语和 be 动词能从上下文恢复，句意仍清楚。"
    if "形式主语" in topic:
        return "解析：it 作形式主语时，真正主语通常是不定式、动名词或 that 从句。"
    if "形式宾语" in topic:
        return "解析：it 作形式宾语时，真正宾语常放在后面，如 to do 或 that 从句。"
    if "虚拟语气" in topic:
        return "解析：虚拟语气表达非真实、愿望、建议或假设，关键是时态后移和固定动词后的原形结构。"
    return "解析：本页题目围绕该语法点的形式、意义和语境展开，做题时先找结构线索，再排除不合规则的选项。"


def extract_topics():
    topics = []
    part = ""
    section = ""
    sub = ""
    skip = {
        "语法知识点大纲",
        "英语语法知识体系 · 结构化目录版",
        "STRUCTURED OUTLINE · 结构化大纲",
        "第一部分",
    }
    with pdfplumber.open(OUTLINE_PDF) as pdf:
        lines = []
        for page in pdf.pages:
            lines += (page.extract_text() or "").splitlines()
    for raw in lines:
        line = raw.strip()
        if (
            not line
            or line in skip
            or line.isdigit()
            or line.startswith(("英语语法知识体系", "STRUCTURED OUTLINE", "说明：", "Grammar Outline Index"))
        ):
            continue
        if line.startswith(("一、", "二、", "三、")):
            part = line
            section = ""
            sub = ""
            continue
        if line.startswith("·"):
            topic = re.sub(r"^\d{3}\s+", "", line[1:].strip())
            topics.append({"cn": topic, "part": part, "section": section, "sub": sub})
            continue
        if re.match(r"^\d+\.\d+\s+", line):
            sub = line
            continue
        if re.match(r"^\d+\s+", line):
            section = line
            sub = ""
            continue
    return topics


def mix_options(correct, wrongs, seed):
    wrongs = list(dict.fromkeys([w for w in wrongs if w != correct]))
    fallback = [
        "incorrect form",
        "wrong sentence structure",
        "wrong word choice",
        "wrong grammar rule",
        "wrong context",
    ]
    fallback_id = 0
    while len(wrongs) < 3:
        candidate = fallback[fallback_id % len(fallback)]
        if fallback_id >= len(fallback):
            candidate = f"{candidate} {fallback_id + 1}"
        fallback_id += 1
        if candidate != correct and candidate not in wrongs:
            wrongs.append(candidate)
    rng = random.Random(seed)
    opts = [correct] + wrongs[:3]
    if len(set(opts)) != 4:
        raise ValueError(f"Options must be unique: {opts}")
    rng.shuffle(opts)
    return opts, LETTERS[opts.index(correct)]


def q(stem, correct, wrongs, seed):
    opts, ans = mix_options(correct, wrongs, seed)
    return stem, opts, ans


def strip_instruction_cn(text):
    replacements = [
        "下面哪一个是专有名词？",
        "句中哪个词是专有名词？",
        "下面哪一个是普通名词？",
        "选择专有名词。",
        "哪个词是专有名词？",
        "哪组包含一个普通名词和一个专有名词？",
        "哪句正确使用了专有名词？",
        "哪个词通常因是专有名词而首字母大写？",
        "句中哪个地名词应视为专有名词？",
        "哪个选项全是普通名词？",
        "哪个名词是可数名词？",
        "哪个名词是不可数名词？",
        "选择正确短语。",
        "哪个短语正确？",
        "哪个名词通常可以直接加 a/an？",
        "补全句子。",
        "哪组全是不可数名词？",
        "哪个问句正确？",
        "哪个名词在通常用法中可数？",
        "哪个词是集合名词？",
        "哪句强调家庭成员各自的行动？",
        "哪个通常不是集合名词？",
        "哪句把 audience 当作一个整体？",
        "哪句最自然地表示一个群体名称？",
        "哪个是物质名词？",
        "哪个是抽象名词？",
        "silver 属于哪类名词？",
        "honesty 属于哪类名词？",
        "哪组包含一个物质名词和一个抽象名词？",
        "哪个词表示情感或品质，而不是物质？",
        "哪个词表示一种物质？",
        "选择抽象名词。",
        "选择物质名词。",
        "哪句含有抽象名词？",
        "选择正确复数。",
        "补全短语。",
        "选择正确句子。",
        "哪个名词复数只需加 -s？",
        "哪个名词通常只有复数形式？",
        "哪个短语自然？",
        "选择主谓一致正确的句子。",
        "哪个词表示一件时常用 a pair of？",
        "选择最佳规则。",
        "补全句子：",
        "选择正确运用本知识点的选项。",
        "哪个选项最适合空格：",
        "句子有误，选择最佳改法：",
        "选择最佳规则说明。",
        "改正画线部分：",
        "根据中文提示选择正确英文。提示：正确运用本页语法点。",
        "在此语境中哪个自然：",
        "哪组形式和句子都正确？",
        "学完本知识点后应选择哪项？",
        "哪个英文说明对应本知识点？",
        "本页主要考什么？",
        "选择最佳学习判断方式。",
        "题型要求是什么？",
        "选择介词。",
        "补全从句。",
        "补全或选择。",
        "选择正确项。",
    ]
    for phrase in replacements:
        text = text.replace(phrase, "")
    text = re.sub(r"\s+([?.!,;:])", r"\1", text)
    text = re.sub(r"：\s*", ": ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def clean_question_instructions(questions):
    return [(strip_instruction_cn(stem), options, answer) for stem, options, answer in questions]


def clean_stem(stem):
    stem = strip_instruction_cn(stem)
    return re.sub(r"\s*(Complete the sentence|Choose the correct option|Choose the correct verb form)\.?$", "", stem).strip()


def is_blank_choice(choice):
    return choice.lower() in {BLANK_OPTION, "no article", "no word needed", "nothing"}


def fill_sentence(stem, choice):
    base = clean_stem(stem)
    if "___" in base:
        if is_blank_choice(choice):
            sentence = base.replace("___", "")
            sentence = re.sub(r"\s+([?.!,;:])", r"\1", sentence)
            return re.sub(r"\s{2,}", " ", sentence).strip()
        return base.replace("___", choice)
    return f"{base} - {choice}"


def mark_sentence(stem, choice):
    base = clean_stem(stem)
    if "___" in base:
        marker = "[leave blank]" if is_blank_choice(choice) else f"[{choice}]"
        return base.replace("___", marker)
    return f"{base} - [{choice}]"


def varied_questions(topic, examples, rule, seed):
    examples = [ex for ex in examples if len(ex) == 3]
    if not examples:
        examples = [("Choose the correct option for this grammar point.", english_gloss(topic), ["an unrelated rule", "an incorrect form", "a wrong sentence pattern"])]

    def ex(i):
        return examples[i % len(examples)]

    e0, e1, e2, e3, e4, e5, e6, e7 = [ex(i) for i in range(8)]
    questions = [
        q(f"Complete the sentence. {clean_stem(e0[0])}", e0[1], e0[2], seed + 1),
        q(
            "Choose the option that correctly uses this grammar point.",
            fill_sentence(e1[0], e1[1]),
            [fill_sentence(e1[0], e1[2][0]), fill_sentence(e1[0], e1[2][1]), fill_sentence(e1[0], e1[2][2])],
            seed + 2,
        ),
        q(f"Which option best fits the blank? {clean_stem(e2[0])}", e2[1], e2[2], seed + 3),
        q(
            f"The bracketed part is wrong. Choose the best correction. {mark_sentence(e3[0], e3[2][0])}",
            e3[1],
            e3[2],
            seed + 4,
        ),
        q("Choose the best rule statement.", rule, ["Use the form only by guessing.", "Ignore the sentence context.", "Choose the longest option every time."], seed + 5),
        q(
            f"Replace the bracketed part. {mark_sentence(e4[0], e4[2][0])}",
            e4[1],
            e4[2],
            seed + 6,
        ),
        q(
            "Choose the option that matches the given meaning.",
            fill_sentence(e5[0], e5[1]),
            [fill_sentence(e5[0], e5[2][0]), fill_sentence(e5[0], e5[2][1]), fill_sentence(e5[0], e5[2][2])],
            seed + 7,
        ),
        q(
            f"In this context, which choice is natural? {clean_stem(e6[0])}",
            e6[1],
            e6[2],
            seed + 8,
        ),
        q(
            "Which pair shows the correct form and sentence?",
            f"{e7[1]} - {fill_sentence(e7[0], e7[1])}",
            [
                f"{e7[2][0]} - {fill_sentence(e7[0], e7[2][0])}",
                f"{e7[2][1]} - {fill_sentence(e7[0], e7[2][1])}",
                f"{e7[2][2]} - {fill_sentence(e7[0], e7[2][2])}",
            ],
            seed + 9,
        ),
        q(
            "After learning this point, which answer should a student choose?",
            fill_sentence(e0[0], e0[1]),
            [fill_sentence(e0[0], e0[2][0]), fill_sentence(e0[0], e0[2][1]), fill_sentence(e0[0], e0[2][2])],
            seed + 10,
        ),
    ]
    return questions


def plural_questions(topic, seed):
    if "s / x / ch / sh" in topic:
        pairs = [("bus", "buses", ["bus", "buss", "busies"]), ("box", "boxes", ["boxs", "boxies", "box"]), ("watch", "watches", ["watchs", "watchies", "watch"]), ("dish", "dishes", ["dishs", "dishies", "dish"])]
        rule = "add -es"
    elif "辅音字母 + y" in topic and "-es" in topic:
        pairs = [("baby", "babies", ["babys", "babyes", "baby"]), ("city", "cities", ["citys", "cityes", "city"]), ("story", "stories", ["storys", "storyes", "story"])]
        rule = "change y to i and add -es"
    elif "元音字母 + y" in topic:
        pairs = [("boy", "boys", ["boies", "boyes", "boy"]), ("key", "keys", ["keies", "keyes", "key"]), ("toy", "toys", ["toies", "toyes", "toy"])]
        rule = "add -s"
    elif "f / fe" in topic:
        pairs = [("leaf", "leaves", ["leafs", "leafes", "leaf"]), ("knife", "knives", ["knifes", "knive", "knife"]), ("wife", "wives", ["wifes", "wifeves", "wife"])]
        rule = "change f/fe to -ves"
    elif "roof" in topic or "belief" in topic:
        pairs = [("roof", "roofs", ["rooves", "roofes", "roof"]), ("belief", "beliefs", ["believes", "beliefes", "belief"]), ("chief", "chiefs", ["chieves", "chiefes", "chief"])]
        rule = "add -s"
    elif "有生命" in topic:
        pairs = [("hero", "heroes", ["heros", "heroies", "hero"]), ("potato", "potatoes", ["potatos", "potatoies", "potato"]), ("tomato", "tomatoes", ["tomatos", "tomatoies", "tomato"])]
        rule = "add -es"
    elif "无生命" in topic:
        pairs = [("photo", "photos", ["photoes", "photoies", "photo"]), ("radio", "radios", ["radioes", "radioies", "radio"]), ("piano", "pianos", ["pianoes", "pianoies", "piano"])]
        rule = "add -s"
    elif "man-men" in topic:
        pairs = [("man", "men", ["mans", "manes", "man"]), ("woman", "women", ["womans", "womanes", "woman"]), ("policeman", "policemen", ["policemans", "policemanes", "policeman"])]
        rule = "use an irregular plural"
    elif "child-children" in topic:
        pairs = [("child", "children", ["childs", "childes", "child"]), ("foot", "feet", ["foots", "feets", "foot"]), ("tooth", "teeth", ["tooths", "toothes", "tooth"])]
        rule = "use an irregular plural"
    elif "单复数同形" in topic:
        pairs = [("sheep", "sheep", ["sheeps", "sheepes", "sheepies"]), ("deer", "deer", ["deers", "deeres", "deeries"]), ("fish", "fish", ["fishes for the usual plural", "fishs", "fishies"])]
        rule = "keep the same form"
    elif "只有复数形式" in topic:
        return [
            q("Choose the correct sentence. 选择正确句子。", "My trousers are new.", ["My trousers is new.", "My trouser are new.", "A trousers is new."], seed + 1),
            q("Complete: These glasses ___ mine. 补全句子。", "are", ["is", "am", "be"], seed + 2),
            q("Which noun is normally plural-only? 哪个名词通常只有复数形式？", "scissors", ["chair", "book", "shirt"], seed + 3),
            q("Choose the correct phrase. 选择正确短语。", "a pair of trousers", ["a trousers", "one trousers", "a trouser"], seed + 4),
            q("Complete: The scissors ___ on the desk. 补全句子。", "are", ["is", "am", "has"], seed + 5),
            q("Which phrase is natural? 哪个短语自然？", "two pairs of glasses", ["two glass", "two glasseses", "two pair of glass"], seed + 6),
            q("Choose the sentence with correct agreement. 选择主谓一致正确的句子。", "His shorts are blue.", ["His shorts is blue.", "His short are blue.", "A shorts is blue."], seed + 7),
            q("Which word needs 'a pair of' for one item? 哪个词表示一件时常用 a pair of？", "scissors", ["desk", "apple", "river"], seed + 8),
            q("Complete: This pair of scissors ___ sharp. 补全句子。", "is", ["are", "am", "be"], seed + 9),
            q("Choose the best rule. 选择最佳规则。", "Some nouns are used only in plural form.", ["All nouns have singular forms.", "Plural-only nouns use a/an directly.", "Trousers is always singular."], seed + 10),
        ]
    elif "复合名词" in topic:
        pairs = [("sister-in-law", "sisters-in-law", ["sister-in-laws", "sisters-in-laws", "sister-ins-law"]), ("passer-by", "passers-by", ["passer-bys", "passers-bys", "passer-by"]), ("mother-in-law", "mothers-in-law", ["mother-in-laws", "mothers-in-laws", "mother-ins-law"])]
        rule = "make the main noun plural"
    else:
        pairs = [("book", "books", ["bookes", "bookies", "book"]), ("pen", "pens", ["penes", "penies", "pen"]), ("map", "maps", ["mapes", "mapies", "map"])]
        rule = "add -s"
    examples = []
    for n, (w, correct, wrongs) in enumerate((pairs * 4)[:10], 1):
        wrong_choices = []
        for candidate in list(wrongs) + [w]:
            if candidate != correct and candidate not in wrong_choices:
                wrong_choices.append(candidate)
        while len(wrong_choices) < 3:
            candidate = f"{w}s"
            if candidate != correct and candidate not in wrong_choices:
                wrong_choices.append(candidate)
            else:
                wrong_choices.append(f"{w}es")
        examples.append((f"There are {n + 1} ___ in the picture.", correct, wrong_choices[:3]))
    examples.append(("Which plural form is correct?", pairs[0][1], pairs[0][2]))
    return varied_questions(topic, examples, rule, seed)


def verb_form_questions(topic, seed):
    if "情态动词 + have done" in topic:
        examples = [
            ("He ___ left already; his coat is gone.", "must have", ["must", "has to", "must be"]),
            ("You ___ told me earlier.", "should have", ["should", "should be", "should has"]),
            ("She ___ missed the bus.", "may have", ["may", "may be", "may has"]),
            ("He ___ forgotten the meeting.", "might have", ["might", "might be", "might has"]),
        ]
        rule = "Use modal + have + past participle to talk about past speculation, regret, or unreal past meaning."
    elif "三单" in topic or "非三单" in topic or "一般现在时" in topic:
        examples = [
            ("He ___ to school.", "goes", ["go", "going", "went"]),
            ("They ___ soccer.", "play", ["plays", "playing", "played"]),
            ("She ___ English.", "studies", ["study", "studys", "studying"]),
            ("Tom ___ lunch at noon.", "has", ["have", "haves", "having"]),
        ]
        rule = "Use the base verb after I/you/we/they, and the third-person singular form after he/she/it."
    elif "现在分词" in topic or "-ing" in topic or "现在进行" in topic:
        examples = [
            ("She is ___ now.", "reading", ["read", "reads", "readed"]),
            ("They are ___ in the park.", "running", ["runing", "run", "ran"]),
            ("He is ___ a letter.", "writing", ["writeing", "writes", "wrote"]),
            ("The baby is ___.", "lying", ["lieing", "lies", "lied"]),
        ]
        rule = "Use am/is/are plus the -ing form for the present continuous."
    elif "过去式" in topic or "过去时" in topic or "didn't" in topic or "Did" in topic:
        examples = [
            ("I ___ TV yesterday.", "watched", ["watch", "watching", "watches"]),
            ("She ___ to Beijing last year.", "went", ["go", "goed", "goes"]),
            ("They didn't ___ late.", "arrive", ["arrived", "arrives", "arriving"]),
            ("___ you see him?", "Did", ["Do", "Does", "Are"]),
        ]
        rule = "Use the past form in affirmative sentences, and did/didn't plus the base verb in questions and negatives."
    elif "将来" in topic or "will" in topic or "going to" in topic or "shall" in topic:
        examples = [
            ("I will ___ tomorrow.", "leave", ["leaves", "left", "leaving"]),
            ("She is going to ___ a cake.", "make", ["makes", "made", "making"]),
            ("___ we meet at six?", "Shall", ["Did", "Does", "Are"]),
            ("They will not ___ late.", "be", ["are", "were", "being"]),
        ]
        rule = "Use will/be going to/shall plus the base verb for future meaning."
    elif "完成时" in topic or "have been" in topic or "has been" in topic:
        examples = [
            ("I have ___ my homework.", "finished", ["finish", "finishing", "finishes"]),
            ("She has ___ to London.", "gone", ["went", "go", "going"]),
            ("He has lived here ___ 2020.", "since", ["for", "at", "during"]),
            ("They have not ___ the film.", "seen", ["saw", "see", "seeing"]),
        ]
        rule = "Use have/has plus the past participle for the present perfect."
    elif "被动" in topic or "done" in topic:
        examples = [
            ("The room is ___ every day.", "cleaned", ["clean", "cleans", "cleaning"]),
            ("The letter was ___ yesterday.", "sent", ["send", "sends", "sending"]),
            ("The bridge will be ___.", "built", ["build", "building", "builds"]),
            ("The work must be ___.", "finished", ["finish", "finishing", "finishes"]),
        ]
        rule = "Use be plus the past participle to form the passive voice."
    else:
        examples = [
            ("Choose the correct verb form.", "to go", ["goes", "went", "going"]),
            ("Choose the correct verb form.", "doing", ["do", "did", "does"]),
            ("Choose the correct verb form.", "done", ["do", "does", "doing"]),
            ("Choose the correct verb form.", "can go", ["can goes", "can went", "can going"]),
        ]
        rule = english_gloss(topic)
    return varied_questions(topic, examples, rule, seed)


def article_questions(topic, seed):
    examples = [
        ("I saw ___ elephant.", "an", ["a", "the for first mention", "no article"]),
        ("She has ___ useful book.", "a", ["an", "the for first mention", "no article"]),
        ("___ sun is bright.", "The", ["A", "An", "No article"]),
        ("We play ___ basketball.", "no article", ["the", "a", "an"]),
        ("He is in ___ hospital as a patient.", "no article", ["the", "a", "an"]),
    ]
    if "an" in topic:
        examples = [("It is ___ old car.", "an", ["a", "the", "no article"]), ("She ate ___ apple.", "an", ["a", "the", "no article"])] + examples
    elif " a " in f" {topic} " or topic.startswith("不定冠词 a"):
        examples = [("He is ___ student.", "a", ["an", "the", "no article"]), ("This is ___ university.", "a", ["an", "the", "no article"])] + examples
    elif "the" in topic or "特指" in topic:
        examples = [("Open ___ door, please.", "the", ["a", "an", "no article"]), ("This is ___ first lesson.", "the", ["a", "an", "no article"])] + examples
    elif "零冠词" in topic:
        examples = [("We have lunch at ___ noon.", "no article", ["the", "a", "an"]), ("China is in ___ Asia.", "no article", ["the", "a", "an"])] + examples
    rule = "Choose a/an/the or no article according to sound, first mention, specific reference, and fixed expression."
    return varied_questions(topic, examples, rule, seed)


def hospital_article_questions(seed):
    """Questions for topic 067 with explicit contexts and no abstract blank option."""
    examples = [
        (
            "In British English, which sentence means that Jack is receiving medical treatment?",
            "Jack is in hospital after the operation.",
            [
                "Jack is in the hospital to visit his sister.",
                "Jack is beside the hospital waiting for a taxi.",
                "Jack works at the hospital every weekday.",
            ],
        ),
        (
            "Which sentence says that Lisa went to a particular hospital building to see a patient?",
            "Lisa went to the hospital to visit her grandfather.",
            [
                "Lisa is in hospital with a broken leg.",
                "Lisa was taken to hospital after the accident.",
                "Lisa stayed in hospital for three days as a patient.",
            ],
        ),
        (
            "Tom was hurt in a cycling accident and is now a patient. Which sentence is correct in British English?",
            "Tom is in hospital.",
            [
                "Tom is in the hospital to deliver some flowers.",
                "Tom is near the hospital, not inside it.",
                "Tom works in the hospital kitchen.",
            ],
        ),
        (
            "Mia is not a patient; she is visiting her mother. Which sentence expresses this meaning?",
            "Mia is at the hospital visiting her mother.",
            [
                "Mia is in hospital after an operation.",
                "Mia was sent to hospital for treatment.",
                "Mia has been in hospital as a patient since Monday.",
            ],
        ),
        (
            "Which sentence focuses on the hospital as a specific building?",
            "The pharmacy is opposite the hospital.",
            [
                "The injured driver was taken to hospital.",
                "Ben has been in hospital since Tuesday.",
                "The doctor says Eva must stay in hospital tonight.",
            ],
        ),
        (
            "Ava had an operation and remained there for treatment. Which sentence is correct in British English?",
            "Ava stayed in hospital for a week.",
            [
                "Ava went to the hospital only to collect her bag.",
                "Ava waited outside the hospital for her friend.",
                "Ava works in the hospital reception area.",
            ],
        ),
        (
            "The speaker is giving directions to one known building. Which sentence is the best choice?",
            "Turn left when you reach the hospital.",
            [
                "Turn left because you are receiving treatment in hospital.",
                "Turn left after you are taken to hospital as a patient.",
                "Turn left while you stay in hospital for surgery.",
            ],
        ),
        (
            "Noah is the patient and his wife is the visitor. Which sentence is correct in British English?",
            "Noah is in hospital; his wife is at the hospital visiting him.",
            [
                "Noah is at the hospital visiting his wife; she is in hospital.",
                "Noah works at the hospital; his wife is in hospital after an operation.",
                "Noah is outside the hospital; his wife was taken to hospital for treatment.",
            ],
        ),
        (
            "Leo needs medical treatment after a fall. Which sentence is most natural in British English?",
            "Leo may have to go to hospital.",
            [
                "Leo may have to go to the hospital merely to visit a friend.",
                "Leo may have to stand behind the hospital building.",
                "Leo may have to work at the hospital reception desk.",
            ],
        ),
        (
            "Sophie is identifying the building where her father works. Which sentence is correct?",
            "Her father works at the hospital near the station.",
            [
                "Her father is in hospital because he is recovering from surgery.",
                "Her father goes to hospital whenever he needs treatment.",
                "Her father stayed in hospital after an accident.",
            ],
        ),
    ]
    return [q(stem, correct, wrongs, seed + i) for i, (stem, correct, wrongs) in enumerate(examples, 1)]


def make_blanks_visible(questions):
    """Use a visible answer slot because thin underscores disappear in some PDF viewers."""
    visible_blank = "（　　）"
    cleaned = []
    for stem, options, answer in questions:
        stem = stem.replace("___", visible_blank)
        options = [
            "不填冠词"
            if option.lower() == "no article"
            else re.sub(r"\bno article\b", "leave the article blank", option, flags=re.IGNORECASE)
            for option in options
        ]
        cleaned.append((stem, options, answer))
    return cleaned


def pronoun_questions(topic, seed):
    if "宾格" in topic or "whom" in topic:
        examples = [("Please help ___.", "me", ["I", "my", "mine"]), ("The teacher asked ___.", "him", ["he", "his", "himself"]), ("Whom did you invite?", "Whom", ["Who as object in formal grammar", "Whose", "Which"])]
    elif "物主" in topic:
        examples = [("This is ___ book.", "my", ["mine", "I", "me"]), ("The red bag is ___.", "hers", ["her", "she", "herself"]), ("Their house is big; ___ is small.", "ours", ["our", "we", "us"])]
    elif "反身" in topic:
        examples = [("She hurt ___.", "herself", ["her", "hers", "she"]), ("I made it ___.", "myself", ["me", "my", "mine"]), ("Enjoy ___!", "yourself", ["you", "your", "yours"])]
    elif "this / that" in topic:
        examples = [("___ is my pen here.", "This", ["These", "Those", "They"]), ("___ is your bag over there.", "That", ["These", "Those", "They"])]
    elif "these / those" in topic:
        examples = [("___ are my books here.", "These", ["This", "That", "It"]), ("___ are your shoes over there.", "Those", ["This", "That", "It"])]
    elif "some / any" in topic:
        examples = [("I have ___ apples.", "some", ["any in affirmative", "much", "little"]), ("Do you have ___ water?", "any", ["some in ordinary question", "many", "few"])]
    elif "many / much" in topic:
        examples = [("There are ___ books.", "many", ["much", "little", "a little"]), ("There is ___ milk.", "much", ["many", "few", "a few"])]
    elif "few" in topic or "little" in topic:
        examples = [("I have ___ friends, so I feel lonely.", "few", ["a few", "little", "a little"]), ("We have ___ time, so hurry.", "little", ["a little", "few", "a few"])]
    elif "both" in topic or "either" in topic:
        examples = [("___ of the two boys are here.", "Both", ["All", "None", "Every"]), ("You may choose either of the two.", "either", ["all", "none for more than two", "every"])]
    elif "all / none" in topic:
        examples = [("___ of the three girls came.", "All", ["Both", "Either", "Neither"]), ("None of the students ___ late.", "was", ["were always only", "be", "am"])]
    elif "each / every" in topic:
        examples = [("___ student has a book.", "Each", ["Both", "All", "Many"]), ("Every child ___ a seat.", "has", ["have", "are", "be"])]
    elif "one / ones" in topic:
        examples = [("I need a pen. Do you have ___?", "one", ["ones", "it for unknown choice", "them"]), ("These apples are nice. I want the red ___.", "ones", ["one when plural", "it", "that"])]
    elif "something" in topic or "anything" in topic or "nothing" in topic:
        examples = [("I have ___ to tell you.", "something", ["anything in affirmative usually", "nothing with positive meaning", "someone"]), ("There is ___ wrong.", "nothing", ["anything in affirmative", "somebody", "many"])]
    elif "形容词后置" in topic:
        examples = [("I need something ___.", "cold", ["cold something", "a cold", "the cold"]), ("There is nothing ___ here.", "new", ["new nothing", "a new", "the new"])]
    elif "other" in topic:
        examples = [("I have two pens. One is blue; ___ is black.", "the other", ["other", "others", "the others"]), ("Some students like tea; ___ like juice.", "others", ["the other", "other", "another only one"])]
    else:
        examples = [("___ am a student.", "I", ["Me", "My", "Mine"]), ("___ is my friend.", "He", ["Him", "His", "Himself"]), ("___ did you see?", "Who", ["Whose", "Which for person usually", "What for person name"])]
    rule = "Choose the pronoun form that matches number, case, ownership, distance, or reference in the sentence."
    return varied_questions(topic, examples, rule, seed)


def comparison_questions(topic, seed):
    if "最高级" in topic or "-est" in topic or "most" in topic or "best" in topic or "worst" in topic:
        examples = [("Tom is the ___ boy in his class.", "tallest", ["taller", "tall", "more tall"]), ("This is the ___ interesting story.", "most", ["more", "much", "many"]), ("good 的最高级是 ___.", "best", ["better", "gooder", "goodest"]), ("She is the tallest ___ the three.", "of", ["than", "in city", "on"])]
    else:
        examples = [("Tom is ___ than Jack.", "taller", ["tallest", "tall", "most tall"]), ("This book is ___ interesting than that one.", "more", ["most", "much", "many"]), ("good 的比较级是 ___.", "better", ["best", "gooder", "well"]), ("It is getting ___.", "warmer and warmer", ["warmest and warmest", "more warm and more", "warm and warm"])]
    rule = "Use the comparative or superlative form according to the number of things compared and the word form."
    return varied_questions(topic, examples, rule, seed)


def preposition_questions(topic, seed):
    if topic.startswith("in + 年"):
        examples = [("___ 2024", "in", ["on", "at", "by"]), ("___ July", "in", ["on", "at", "to"]), ("___ spring", "in", ["on", "at", "for"])]
    elif topic.startswith("on +"):
        examples = [("___ Monday", "on", ["in", "at", "by"]), ("___ May 1", "on", ["in", "at", "for"])]
    elif topic.startswith("at +"):
        examples = [("___ six o'clock", "at", ["in", "on", "for"]), ("___ noon", "at", ["in", "on", "during"])]
    elif "since / for" in topic:
        examples = [("I have lived here ___ 2020.", "since", ["for", "during", "at"]), ("She has studied for two hours.", "for", ["since", "at", "on"])]
    elif "between / among" in topic:
        examples = [("The ball is ___ the two boxes.", "between", ["among", "over", "through"]), ("She stood ___ many students.", "among", ["between", "across", "below"])]
    elif "through / across" in topic:
        examples = [("Walk ___ the bridge.", "across", ["through", "in", "among"]), ("The train went ___ the tunnel.", "through", ["across", "over", "on"])]
    elif "by +" in topic:
        examples = [("I go to school ___ bus.", "by", ["with", "in", "on a"]), ("The message was sent ___ email.", "by", ["with", "at", "for"])]
    elif "with +" in topic:
        examples = [("She cut the paper ___ scissors.", "with", ["by", "in", "on"]), ("He wrote ___ a pen.", "with", ["by", "at", "from"])]
    elif "in + 语言" in topic:
        examples = [("Please answer ___ English.", "in", ["by", "with", "on"]), ("The desk is made ___ wood.", "of", ["in", "by", "with"])]
    else:
        examples = [("He is ___ school.", "at", ["in for city", "on", "over"]), ("The picture is ___ the wall.", "on", ["in", "at", "below"]), ("The cat is ___ the table.", "under", ["above when lower", "over", "between"])]
    rule = "Choose the preposition according to time, place, direction, means, instrument, or fixed collocation."
    return varied_questions(topic, examples, rule, seed)


def possessive_questions(topic, seed):
    if "s 结尾复数" in topic:
        examples = [
            ("The ___ room is on the second floor.", "teachers'", ["teacher's", "teachers", "teacher"]),
            ("The ___ bags are near the door.", "students'", ["student's", "students", "student"]),
            ("The ___ uniforms are blue.", "nurses'", ["nurse's", "nurses", "nurse"]),
            ("The ___ office is closed today.", "workers'", ["worker's", "workers", "worker"]),
        ]
        rule = "For plural nouns ending in -s, add only an apostrophe to show possession."
    elif "不以 s 结尾复数" in topic:
        examples = [
            ("The ___ toys are everywhere.", "children's", ["childrens'", "children", "child's"]),
            ("The ___ shoes are by the door.", "men's", ["mens'", "men", "man's"]),
            ("The ___ coats are red.", "women's", ["womens'", "women", "woman's"]),
            ("The ___ room is downstairs.", "people's", ["peoples'", "people", "person's"]),
        ]
        rule = "For plural nouns not ending in -s, add apostrophe + s."
    elif "共同拥有" in topic:
        examples = [
            ("___ car is new. Tom and Jack share one car.", "Tom and Jack's", ["Tom's and Jack's", "Tom and Jack", "Tom's and Jack"]),
            ("___ rooms are on different floors. They each have one.", "Linda's and Mary's", ["Linda and Mary's", "Linda and Mary", "Linda's and Mary"]),
            ("___ house is near the park. It belongs to both of them.", "Mr. and Mrs. Green's", ["Mr.'s and Mrs. Green's", "Mr. and Mrs. Green", "Mr.'s and Mrs. Green"]),
            ("___ bikes are outside. Each boy has a bike.", "Ben's and Leo's", ["Ben and Leo's", "Ben and Leo", "Ben's and Leo"]),
        ]
        rule = "Use one possessive ending for shared ownership, and separate possessive endings for separate ownership."
    elif "of 所有格" in topic:
        examples = [
            ("The ___ is open.", "door of the room", ["room's door for object", "room door's", "door's room"]),
            ("I like the ___ of the story.", "ending", ["story's ending always", "end's story", "story ending's"]),
            ("The ___ of the building is white.", "roof", ["building's roof always", "roof's building", "building roof's"]),
            ("The ___ of the table is smooth.", "surface", ["table's surface always", "surface's table", "table surface's"]),
        ]
        rule = "Use of-possessive especially for inanimate things, parts, and abstract relationships."
    elif "双重所有格" in topic:
        examples = [
            ("She is ___ mine.", "a friend of", ["a friend of me", "my friend of", "a friend mine"]),
            ("This is ___ father's.", "a photo of my", ["a photo of me", "my photo of", "a photo my"]),
            ("He is ___ Tom's.", "a classmate of", ["a classmate Tom", "Tom's classmate of", "a classmate of Tom"]),
            ("I borrowed ___ hers.", "a book of", ["a book her", "her book of", "a book of she"]),
        ]
        rule = "A double possessive uses of plus a possessive noun or possessive pronoun."
    else:
        examples = [
            ("This is ___ book.", "Tom's", ["Tom", "Toms'", "Tom is"]),
            ("That is ___ bag.", "my sister's", ["my sister", "my sisters", "my sister is"]),
            ("The ___ tail is long.", "cat's", ["cats'", "cat", "cats"]),
            ("I found ___ pencil.", "Jack's", ["Jack", "Jacks'", "Jack is"]),
        ]
        rule = "For most singular nouns, add apostrophe + s to show possession."
    return varied_questions(topic, examples, rule, seed)


def number_questions(topic, seed):
    if "hundred / thousand / million 前有具体数字" in topic:
        examples = [
            ("There are two ___ students.", "hundred", ["hundreds", "hundred of", "hundreds of"]),
            ("The city has five ___ people.", "million", ["millions", "million of", "millions of"]),
            ("She paid three ___ dollars.", "thousand", ["thousands", "thousand of", "thousands of"]),
            ("They planted six ___ trees.", "hundred", ["hundreds", "hundreds of", "hundred of"]),
        ]
        rule = "After a specific number, hundred/thousand/million stay singular and do not take of."
    elif "hundreds of" in topic or "thousands of" in topic:
        examples = [
            ("___ birds flew over the lake.", "Hundreds of", ["Hundred", "Three hundreds", "Hundred of"]),
            ("___ people visited the museum.", "Thousands of", ["Thousand", "Two thousands", "Thousand of"]),
            ("There are ___ stars in the sky.", "millions of", ["million", "three millions", "million of"]),
            ("___ fans waited outside.", "Hundreds of", ["Hundred", "Five hundreds", "Hundred of"]),
        ]
        rule = "Use hundreds of/thousands of/millions of for vague large numbers."
    elif "1-100" in topic:
        examples = [
            ("Choose the correct spelling of 13.", "thirteen", ["threeteen", "thirty", "teenthree"]),
            ("Choose the correct spelling of 40.", "forty", ["fourty", "fourteen", "forteen"]),
            ("Choose the correct spelling of 80.", "eighty", ["eightty", "eighteen", "eightteen"]),
            ("Choose the correct spelling of 21.", "twenty-one", ["twenteen-one", "twenty first", "two-one"]),
        ]
        rule = "Spell cardinal numbers accurately; use a hyphen for compounds like twenty-one."
    elif "特殊序数词" in topic:
        examples = [
            ("one 的序数词是 ___.", "first", ["oneth", "oneest", "fiveth"]),
            ("two 的序数词是 ___.", "second", ["twoth", "twoest", "twentieth"]),
            ("three 的序数词是 ___.", "third", ["threeth", "threeest", "thirth"]),
            ("She came ___ in the race.", "first", ["one", "oneth", "firstly only"]),
        ]
        rule = "The ordinal forms of one, two, and three are first, second, and third."
    elif "-ve 结尾" in topic:
        examples = [
            ("five 的序数词是 ___.", "fifth", ["fiveth", "fivethth", "fiveith"]),
            ("twelve 的序数词是 ___.", "twelfth", ["twelveth", "twelvethth", "twelveths"]),
            ("This is my ___ birthday.", "twelfth", ["twelveth", "twelve", "twelveths"]),
            ("The ___ lesson is about fractions.", "fifth", ["fiveth", "five", "fivest"]),
        ]
        rule = "For five and twelve, change ve to f before adding -th."
    elif "-ty 结尾" in topic:
        examples = [
            ("twenty 的序数词是 ___.", "twentieth", ["twentyth", "twentyth", "twentieths"]),
            ("thirty 的序数词是 ___.", "thirtieth", ["thirtyth", "thirteeth", "thirtith"]),
            ("This is the ___ page.", "twentieth", ["twenty", "twentyth", "twentyth"]),
            ("He finished ___ in the race.", "thirtieth", ["thirty", "thirtyth", "threeth"]),
        ]
        rule = "For -ty numbers, change y to i and add -eth."
    elif "序数词缩写" in topic:
        examples = [
            ("Choose the correct abbreviation for first.", "1st", ["1th", "1rd", "1nd"]),
            ("Choose the correct abbreviation for second.", "2nd", ["2st", "2rd", "2th"]),
            ("Choose the correct abbreviation for third.", "3rd", ["3st", "3nd", "3th"]),
            ("Choose the correct abbreviation for fourth.", "4th", ["4st", "4nd", "4rd"]),
        ]
        rule = "Use 1st, 2nd, 3rd, and usually -th from 4th onward."
    elif "分数表达" in topic:
        examples = [
            ("1/3 is read as ___.", "one third", ["one three", "first three", "one thirds"]),
            ("2/3 is read as ___.", "two thirds", ["two third", "second thirds", "two three"]),
            ("3/4 is read as ___.", "three fourths", ["three fourth", "third four", "three fours"]),
            ("1/2 is read as ___.", "one half", ["one second", "one halves", "first halfs"]),
        ]
        rule = "Use a cardinal numerator and an ordinal denominator; add -s to the denominator when the numerator is greater than one."
    elif "小数" in topic:
        examples = [
            ("3.14 is read as ___.", "three point one four", ["three point fourteen", "three and fourteen", "third point fourteen"]),
            ("0.5 is read as ___.", "zero point five", ["zero and five", "five point zero", "zeroth five"]),
            ("12.06 is read as ___.", "twelve point zero six", ["twelve point six", "twelve and six", "twelfth point six"]),
            ("2.8 is read as ___.", "two point eight", ["two and eight", "second point eight", "twenty-eight"]),
        ]
        rule = "Read decimals with point, then say each digit after the decimal point."
    elif "百分数" in topic:
        examples = [
            ("25% is read as ___.", "twenty-five percent", ["twenty-five percentage", "twenty fifth percent", "percent twenty-five"]),
            ("Only ___ of the students passed.", "60 percent", ["60 percents", "60 percentage", "percent 60"]),
            ("100% is read as ___.", "one hundred percent", ["one hundreds percent", "hundred percentage", "one hundred percents"]),
            ("The price rose by ___.", "ten percent", ["ten percents", "tenth percent", "percent ten"]),
        ]
        rule = "Use percent after the number; percent does not take plural -s."
    elif "past 表达" in topic:
        examples = [
            ("8:10 can be said as ___.", "ten past eight", ["ten to eight", "eight past ten", "eight to ten"]),
            ("6:20 can be said as ___.", "twenty past six", ["twenty to six", "six past twenty", "six to twenty"]),
            ("9:15 can be said as ___.", "a quarter past nine", ["a quarter to nine", "nine past quarter", "quarter nine past"]),
            ("3:05 can be said as ___.", "five past three", ["five to three", "three past five", "three to five"]),
        ]
        rule = "Use minutes past the hour for times after the hour."
    elif "to 表达" in topic:
        examples = [
            ("7:50 can be said as ___.", "ten to eight", ["ten past eight", "eight to ten", "seven past fifty"]),
            ("4:45 can be said as ___.", "a quarter to five", ["a quarter past five", "five to quarter", "four past forty-five"]),
            ("11:55 can be said as ___.", "five to twelve", ["five past twelve", "twelve to five", "eleven past fifty-five"]),
            ("2:40 can be said as ___.", "twenty to three", ["twenty past three", "three to twenty", "two past forty"]),
        ]
        rule = "Use minutes to the next hour for times before the next hour."
    elif "整点、半点" in topic:
        examples = [
            ("6:00 can be said as ___.", "six o'clock", ["six half", "half six in standard school English", "six past"]),
            ("8:30 can be said as ___.", "half past eight", ["half to eight", "eight past half", "half eight in formal school form"]),
            ("12:00 can be said as ___.", "twelve o'clock", ["twelve past", "half past twelve", "to twelve"]),
            ("1:30 can be said as ___.", "half past one", ["half to one", "one to half", "one past half"]),
        ]
        rule = "Use o'clock for exact hours and half past for thirty minutes after the hour."
    elif "日期" in topic:
        examples = [
            ("May 1 is read as ___.", "May the first", ["May one", "the May first", "May firsts"]),
            ("September 10 is read as ___.", "September the tenth", ["September ten", "the September tenth", "September tenst"]),
            ("Write the date with an ordinal abbreviation.", "June 3rd", ["June 3th", "June 3nd", "June 3st"]),
            ("December 25 is read as ___.", "December the twenty-fifth", ["December twenty-five", "the December twenty-five", "December twenty-fiveth"]),
        ]
        rule = "Dates are commonly read with ordinal numbers."
    elif "年代" in topic:
        examples = [
            ("the 1990s means ___.", "the years from 1990 to 1999", ["only the year 1990", "nineteen ninety", "the 1990th year"]),
            ("Complete: This song was popular ___ the 1980s.", "in", ["on", "at", "to"]),
            ("Choose the correct form.", "in the 2000s", ["in the 2000's as required form", "on the 2000s", "at 2000s"]),
            ("the 1960s is read as ___.", "the nineteen sixties", ["the nineteen sixty", "the sixtieth", "the one nine six zero"]),
        ]
        rule = "Use in the + year + s to talk about a decade."
    else:
        examples = [
            ("four 的序数词是 ___.", "fourth", ["four", "fiveth", "fourst"]),
            ("six 的序数词是 ___.", "sixth", ["six", "sixst", "sixrd"]),
            ("ten 的序数词是 ___.", "tenth", ["ten", "tenst", "tenty"]),
            ("This is the ___ lesson.", "sixth", ["six", "sixteen", "sixst"]),
        ]
        rule = "For many ordinal numbers, add -th to the cardinal number with any needed spelling change."
    return varied_questions(topic, examples, rule, seed)


def adjective_adverb_questions(topic, seed):
    if "作定语" in topic:
        examples = [
            ("She has a ___ dress.", "red", ["redly", "very", "beauty"]),
            ("I bought an ___ book.", "interesting", ["interestingly", "interest", "interestedly"]),
            ("The ___ boy is my brother.", "tall", ["tallly", "height", "taller than"]),
            ("They live in a ___ house.", "small", ["smallly", "smaller than", "smallness"]),
        ]
        rule = "An attributive adjective usually goes before the noun it modifies."
    elif "作表语" in topic:
        examples = [
            ("The soup tastes ___.", "good", ["well as adjective here", "goodly", "nicely"]),
            ("She looks ___ today.", "happy", ["happily", "happiness", "happier than"]),
            ("The room is ___.", "clean", ["cleanly", "cleaning", "cleaned by"]),
            ("This music sounds ___.", "beautiful", ["beautifully", "beauty", "more beautifully"]),
        ]
        rule = "A predicative adjective follows a linking verb such as be, look, sound, taste, or feel."
    elif "宾语补足语" in topic:
        examples = [
            ("The news made me ___.", "happy", ["happily", "happiness", "to happy"]),
            ("We found the room ___.", "empty", ["emptily", "emptiness", "to empty"]),
            ("Keep the door ___.", "open", ["openly", "opened by", "opening"]),
            ("The teacher made the rule ___.", "clear", ["clearly", "clearness", "to clear"]),
        ]
        rule = "An adjective can describe the object as an object complement."
    elif "多个形容词" in topic:
        examples = [
            ("She bought a ___ dress.", "beautiful long red", ["red long beautiful", "long red beautiful", "beautiful red long"]),
            ("He lives in a ___ house.", "small old stone", ["stone old small", "old stone small", "small stone old"]),
            ("I saw a ___ table.", "large round wooden", ["wooden round large", "round wooden large", "large wooden round"]),
            ("They found a ___ box.", "little square blue", ["blue square little", "square little blue", "little blue square"]),
        ]
        rule = "A common adjective order is opinion, size, age, shape, color, origin, material, purpose."
    elif "-ing 形容词" in topic or "-ed 形容词" in topic:
        examples = [
            ("The film is ___.", "boring", ["bored", "bore", "boringly for adjective"]),
            ("I feel ___ after the long meeting.", "tired", ["tiring", "tire", "tiredly"]),
            ("The story was ___.", "exciting", ["excited", "excite", "excitedly"]),
            ("The children were ___ by the game.", "interested", ["interesting", "interest", "interestingly"]),
        ]
        rule = "-ing adjectives describe the cause; -ed adjectives describe a person's feeling."
    elif "good-well" in topic:
        examples = [
            ("She sings ___.", "well", ["good", "goodly", "better as base adverb"]),
            ("He is a ___ swimmer.", "good", ["well", "goodly", "wellly"]),
            ("The team played ___.", "well", ["good", "gooder", "goodly"]),
            ("This is a ___ answer.", "good", ["well", "wellly", "goodly"]),
        ]
        rule = "Good is usually an adjective; well is usually the adverb form."
    elif "副词位置" in topic:
        examples = [
            ("She ___ goes to school by bus.", "often", ["goes often to", "is often goes", "often is goes"]),
            ("He is ___ late.", "never", ["late never", "never is", "is late never"]),
            ("They have ___ finished dinner.", "already", ["finished already have", "have finished already only", "already have finished never"]),
            ("I can ___ understand him.", "hardly", ["understand hardly him", "can understand hardly him", "hard him understand"]),
        ]
        rule = "Frequency and many mid-position adverbs often go before main verbs but after be, auxiliaries, or modals."
    elif "enough" in topic:
        examples = [
            ("He is old ___ to drive.", "enough", ["enough old", "too", "very"]),
            ("She runs fast ___ to win.", "enough", ["enough fast", "too", "very"]),
            ("The box is not light ___.", "enough", ["enough light", "too", "very"]),
            ("This room is big ___ for us.", "enough", ["enough big", "too", "many"]),
        ]
        rule = "Enough comes after the adjective or adverb it modifies."
    elif "辅音 + y" in topic and "-ly" in topic:
        examples = [
            ("happy 变副词是 ___.", "happily", ["happyly", "happiely", "happy"]),
            ("easy 变副词是 ___.", "easily", ["easyly", "easiely", "easy"]),
            ("She answered ___.", "happily", ["happyly", "happy", "happier"]),
            ("He solved it ___.", "easily", ["easyly", "easy", "easier"]),
        ]
        rule = "For consonant + y adjectives, change y to i and add -ly."
    elif "le 结尾" in topic:
        examples = [
            ("simple 变副词是 ___.", "simply", ["simplely", "simplily", "simple"]),
            ("gentle 变副词是 ___.", "gently", ["gentlely", "gentily", "gentle"]),
            ("He explained it ___.", "simply", ["simplely", "simple", "simpler"]),
            ("She spoke ___.", "gently", ["gentlely", "gentle", "gentlier"]),
        ]
        rule = "For many -le adjectives, drop e and add -y to form the adverb."
    else:
        examples = [
            ("quick 变副词是 ___.", "quickly", ["quick", "quickily", "quickness"]),
            ("slow 变副词是 ___.", "slowly", ["slow", "slowlily", "slowness"]),
            ("She walks ___.", "slowly", ["slow", "slower", "slowest"]),
            ("He answered ___.", "quickly", ["quick", "quicker", "quickness"]),
        ]
        rule = "Many adjectives form adverbs by adding -ly."
    return varied_questions(topic, examples, rule, seed)


def syntax_questions(topic, seed):
    if "识别主语" in topic:
        examples = [("In 'The boy runs fast,' the subject is ___.", "The boy", ["runs", "fast", "boy runs"]), ("In 'Mary likes tea,' the subject is ___.", "Mary", ["likes", "tea", "likes tea"])]
    elif "识别谓语" in topic:
        examples = [("In 'The boy runs fast,' the predicate verb is ___.", "runs", ["The boy", "fast", "boy"]), ("In 'She can swim,' the predicate is ___.", "can swim", ["She", "swim only", "can only"])]
    elif "识别宾语" in topic:
        examples = [("In 'I read a book,' the object is ___.", "a book", ["I", "read", "book read"]), ("In 'She loves music,' the object is ___.", "music", ["She", "loves", "She loves"])]
    elif "识别表语" in topic:
        examples = [("In 'He is happy,' the predicative is ___.", "happy", ["He", "is", "He is"]), ("In 'This soup tastes good,' the predicative is ___.", "good", ["soup", "tastes", "This"])]
    elif "宾语补足语" in topic:
        examples = [("In 'We found him honest,' the object complement is ___.", "honest", ["We", "him", "found"]), ("In 'They made her captain,' the object complement is ___.", "captain", ["They", "made", "her"])]
    elif "同位语" in topic:
        examples = [("In 'Tom, my brother, is here,' the appositive is ___.", "my brother", ["Tom", "is", "here"]), ("Choose the appositive.", "Mr. Green, our teacher", ["runs fast", "very happy", "in the room"])]
    elif topic.startswith("S + V"):
        examples = [("Which sentence matches the pattern?", "Birds fly.", ["She is happy.", "I read books.", "He gave me a pen."])]
    elif "疑问" in topic or "what 引导" in topic or "where 引导" in topic or "how" in topic:
        examples = [("Choose the correct question.", "Where do you live?", ["Where you live?", "Where does you live?", "Where are you live?"]), ("Choose the correct short answer.", "Yes, I am.", ["Yes, I do am.", "Yes, I is.", "Yes, am."])]
    elif "祈使" in topic or "Don't" in topic or "Let's" in topic:
        examples = [("Choose the imperative sentence.", "Open the door.", ["You open the door?", "Opened the door.", "To open the door."]), ("Choose the negative imperative.", "Don't run.", ["Not run.", "Doesn't run.", "No running it."])]
    elif "What" in topic and "形容词" in topic:
        examples = [("Choose the correct exclamation.", "What a nice day!", ["How a nice day!", "What nice a day!", "What day nice!"])]
    elif "There be" in topic:
        examples = [("Choose the correct sentence.", "There is a book on the desk.", ["There has a book on the desk.", "There are a book on the desk.", "There be a book on the desk."]), ("Complete: There ___ two pens.", "are", ["is", "has", "be"])]
    elif "and" in topic:
        examples = [("Choose the best conjunction.", "I opened the door and walked in.", ["but", "so", "or"])]
    elif "but" in topic:
        examples = [("Choose the best conjunction.", "He is poor but happy.", ["and", "so", "because"])]
    elif "so 表结果" in topic:
        examples = [("Choose the best conjunction.", "It rained, so we stayed home.", ["but", "or", "and"])]
    elif "or" in topic:
        examples = [("Choose the best conjunction.", "Hurry up, or you will be late.", ["and", "but", "so"])]
    else:
        examples = [("Choose the sentence that fits this grammar point.", "This is the correct pattern.", ["This are the correct pattern.", "This correct pattern.", "This be correct pattern."])]
    rule = "Identify or build the sentence pattern according to the role of each word group in the sentence."
    return varied_questions(topic, examples, rule, seed)


def clause_questions(topic, seed):
    if "who" in topic:
        examples = [("The man ___ lives next door is a doctor.", "who", ["which", "where", "when"]), ("I know the girl ___ won the prize.", "who", ["which", "why", "when"])]
    elif "whom" in topic:
        examples = [("The man ___ I met was kind.", "whom", ["which", "whose", "where"]), ("This is the teacher ___ we invited.", "whom", ["which", "when", "why"])]
    elif "whose" in topic:
        examples = [("The boy ___ bike was lost is sad.", "whose", ["who", "whom", "which"]), ("I know a girl ___ father is a pilot.", "whose", ["who", "where", "when"])]
    elif "which" in topic:
        examples = [("The book ___ I bought is useful.", "which", ["who", "where", "when"]), ("He showed me the photo, ___ was beautiful.", "which", ["that in nonrestrictive clause", "who", "why"])]
    elif "that" in topic:
        examples = [("This is the best film ___ I have seen.", "that", ["which after superlative", "where", "when"]), ("The dog ___ barked is mine.", "that", ["where", "why", "whom"])]
    elif "when" in topic:
        examples = [("I remember the day ___ we met.", "when", ["where", "why", "who"]), ("Call me ___ you arrive.", "when", ["where", "who", "which"])]
    elif "where" in topic:
        examples = [("This is the place ___ I was born.", "where", ["when", "why", "who"]), ("Stay ___ you are.", "where", ["when", "which", "whose"])]
    elif "why" in topic:
        examples = [("Tell me the reason ___ you left.", "why", ["where", "when", "who"])]
    elif "if / whether" in topic:
        examples = [("I wonder ___ he will come.", "whether", ["that", "who", "where"]), ("She asked ___ I liked tea.", "if", ["that", "which", "whose"])]
    elif "because" in topic:
        examples = [("I stayed home ___ I was ill.", "because", ["so", "although", "where"])]
    elif "though" in topic or "although" in topic:
        examples = [("___ it was raining, we went out.", "Although", ["Because", "So", "Where"])]
    elif "unless" in topic:
        examples = [("You will fail ___ you work hard.", "unless", ["if", "because", "although"])]
    elif "so ... that" in topic or "such ... that" in topic:
        examples = [("He was ___ tired that he slept at once.", "so", ["such", "too", "enough"]), ("It was ___ a good film that we watched it twice.", "such", ["so", "too", "very"])]
    elif "so that" in topic:
        examples = [("Speak clearly ___ everyone can hear you.", "so that", ["because", "although", "unless"])]
    else:
        examples = [("I believe ___ he is honest.", "that", ["what", "where", "whose"]), ("___ he said is true.", "What", ["That as subject content", "Where", "Whoever for place"])]
    rule = "Choose the correct conjunction, relative word, or clause structure according to its role and meaning."
    return varied_questions(topic, examples, rule, seed)


def special_questions(topic, seed):
    if "only +" in topic:
        examples = [
            ("Only then ___ the truth.", "did I understand", ["I understood", "understood I", "I did understand"]),
            ("Only in this way ___ the problem.", "can we solve", ["we can solve", "we solve can", "can solve we"]),
            ("Only after the class ___ home.", "did he go", ["he went", "went he", "he did went"]),
            ("Only when she called ___ safe.", "did I feel", ["I felt", "felt I", "I did felt"]),
        ]
        rule = "When only plus an adverbial is placed at the beginning, use partial inversion in the main clause."
    elif "否定词置于句首" in topic:
        examples = [
            ("Never ___ such a beautiful place.", "have I seen", ["I have seen", "I saw have", "have seen I"]),
            ("Hardly ___ the room when it started raining.", "had we entered", ["we had entered", "had entered we", "we entered had"]),
            ("Not only ___ English, but he also speaks French.", "does he speak", ["he speaks", "he does speak", "speaks he"]),
            ("Little ___ about the plan.", "did I know", ["I knew", "knew I", "I did knew"]),
        ]
        rule = "When a negative word or phrase begins the sentence, use partial inversion."
    elif "so / neither / nor" in topic:
        examples = [
            ("Tom likes music, and ___ Mary.", "so does", ["so is", "neither does", "Mary does so"]),
            ("I can't swim, and ___ my brother.", "neither can", ["so can", "neither does", "nor does"]),
            ("She was tired, and ___ I.", "so was", ["so did", "neither was", "was so"]),
            ("He hasn't finished, and ___ I.", "neither have", ["so have", "neither did", "nor do"]),
        ]
        rule = "Use so plus auxiliary plus subject for agreement with an affirmative statement; use neither/nor for a negative statement."
    elif "完全倒装" in topic:
        examples = [
            ("On the wall ___ a picture.", "hangs", ["a picture hangs", "does hang", "is hang"]),
            ("Here ___ the bus.", "comes", ["the bus comes", "does come", "coming"]),
            ("Under the tree ___ an old man.", "sat", ["an old man sat", "did sit", "was sit"]),
            ("Away ___ the children.", "ran", ["the children ran", "did run", "were run"]),
        ]
        rule = "Full inversion can place the whole verb before the subject after certain place or direction adverbials."
    elif "强调句型" in topic:
        examples = [
            ("___ Tom who broke the window.", "It was", ["It is was", "There was", "This was"]),
            ("It was in Beijing ___ I met her.", "that", ["where in cleft", "which", "when"]),
            ("___ Mary that won the prize.", "It was", ["She was", "There was", "That was"]),
            ("It is my father ___ teaches me English.", "who", ["which", "where", "when"]),
        ]
        rule = "Use It is/was + emphasized part + that/who + the rest of the sentence."
    elif "省略" in topic:
        examples = [
            ("When ___ young, he liked drawing.", "he was", ["was he always required", "he is", "being he"]),
            ("If ___ possible, call me tonight.", "it is", ["is it always required", "it was", "being it"]),
            ("Though ___ tired, she kept working.", "she was", ["was she", "she is always", "being she"]),
            ("While ___ in London, I visited the museum.", "I was", ["was I", "I am always", "being I"]),
        ]
        rule = "In some adverbial clauses, repeated subject and be can be omitted when the meaning is clear."
    elif "形式宾语" in topic:
        examples = [
            ("I find ___ hard to learn grammar.", "it", ["this", "that", "there"]),
            ("She made ___ clear that she was busy.", "it", ["this", "that", "there"]),
            ("We think ___ important to read daily.", "it", ["there", "this", "that"]),
            ("He considered ___ impossible to finish today.", "it", ["there", "this", "that"]),
        ]
        rule = "Use it as a formal object when the real object is an infinitive phrase or a clause later in the sentence."
    elif "if 条件句与主句时态搭配" in topic:
        examples = [
            ("If I ___ rich, I would travel around the world.", "were", ["am", "was in formal rule", "will be"]),
            ("If he had studied harder, he ___ passed.", "would have", ["will have", "would", "had"]),
            ("If I saw him, I ___ tell him.", "would", ["will", "do", "am"]),
            ("If she had left earlier, she ___ the train.", "would have caught", ["will catch", "would catch", "had caught"]),
        ]
        rule = "In unreal conditionals, match the if-clause tense with would/could/might in the main clause."
    elif "suggest / insist" in topic:
        examples = [
            ("I suggest that he ___ earlier.", "leave", ["leaves", "left", "will leave"]),
            ("The teacher insisted that we ___ quiet.", "be", ["are", "were", "will be"]),
            ("She suggested that Tom ___ the doctor.", "see", ["sees", "saw", "will see"]),
            ("They insisted that the rule ___ followed.", "be", ["is", "was", "will be"]),
        ]
        rule = "After verbs like suggest and insist expressing a demand or recommendation, use that + subject + base verb."
    elif "wish 后" in topic:
        examples = [
            ("I wish I ___ taller.", "were", ["am", "will be", "have been"]),
            ("She wishes she ___ a car now.", "had", ["has", "will have", "has had"]),
            ("I wish I ___ him yesterday.", "had seen", ["saw", "see", "would see"]),
            ("He wishes he ___ fly.", "could", ["can", "will", "may"]),
        ]
        rule = "After wish, use past forms for unreal present wishes and past perfect for regrets about the past."
    elif "情态动词 + have done" in topic:
        return verb_form_questions(topic, seed)
    else:
        examples = [
            ("If I ___ you, I would say no.", "were", ["am", "was always", "will be"]),
            ("It is important ___ students read daily.", "that", ["which", "where", "who"]),
            ("Never ___ late again.", "will I be", ["I will be", "I am", "be I will"]),
            ("I find ___ useful to keep notes.", "it", ["there", "this", "that"]),
        ]
        rule = "Apply the special sentence pattern according to inversion, emphasis, ellipsis, formal it, or subjunctive meaning."
    return varied_questions(topic, examples, rule, seed)


def generic_questions(topic, seed):
    gloss = english_gloss(topic)
    examples = [
        ("Which English description matches this point? 哪个英文说明对应本知识点？", gloss, ["plural nouns only", "past-tense negatives only", "article use only"]),
        ("What should you focus on here? 本页主要考什么？", "the form and usage in context", ["spelling Chinese words", "translating every sentence literally", "ignoring the sentence meaning"]),
        ("Choose the best learning strategy. 选择最佳学习判断方式。", "check the sentence structure and grammar rule", ["guess from word length", "choose the longest answer", "ignore the subject"]),
        ("Which answer type is expected? 题型要求是什么？", "one best answer", ["two answers", "no answer", "free writing only"]),
    ]
    return varied_questions(topic, examples, f"Apply the rule for {english_gloss(topic)} in context.", seed)


def make_questions(topic, idx):
    if topic in FIRST_FIVE:
        return clean_question_instructions(FIRST_FIVE[topic])
    seed = int(hashlib.sha1(f"{idx}-{topic}".encode("utf-8")).hexdigest()[:8], 16)
    if idx == 67:
        return hospital_article_questions(seed)
    if idx >= 276 or any(k in topic for k in ["倒装", "强调句型", "省略", "形式宾语", "虚拟语气", "情态动词 + have done"]):
        return clean_question_instructions(special_questions(topic, seed))
    if any(k in topic for k in ["动词三单", "三单不规则", "非三单主语", "一般现在时否定", "一般现在时一般疑问句"]):
        return clean_question_instructions(verb_form_questions(topic, seed))
    if any(k in topic for k in ["复数", "结尾", "加 -s", "加 -es", "变 y", "变 f", "sheep", "trousers", "复合名词"]):
        return clean_question_instructions(plural_questions(topic, seed))
    if "所有格" in topic:
        return clean_question_instructions(possessive_questions(topic, seed))
    if any(k in topic for k in ["基数词", "序数词", "分数", "小数", "百分", "整点", "半点", "past 表达", "to 表达", "日期", "年代", "hundred", "thousand", "million", "1-100", "1st"]):
        return clean_question_instructions(number_questions(topic, seed))
    if any(k in topic for k in ["形容词", "副词", "-ly", "good-well", "enough 修饰"]):
        return clean_question_instructions(adjective_adverb_questions(topic, seed))
    if any(k in topic for k in ["冠词", " a ", " an ", "the", "零冠词", "in hospital"]):
        return clean_question_instructions(article_questions(topic, seed))
    if any(k in topic for k in ["比较级", "-er", "more", "than", "越来越", "越……越"]):
        return clean_question_instructions(comparison_questions(topic, seed))
    if any(k in topic for k in ["最高级", "-est", "most", "best", "worst"]):
        return clean_question_instructions(comparison_questions(topic, seed))
    if any(k in topic for k in ["介词", "in +", "on +", "at +", "since / for", "before / after", "during", "over / above", "between / among", "front of", "through / across", "by +", "with +"]):
        return clean_question_instructions(preposition_questions(topic, seed))
    if any(k in topic for k in ["从句", "指代人", "指代物", "限定性", "非限定性", "只用 that", "只用 which", "as 引导", "关系副词", "if / whether", "because", "though", "although", "unless", "so ... that", "so that"]):
        return clean_question_instructions(clause_questions(topic, seed))
    if any(k in topic for k in ["代词", "this", "that 单数", "these", "those", "some", "any", "many", "much", "few", "little", "both", "either", "neither", "all", "none", "each", "every", "one / ones", "something", "other", "what / which / who"]):
        return clean_question_instructions(pronoun_questions(topic, seed))
    if any(k in topic for k in ["动词", "三单", "一般现在", "现在进行", "一般过去", "过去进行", "一般将来", "现在完成", "过去完成", "将来进行", "将来完成", "doing", "done", "to do", "will", "going to", "shall", "been", "被动", "过去式", "否定", "疑问句", "情态", "must", "should", "need", "can / could", "may / might", "have done"]):
        return clean_question_instructions(verb_form_questions(topic, seed))
    if any(k in topic for k in ["识别", "S +", "句", "There be", "and", "but", "so 表", "or 表", "倒装", "强调", "省略", "虚拟", "形式"]):
        return clean_question_instructions(syntax_questions(topic, seed))
    return clean_question_instructions(generic_questions(topic, seed))


def wrap_text(text, size, max_width):
    lines = []
    line = ""
    for ch in text:
        candidate = line + ch
        if pdfmetrics.stringWidth(candidate, FONT, size) <= max_width or not line:
            line = candidate
        else:
            lines.append(line.rstrip())
            line = ch.lstrip()
    if line:
        lines.append(line.rstrip())
    return lines


def normalized_stem(stem):
    return re.sub(r"'.*?'|\d+|___|[A-D]\.\s*", "X", stem)


def draw_wrapped(c, text, x, y, size=9, leading=11.5, max_width=510, fill=colors.black):
    c.setFont(FONT, size)
    c.setFillColor(fill)
    for line in wrap_text(text, size, max_width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_header(c, item, no):
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont(FONT, 14.2)
    c.drawString(MARGIN_X, TOP, f"{no:03d}  {item['cn']}")
    c.setFont(FONT, 9.4)
    c.setFillColor(colors.HexColor("#475569"))
    path = " > ".join([p for p in [item["part"], item["section"], item["sub"]] if p])
    c.drawString(MARGIN_X, TOP - 16, path[:90])
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(MARGIN_X, TOP - 25, PAGE_W - MARGIN_X, TOP - 25)
    c.setFont(FONT, 8.2)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PAGE_W - MARGIN_X, 24, f"Complete English Grammar Worksheets | {no:03d}")


def draw_question_page(c, item, no, questions):
    draw_header(c, item, no)
    y = TOP - 42
    y = draw_wrapped(c, "中文概念：" + chinese_intro(item["cn"]), MARGIN_X, y, size=8.8, leading=11, max_width=PAGE_W - 2 * MARGIN_X, fill=colors.HexColor("#374151"))
    y = draw_wrapped(c, "English concept: " + english_intro(item["cn"]), MARGIN_X, y, size=8.4, leading=10.5, max_width=PAGE_W - 2 * MARGIN_X, fill=colors.HexColor("#374151"))
    y -= 4
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.roundRect(MARGIN_X, y - 10, PAGE_W - 2 * MARGIN_X, 15, 4, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#475569"))
    c.setFont(FONT, 8.1)
    c.drawString(MARGIN_X + 8, y - 5, "Choose the one best answer.")
    y -= 22
    for idx, (stem, options, _answer) in enumerate(questions, 1):
        y = draw_wrapped(c, f"{idx}. {stem}", MARGIN_X, y, size=8.55, leading=10.2, max_width=PAGE_W - 2 * MARGIN_X)
        for label, opt in zip(LETTERS, options):
            y = draw_wrapped(c, f"{label}. {opt}", MARGIN_X + 18, y, size=8.1, leading=9.5, max_width=PAGE_W - 2 * MARGIN_X - 24, fill=colors.HexColor("#111827"))
        y -= 1.2
    if y < BOTTOM:
        raise ValueError(f"Page overflow on topic {no:03d}: {item['cn']} y={y}")


def create_questions_pdf(topics, all_questions):
    c = canvas.Canvas(str(QUESTIONS_PDF), pagesize=A4)
    c.setTitle("完整语法题库 第001-286知识点 Worksheet")
    for no, item in enumerate(topics, 1):
        draw_question_page(c, item, no, all_questions[no - 1])
        c.showPage()
    c.save()


def create_answers_pdf(topics, all_questions):
    c = canvas.Canvas(str(ANSWERS_PDF), pagesize=A4)
    c.setTitle("完整语法题库 第001-286知识点 答案")
    page = 1

    def new_page():
        nonlocal page
        c.setFillColor(colors.HexColor("#1F2937"))
        c.setFont(FONT, 15.5)
        c.drawString(MARGIN_X, TOP, "完整语法题库答案")
        c.setFont(FONT, 9.6)
        c.setFillColor(colors.HexColor("#4B5563"))
        c.drawString(MARGIN_X, TOP - 18, "Answer Key | 第001-286知识点")
        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.line(MARGIN_X, TOP - 28, PAGE_W - MARGIN_X, TOP - 28)
        c.setFont(FONT, 8.2)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawRightString(PAGE_W - MARGIN_X, 24, f"Complete English Grammar Worksheets | Answer Key {page}")
        page += 1

    new_page()
    y = TOP - 54
    for no, (item, questions) in enumerate(zip(topics, all_questions), 1):
        answer_text = "答案：" + "   ".join(f"{i + 1}.{q[2]}" for i, q in enumerate(questions))
        needed = 12 + len(wrap_text(answer_text, 8.2, PAGE_W - 2 * MARGIN_X - 10)) * 10 + 9
        if y - needed < 48:
            c.showPage()
            new_page()
            y = TOP - 54
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont(FONT, 8.7)
        c.drawString(MARGIN_X, y, f"{no:03d} {item['cn'][:42]}")
        y -= 12
        y = draw_wrapped(c, answer_text, MARGIN_X + 10, y, size=8.2, leading=10.2, max_width=PAGE_W - 2 * MARGIN_X - 10, fill=colors.HexColor("#334155"))
        y -= 6
    c.save()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    topics = extract_topics()
    if len(topics) != 286:
        raise RuntimeError(f"Expected 286 topics, found {len(topics)}")
    all_questions = [make_blanks_visible(make_questions(item["cn"], i)) for i, item in enumerate(topics, 1)]
    bad = [(i + 1, topics[i]["cn"], len(qs)) for i, qs in enumerate(all_questions) if len(qs) != 10]
    if bad:
        raise RuntimeError(f"Every worksheet must have 10 questions, bad pages: {bad[:10]}")
    format_bad = []
    duplicate_stems = []
    fallback_options = []
    instruction_cn = []
    invisible_blanks = []
    unclear_article_options = []
    cn_instruction_patterns = ["补全", "选择", "下面", "哪个", "哪句", "哪组", "中文提示", "句子有误", "学完", "改正", "本页主要考", "题型要求"]
    for page_no, qs in enumerate(all_questions, 1):
        seen = set()
        for q_no, (stem, options, answer) in enumerate(qs, 1):
            if len(options) != 4 or len(set(options)) != 4 or answer not in LETTERS:
                format_bad.append((page_no, q_no, stem, options, answer))
            if any(pattern in stem for pattern in cn_instruction_patterns):
                instruction_cn.append((page_no, q_no, stem))
            if "___" in stem:
                invisible_blanks.append((page_no, q_no, stem))
            key = normalized_stem(stem)
            if key in seen:
                duplicate_stems.append((page_no, q_no, stem))
            seen.add(key)
            for option in options:
                if option.lower() == "no article":
                    unclear_article_options.append((page_no, q_no, option))
                if option.startswith(("not ", "incorrect form", "wrong sentence structure", "wrong word choice", "wrong grammar rule", "wrong context")):
                    fallback_options.append((page_no, q_no, option))
    if format_bad:
        raise RuntimeError(f"Every question must be A/B/C/D single choice with unique options: {format_bad[:5]}")
    if duplicate_stems:
        raise RuntimeError(f"Repeated question stems found: {duplicate_stems[:5]}")
    if fallback_options:
        raise RuntimeError(f"Mechanical fallback options found: {fallback_options[:5]}")
    if instruction_cn:
        raise RuntimeError(f"Chinese instruction text found in question stems: {instruction_cn[:5]}")
    if invisible_blanks:
        raise RuntimeError(f"Invisible underscore blanks found: {invisible_blanks[:5]}")
    if unclear_article_options:
        raise RuntimeError(f"Unclear no-article options found: {unclear_article_options[:5]}")
    create_questions_pdf(topics, all_questions)
    create_answers_pdf(topics, all_questions)
    print(QUESTIONS_PDF)
    print(ANSWERS_PDF)


if __name__ == "__main__":
    main()
