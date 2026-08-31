import json
from pathlib import Path

import generate_complete_grammar_workbook as grammar


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "data.js"


def main():
    topics = grammar.extract_topics()
    payload = []
    for number, item in enumerate(topics, 1):
        questions = grammar.make_blanks_visible(grammar.make_questions(item["cn"], number))
        payload.append(
            {
                "number": number,
                "title": item["cn"],
                "part": item["part"],
                "section": item["section"],
                "subsection": item["sub"],
                "questions": [
                    {
                        "stem": stem,
                        "options": options,
                        "answer": answer,
                    }
                    for stem, options, answer in questions
                ],
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data = {"topicCount": len(payload), "questionCount": sum(len(x["questions"]) for x in payload), "topics": payload}
    OUTPUT.write_text("window.GRAMMAR_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()

