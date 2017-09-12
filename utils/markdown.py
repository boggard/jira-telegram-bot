def markdown_prepare(text: str):
    if text is None:
        return ""
    return text.replace("*", "\*")
