text = """
Salom
Origin City: Gayrat Sultonov
How are you
"""


def finding_text(original, finding_text_original) -> int:
    lower_text = original.lower()
    lower_finding_text = finding_text_original.lower()
    finding_text_len = len(finding_text_original)
    num_index = lower_text.find(lower_finding_text)
    if num_index != -1:
        end_index = finding_text_len + num_index
        return end_index
    return num_index


def get_value(original, finding_text_original):
    num_index = finding_text(original, finding_text_original)
    if num_index == -1:
        return None
    start_line_index = original.rfind('\n', 0, num_index) + 1

    # Find the end of the line containing the found text
    end_line_index = original.find('\n', num_index)
    if end_line_index == -1:
        end_line_index = len(original)

    # Extract the line containing the found text
    line = original[start_line_index:end_line_index]

    # Extract the substring starting from num_index to the end of the line
    result = line[num_index - start_line_index:]

    return result.strip()


finding_text_original = "origin city:"
value = get_value(text, finding_text_original)
