from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


QUESTIONS_PDF = "英语语法题库PDF/第001-005知识点_题目_名词分类与规则复数-s.pdf"
ANSWERS_PDF = "英语语法题库PDF/第001-005知识点_答案_名词分类与规则复数-s.pdf"


FONT = "Songti"
pdfmetrics.registerFont(TTFont(FONT, "/System/Library/Fonts/Supplemental/Songti.ttc", subfontIndex=0))

PAGE_W, PAGE_H = A4
MARGIN_X = 42
TOP = PAGE_H - 40
BOTTOM = 42


TOPICS = [
    {
        "no": "001",
        "title_cn": "普通名词与专有名词识别",
        "title_en": "Common Nouns vs. Proper Nouns",
        "focus": "判断名词是否表示一般类别，或特定的人名、地名、机构名等。",
        "questions": [
            ("Which word is a proper noun? 下面哪一个是专有名词？", ["city", "teacher", "London", "river"], "C"),
            ("In the sentence 'Emma reads a book.', which word is a proper noun? 句中哪个词是专有名词？", ["Emma", "reads", "book", "a"], "A"),
            ("Which word is a common noun? 下面哪一个是普通名词？", ["China", "Monday", "school", "Tom"], "C"),
            ("Choose the proper noun. 选择专有名词。", ["mountain", "Mr. Smith", "restaurant", "student"], "B"),
            ("In 'We visited the museum in Paris.', which word is a proper noun? 哪个词是专有名词？", ["visited", "museum", "Paris", "the"], "C"),
            ("Which pair has one common noun and one proper noun? 哪组包含一个普通名词和一个专有名词？", ["apple / banana", "Sarah / Alice", "country / Japan", "quick / slowly"], "C"),
            ("Which sentence uses a proper noun correctly? 哪句正确使用了专有名词？", ["My friend is a doctor.", "We live near the river.", "David plays tennis.", "A cat is sleeping."], "C"),
            ("Which word usually needs a capital letter because it is a proper noun? 哪个词通常因是专有名词而首字母大写？", ["january", "desk", "woman", "flower"], "A"),
            ("In 'The Nile is a long river.', which word is a proper noun? 哪个词是专有名词？", ["Nile", "long", "river", "The"], "A"),
            ("Which option contains only common nouns? 哪个选项全是普通名词？", ["Beijing, city", "doctor, classroom", "Anna, girl", "Sunday, day"], "B"),
        ],
    },
    {
        "no": "002",
        "title_cn": "可数名词、不可数名词识别",
        "title_en": "Countable Nouns vs. Uncountable Nouns",
        "focus": "判断名词能否直接计数，以及是否常用 a/an、many 或 much 搭配。",
        "questions": [
            ("Which noun is countable? 哪个名词是可数名词？", ["water", "rice", "apple", "music"], "C"),
            ("Which noun is uncountable? 哪个名词是不可数名词？", ["chair", "idea", "furniture", "student"], "C"),
            ("Choose the correct phrase. 选择正确短语。", ["many water", "much water", "a water", "two water"], "B"),
            ("Which phrase is correct? 哪个短语正确？", ["an advice", "two advices", "some advice", "many advice"], "C"),
            ("Which noun can normally take a/an? 哪个名词通常可以直接加 a/an？", ["information", "bread", "orange", "homework"], "C"),
            ("Complete: There are three ___ on the table. 补全句子。", ["cup", "cups", "water", "rice"], "B"),
            ("Complete: I need some ___. 补全句子。", ["informations", "information", "an information", "many information"], "B"),
            ("Which set contains only uncountable nouns? 哪组全是不可数名词？", ["milk, sugar, air", "book, pen, desk", "child, dog, song", "city, road, car"], "A"),
            ("Which question is correct? 哪个问句正确？", ["How many money do you have?", "How much money do you have?", "How many milk do you need?", "How much apples are there?"], "B"),
            ("Which noun is countable in ordinary use? 哪个名词在通常用法中可数？", ["news", "homework", "bottle", "traffic"], "C"),
        ],
    },
    {
        "no": "003",
        "title_cn": "集合名词 family / class 等用法",
        "title_en": "Collective Nouns: family, class, team",
        "focus": "集合名词表示一个群体；看作整体时常用单数，看作成员时可强调复数意义。",
        "questions": [
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
    },
    {
        "no": "004",
        "title_cn": "物质名词、抽象名词识别",
        "title_en": "Material Nouns vs. Abstract Nouns",
        "focus": "物质名词表示材料或物质；抽象名词表示品质、状态、情感或概念。",
        "questions": [
            ("Which is a material noun? 哪个是物质名词？", ["gold", "kindness", "idea", "beauty"], "A"),
            ("Which is an abstract noun? 哪个是抽象名词？", ["wood", "milk", "freedom", "cotton"], "C"),
            ("In 'The ring is made of silver.', what type of noun is 'silver'? silver 属于哪类名词？", ["proper noun", "material noun", "collective noun", "verb"], "B"),
            ("In 'Honesty is important.', what type of noun is 'honesty'? honesty 属于哪类名词？", ["abstract noun", "material noun", "proper noun", "countable place noun"], "A"),
            ("Which pair contains one material noun and one abstract noun? 哪组包含一个物质名词和一个抽象名词？", ["iron / courage", "teacher / student", "London / China", "family / class"], "A"),
            ("Which word names a feeling or quality, not a physical material? 哪个词表示情感或品质，而不是物质？", ["plastic", "anger", "water", "wool"], "B"),
            ("Which word names a substance? 哪个词表示一种物质？", ["happiness", "sand", "truth", "peace"], "B"),
            ("Choose the abstract noun. 选择抽象名词。", ["glass", "patience", "paper", "steel"], "B"),
            ("Choose the material noun. 选择物质名词。", ["love", "oil", "wisdom", "success"], "B"),
            ("Which sentence contains an abstract noun? 哪句含有抽象名词？", ["The table is made of wood.", "She showed great courage.", "The bottle is full of water.", "They bought cotton shirts."], "B"),
        ],
    },
    {
        "no": "005",
        "title_cn": "可数名词单数变复数：一般情况直接加 -s",
        "title_en": "Regular Plurals: Add -s",
        "focus": "多数可数名词变复数时，直接在词尾加 -s。",
        "questions": [
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
    },
]


def wrap_text(text, size, max_width):
    words = []
    current = ""
    for ch in text:
        if ord(ch) < 128 and ch == " ":
            words.append(ch)
        else:
            words.append(ch)
    lines = []
    line = ""
    for token in words:
        candidate = line + token
        if pdfmetrics.stringWidth(candidate, FONT, size) <= max_width or not line:
            line = candidate
        else:
            lines.append(line.rstrip())
            line = token.lstrip()
    if line:
        lines.append(line.rstrip())
    return lines


def draw_wrapped(c, text, x, y, size=10, leading=13, max_width=510, fill=colors.black):
    c.setFont(FONT, size)
    c.setFillColor(fill)
    lines = wrap_text(text, size, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_header(c, topic, page_no):
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont(FONT, 15)
    c.drawString(MARGIN_X, TOP, f"{topic['no']}  {topic['title_cn']}")
    c.setFont(FONT, 10.5)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.drawString(MARGIN_X, TOP - 18, topic["title_en"])
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(MARGIN_X, TOP - 28, PAGE_W - MARGIN_X, TOP - 28)
    c.setFont(FONT, 8.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PAGE_W - MARGIN_X, 24, f"English Grammar MCQ | Page {page_no}")


def draw_question_page(c, topic, page_no):
    draw_header(c, topic, page_no)
    y = TOP - 46
    y = draw_wrapped(c, f"考点 Focus: {topic['focus']}", MARGIN_X, y, size=9.2, leading=12, max_width=PAGE_W - 2 * MARGIN_X, fill=colors.HexColor("#374151"))
    y -= 4
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.roundRect(MARGIN_X, y - 10, PAGE_W - 2 * MARGIN_X, 16, 4, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#475569"))
    c.setFont(FONT, 8.5)
    c.drawString(MARGIN_X + 8, y - 5, "每题只有一个最佳答案。Choose the one best answer.")
    y -= 24

    for idx, (stem, options, _answer) in enumerate(topic["questions"], 1):
        if y < BOTTOM + 62:
            raise ValueError(f"Page overflow in topic {topic['no']} question {idx}")
        y = draw_wrapped(c, f"{idx}. {stem}", MARGIN_X, y, size=9.3, leading=12, max_width=PAGE_W - 2 * MARGIN_X)
        y -= 1
        for label, opt in zip(["A", "B", "C", "D"], options):
            y = draw_wrapped(c, f"{label}. {opt}", MARGIN_X + 18, y, size=8.9, leading=11, max_width=PAGE_W - 2 * MARGIN_X - 24, fill=colors.HexColor("#111827"))
        y -= 3


def create_questions_pdf():
    c = canvas.Canvas(QUESTIONS_PDF, pagesize=A4)
    c.setTitle("英语语法单选题 第001-005知识点")
    for page_no, topic in enumerate(TOPICS, 1):
        draw_question_page(c, topic, page_no)
        c.showPage()
    c.save()


def create_answers_pdf():
    c = canvas.Canvas(ANSWERS_PDF, pagesize=A4)
    c.setTitle("英语语法答案 第001-005知识点")
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont(FONT, 16)
    c.drawString(MARGIN_X, TOP, "英语语法单选题答案")
    c.setFont(FONT, 10.5)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.drawString(MARGIN_X, TOP - 20, "Answer Key | 第001-005知识点")
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(MARGIN_X, TOP - 31, PAGE_W - MARGIN_X, TOP - 31)

    y = TOP - 58
    col_x = [MARGIN_X, 200, 358]
    row_h = 132
    for i, topic in enumerate(TOPICS):
        x = col_x[i % 3]
        if i == 3:
            y = TOP - 58 - row_h
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(x - 8, y - 103, 145, 116, 5, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont(FONT, 10)
        c.drawString(x, y, f"{topic['no']} {topic['title_cn']}")
        c.setFont(FONT, 8.2)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(x, y - 13, topic["title_en"][:35])
        answers = [q[2] for q in topic["questions"]]
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont(FONT, 9.4)
        for n in range(10):
            row = n % 5
            subcol = n // 5
            c.drawString(x + subcol * 66, y - 34 - row * 13, f"{n + 1}. {answers[n]}")

    notes_y = 255
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont(FONT, 11.5)
    c.drawString(MARGIN_X, notes_y, "简要提示")
    c.setFont(FONT, 9)
    c.setFillColor(colors.HexColor("#374151"))
    notes = [
        "001: 专有名词指具体的人名、地名、机构名、月份等，通常首字母大写。",
        "002: 可数名词可直接计数并有复数形式；不可数名词常与 much / some 搭配。",
        "003: 集合名词表示群体；整体意义常用单数，强调成员时可用复数意义。",
        "004: 物质名词表示材料或物质；抽象名词表示品质、状态、情感或概念。",
        "005: 一般可数名词变复数，直接在词尾加 -s，如 book-books。",
    ]
    y = notes_y - 20
    for note in notes:
        y = draw_wrapped(c, note, MARGIN_X, y, size=9, leading=13, max_width=PAGE_W - 2 * MARGIN_X, fill=colors.HexColor("#374151"))

    c.setFont(FONT, 8.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawRightString(PAGE_W - MARGIN_X, 24, "English Grammar MCQ | Answer Key")
    c.save()


if __name__ == "__main__":
    create_questions_pdf()
    create_answers_pdf()
    print(QUESTIONS_PDF)
    print(ANSWERS_PDF)
