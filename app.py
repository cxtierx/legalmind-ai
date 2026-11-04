from pathlib import Path
import re

import streamlit as st


SOURCE_URL = "https://www.legislative.gov.in/static/uploads/2025/07/359f70a69695affb9d72f8393102bd2e.pdf"
SOURCE_PATH = Path(__file__).parent / "sources" / "Part_III_Fundamental_Rights_Articles_12-28.txt"
ARTICLE_HEADINGS = re.compile(r"(?m)^(21A|1[2-9]|2[0-8])\.\s+")


def load_constitution_articles():
    try:
        source_text = SOURCE_PATH.read_text(encoding="utf-8")
    except OSError:
        return {}

    matches = list(ARTICLE_HEADINGS.finditer(source_text))
    articles = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source_text)
        article_text = source_text[match.start():end]
        article_text = re.sub(r"(?m)^\d{1,3}\s+The Constitution of India\s*$", "", article_text)
        article_id = match.group(1)
        article_key = article_id if article_id.endswith("A") else int(article_id)
        articles[article_key] = article_text.strip()
    return articles


CONSTITUTION_ARTICLES = load_constitution_articles()
SEARCH_STOPWORDS = {
    "a", "about", "all", "an", "and", "are", "article", "art", "can", "does",
    "explain", "for", "from", "how", "in", "is", "me", "of", "on", "say", "tell",
    "the", "to", "what", "which", "who", "why",
}


def search_constitution_articles(question):
    terms = {
        term for term in re.findall(r"[a-z0-9]+", question.lower())
        if len(term) > 2 and term not in SEARCH_STOPWORDS
    }
    if not terms:
        return []

    results = []
    for article_number, article_text in CONSTITUTION_ARTICLES.items():
        matched_terms = [
            term for term in sorted(terms)
            if re.search(rf"\b{re.escape(term)}\w*\b", article_text, re.IGNORECASE)
        ]
        if matched_terms:
            results.append((article_number, matched_terms))

    results.sort(key=lambda item: (-len(item[1]), str(item[0])))
    if not results:
        return []
    best_score = len(results[0][1])
    return [item for item in results if len(item[1]) == best_score][:3]


DEMO_SUMMARIES = {
    14: (
        "**Sample answer (plain-language summary):** Article 14 says that the State "
        "must not deny any person equality before the law or equal protection of the "
        "laws in India. This is a summary of the constitutional text, not advice about "
        "how it applies to a situation."
    ),
    19: (
        "**Sample answer (plain-language summary):** Article 19 gives Indian citizens "
        "specified freedoms, including speech and expression, peaceful assembly without "
        "arms, forming associations, movement, residence, and choosing a profession or "
        "occupation. These freedoms are subject to the conditions and reasonable "
        "restrictions set out in Article 19 itself; they are not unlimited. This is a "
        "summary of the constitutional text, not advice about a particular situation."
    ),
    21: (
        "**Sample answer (plain-language summary):** Article 21 says that a person’s "
        "life or personal liberty cannot be taken away except according to a procedure "
        "established by law. This is a summary of the constitutional text only, not an "
        "explanation of how courts have interpreted it."
    ),
}


st.set_page_config(page_title="LegalMind AI", page_icon="⚖️", layout="centered")

st.title("⚖️ LegalMind AI")
st.caption("A learning prototype for India-focused legal research support")

st.warning(
    "Educational hackathon prototype only. It is not legal advice and does not "
    "replace a qualified Indian lawyer. Verify every point against current, "
    "authoritative sources and obtain human review."
)

st.subheader("Ask a research question")
st.caption("Search by Article number or a phrase, such as ‘freedom of speech’. Articles 14, 19, and 21 also have demo summaries.")
st.write(
    "This prototype matches words in the selected Constitution text. It does "
    "not use an external AI service or interpret legal meaning."
)
st.caption(
    "In a hosted demo, text you enter is sent to the hosting provider to run the app. "
    "Use only fictional or public text; do not enter private or confidential information."
)
question = st.text_area("Try a general question (do not enter private or identifying details).")
if st.button("Prepare question"):
    if question.strip():
        article_match = re.search(r"\b(?:article|art\.?)\s*(21A|1[2-9]|2[0-8])\b", question, re.IGNORECASE)
        if article_match:
            article_id = article_match.group(1).upper()
            article_number = article_id if article_id.endswith("A") else int(article_id)
            article_text = CONSTITUTION_ARTICLES.get(article_number)
            if article_text:
                if isinstance(article_number, int) and article_number in DEMO_SUMMARIES:
                    st.markdown(DEMO_SUMMARIES[article_number])
                    with st.expander(f"View source text for Article {article_number}"):
                        st.code(article_text)
                else:
                    st.info("AI is not connected, so this is the source text rather than an AI-generated explanation.")
                    st.code(article_text)
                st.markdown(
                    f"**Source:** [Constitution of India, Article {article_number} "
                    "(Legislative Department, as on 11 November 2025)]"
                    f"({SOURCE_URL})"
                )
                st.caption("This is educational information, not legal advice. Check the current text and seek qualified human review.")
            else:
                st.error("That Article could not be found in the local source file. Check the source set before relying on this app.")
        else:
            results = search_constitution_articles(question)
            if results:
                for article_number, matched_terms in results:
                    st.markdown(f"**Possible match: Article {article_number}**")
                    st.caption(f"Matched words: {', '.join(matched_terms)}")
                    with st.expander(f"View source text for Article {article_number}"):
                        st.code(CONSTITUTION_ARTICLES[article_number])
                    st.markdown(f"**Source:** [Constitution of India, Article {article_number} (Legislative Department, as on 11 November 2025)]({SOURCE_URL})")
            else:
                st.info(
                    "No matching words were found in the selected Articles. Try a "
                    "phrase from the Constitution or enter an Article number from 12 to 28."
                )
    else:
        st.info("Type a general question first.")

st.subheader("Sample document review")
st.caption("This basic scan does not use an AI service. In a hosted demo, text is sent to the hosting provider to run the app. Use fictional or public sample material only; do not enter client or confidential documents.")
st.write(
    "This first basic scan looks for date-like text, time periods, and sentences "
    "with common obligation words. It runs in this app and does not send the text "
    "to an AI service. It does not interpret the document or provide legal advice."
)
demo_contract_text = (
    "This fictional consulting agreement is between Client and Contractor. "
    "The Contractor shall deliver the final report by 15 January 2027. "
    "The Client must pay a fee of INR 10,000 within 30 days of receiving the invoice. "
    "Either party may terminate the agreement by giving 30 days' written notice. "
    "The Contractor shall keep all confidential information private."
)
st.caption("The built-in example is invented for demonstration only. It is not a real or usable contract.")
if st.button("Load fictional demo sample"):
    st.session_state["sample_document_text"] = demo_contract_text

sample_text = st.text_area(
    "Paste fictional sample text (optional)",
    placeholder="Example: Either party may end this fictional agreement by giving 30 days' written notice.",
    key="sample_document_text",
)
if st.button("Scan sample text"):
    if sample_text.strip():
        st.write("**Text you entered:**")
        st.code(sample_text)

        date_pattern = re.compile(
            r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
            r"\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|"
            r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|"
            r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|"
            r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
            r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
            r"Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4})\b",
            re.IGNORECASE,
        )
        period_pattern = re.compile(
            r"\b(?:within|no later than|at least|not less than)\s+\d+\s+"
            r"(?:business\s+|calendar\s+)?(?:days?|weeks?|months?|years?)\b|"
            r"\b\d+\s*[- ]days?\b|\b\d+\s+days?'(?:\s|$)",
            re.IGNORECASE,
        )
        obligation_pattern = re.compile(
            r"\b(?:shall|must|required to|responsible for|agrees to|"
            r"undertakes to|obligated to)\b",
            re.IGNORECASE,
        )
        topic_patterns = {
            "Payment": re.compile(r"\b(?:payment|pay|fee|invoice|price|billing)\b", re.IGNORECASE),
            "Ending or renewing the agreement": re.compile(
                r"\b(?:terminat\w*|end this agreement|notice|renew\w*)\b", re.IGNORECASE
            ),
            "Confidentiality": re.compile(
                r"\b(?:confidential\w*|non-disclosure|nda)\b", re.IGNORECASE
            ),
        }

        dates = list(dict.fromkeys(match.group(0) for match in date_pattern.finditer(sample_text)))
        periods = list(dict.fromkeys(match.group(0) for match in period_pattern.finditer(sample_text)))
        sentences = re.split(r"(?<=[.!?;])\s+|\n+", sample_text.strip())
        obligations = [sentence.strip() for sentence in sentences if obligation_pattern.search(sentence)]

        st.markdown("**Date-like text found**")
        if dates:
            for date in dates:
                st.write(f"- {date}")
        else:
            st.write("No date-like text detected by this simple scan.")

        st.markdown("**Time periods found**")
        if periods:
            for period in periods:
                st.write(f"- {period}")
        else:
            st.write("No time period detected by this simple scan.")

        st.markdown("**Common topic words found**")
        found_topics = {}
        for topic, pattern in topic_patterns.items():
            contexts = []
            for sentence in sentences:
                words = list(dict.fromkeys(match.group(0) for match in pattern.finditer(sentence)))
                if words:
                    contexts.append((sentence.strip(), words))
            if contexts:
                found_topics[topic] = contexts
        if found_topics:
            for topic, contexts in found_topics.items():
                st.markdown(f"**{topic}**")
                for sentence, words in contexts:
                    st.write(f"Matched words: {', '.join(words)}")
                    st.code(sentence)
        else:
            st.write("No matching topic words detected by this simple scan.")

        st.markdown("**Sentences with common obligation words**")
        if obligations:
            for sentence in obligations:
                st.write(f"- {sentence}")
        else:
            st.write("No matching obligation words detected by this simple scan.")

        st.caption(
            "This scan only matches a few text patterns. It can miss important "
            "information or flag irrelevant text; have a qualified person review "
            "the full document."
        )
    else:
        st.info("Add fictional sample text first.")

st.divider()
st.caption("Privacy first • Source citations required • Human review required")
