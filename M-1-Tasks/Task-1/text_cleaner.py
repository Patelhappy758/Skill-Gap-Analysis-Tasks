import re
from typing import List, Callable


def normalize_whitespace(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"\u00a0", " ", text)
    text = re.sub(r"\t+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_emails(text: str) -> str:
    return re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", " ", text)


def remove_urls(text: str) -> str:
    return re.sub(r"https?://\S+|www\.\S+", " ", text)


def dehyphenate_line_breaks(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"-\n\s*", "", text)


def basic_clean(text: str) -> str:
    transformations: List[Callable[[str], str]] = [
        dehyphenate_line_breaks,
        remove_urls,
        remove_emails,
        normalize_whitespace,
    ]
    cleaned_text = text or ""
    for transform in transformations:
        cleaned_text = transform(cleaned_text)
    return cleaned_text


if __name__ == "__main__":
    sample = (
        "Email: john.doe@example.com\nLinkedIn: https://linkedin.com/in/john\n"
        "Machine-\nlearning, data\tScience\n\n  Skills: Python, SQL"
    )
    print(basic_clean(sample))
