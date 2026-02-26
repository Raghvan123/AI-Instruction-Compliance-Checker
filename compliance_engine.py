import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load Model (Global)

model = SentenceTransformer('all-MiniLM-L6-v2')

# SEMANTIC SIMILARITY

def compute_semantic_similarity(instruction, response):
    embeddings = model.encode([instruction, response])
    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]
    return float(similarity)

# AUXILIARY METRICS

def compute_keyword_coverage(instruction, response):
    instruction_words = set(instruction.lower().split())
    response_words = set(response.lower().split())

    if not instruction_words:
        return 0.0

    overlap = instruction_words.intersection(response_words)
    return len(overlap) / len(instruction_words)


def compute_length_adequacy(instruction, response):
    inst_len = len(instruction.split())
    resp_len = len(response.split())

    if inst_len == 0:
        return 0.0

    return min(resp_len / inst_len, 1.0)


def compute_auxiliary_score(instruction, response):
    keyword_score = compute_keyword_coverage(instruction, response)
    length_score = compute_length_adequacy(instruction, response)

    return (keyword_score + length_score) / 2

# DYNAMIC CONSTRAINT ENGINE

def extract_constraints(instruction):
    constraints = {}
    instruction = instruction.lower()

    # Count detection
    number_match = re.search(r'\b(one|two|three|four|five|\d+)\b', instruction)
    if number_match:
        word_to_number = {
            "one": 1, "two": 2, "three": 3,
            "four": 4, "five": 5
        }

        value = number_match.group()
        constraints["count"] = word_to_number.get(
            value, int(value) if value.isdigit() else None
        )

    # Format detection
    if "bullet" in instruction:
        constraints["format"] = "bullet"

    if "paragraph" in instruction:
        constraints["format"] = "paragraph"

    # Starts with detection
    start_match = re.search(r'start with\s+"?([a-z])"?', instruction)
    if start_match:
        constraints["starts_with"] = start_match.group(1).upper()

    # Word count detection
    word_count_match = re.search(r'(\d+)\s+words?', instruction)
    if word_count_match:
        constraints["word_count"] = int(word_count_match.group(1))

    return constraints


def check_bullet_format(response):
    lines = response.split("\n")
    bullet_lines = [
        line for line in lines
        if line.strip().startswith(("•", "-", "*"))
    ]
    return 1.0 if len(bullet_lines) > 0 else 0.0


def extract_list_items(response):
    lines = response.split("\n")
    items = [
        line.strip("•-* ").strip()
        for line in lines
        if line.strip()
    ]
    return items


def evaluate_constraints(instruction, response):
    constraints = extract_constraints(instruction)
    scores = []

    items = extract_list_items(response)

    # Count check
    if "count" in constraints and constraints["count"] is not None:
        scores.append(1.0 if len(items) == constraints["count"] else 0.0)

    # Format check
    if constraints.get("format") == "bullet":
        scores.append(check_bullet_format(response))

    # Starts with check
    if "starts_with" in constraints:
        if items:
            correct = sum(
                1 for item in items
                if item.upper().startswith(constraints["starts_with"])
            )
            scores.append(correct / len(items))
        else:
            scores.append(0.0)

    # Word count check
    if "word_count" in constraints:
        word_count = len(response.split())
        scores.append(
            1.0 if word_count >= constraints["word_count"] else 0.0
        )

    if not scores:
        return 1.0

    return sum(scores) / len(scores)

# FINAL SCORE

def compute_final_score(instruction, response):

    semantic_score = compute_semantic_similarity(instruction, response)
    auxiliary_score = compute_auxiliary_score(instruction, response)
    constraint_score = evaluate_constraints(instruction, response)

    final = (
        0.4 * semantic_score +
        0.3 * auxiliary_score +
        0.3 * constraint_score
    )

    results = {
        "semantic": round(semantic_score, 3),
        "auxiliary": round(auxiliary_score, 3),
        "constraint": round(constraint_score, 3),
        "final_score": round(final * 100, 2)
    }

    grade, explanation = generate_explanation(results)

    results["grade"] = grade
    results["explanation"] = explanation

    return results

def generate_explanation(results):
    explanation = []

    semantic = results["semantic"]
    auxiliary = results["auxiliary"]
    constraint = results["constraint"]
    final_score = results["final_score"]

    # Grade classification
    if final_score >= 85:
        grade = "Excellent Compliance"
    elif final_score >= 70:
        grade = "Good Compliance"
    elif final_score >= 50:
        grade = "Moderate Compliance"
    else:
        grade = "Poor Compliance"

    # Semantic explanation
    if semantic > 0.75:
        explanation.append("Strong semantic similarity between instruction and response.")
    elif semantic > 0.5:
        explanation.append("Moderate semantic similarity detected.")
    else:
        explanation.append("Low semantic similarity. Response meaning may not align closely with instruction.")

    # Auxiliary explanation
    if auxiliary > 0.7:
        explanation.append("Good keyword coverage and appropriate response length.")
    elif auxiliary > 0.4:
        explanation.append("Partial keyword overlap or moderate length adequacy.")
    else:
        explanation.append("Low keyword overlap and/or insufficient length adequacy.")

    # Constraint explanation
    if constraint == 1.0:
        explanation.append("All structural constraints are satisfied.")
    elif constraint >= 0.5:
        explanation.append("Some structural constraints are partially satisfied.")
    else:
        explanation.append("Structural constraints are not satisfied.")

    return grade, explanation