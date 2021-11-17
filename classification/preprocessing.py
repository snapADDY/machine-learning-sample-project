from typing import Optional

from bs4 import BeautifulSoup


def extract_text(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, features="html.parser")
    if body := soup.find("body"):
        return body.text
