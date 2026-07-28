# Annotation guidelines

## Objective

Label each question pair according to the semantic relationship between the two questions.

## Label definitions

- `exact_duplicate`
  - The two questions express the same intent and can be answered by the same response.
  - Example: "How do I reset my password?" / "What is the process for resetting a password?"

- `paraphrase`
  - The two questions express the same underlying meaning with different wording.
  - Example: "What is the best way to lose weight?" / "How can I reduce my body fat?"

- `related_but_not_duplicate`
  - The pair is on the same topic or domain but asks a different specific question.
  - Example: "How to bake a cake?" / "What ingredients does a cake need?"

- `partial_overlap`
  - The questions share some topic, entity, or context, but the intents are only partially aligned.
  - Example: "Can I travel with my laptop?" / "What are the security measures for laptops at airports?"

- `unrelated`
  - The questions are about different topics or intents.
  - Example: "How do I change a tire?" / "What is the capital of France?"

## Annotation instructions

1. **Focus on intent first**
   - Choose the label that best matches the underlying user goal, not just the shared words.

2. **Use examples as guides**
   - If the meaning is the same, prefer `exact_duplicate` or `paraphrase`.
   - If the topic is shared but the question is different, use `related_but_not_duplicate`.
   - If the overlap is weak or incidental, use `partial_overlap`.

3. **Be conservative on ambiguity**
   - When unsure, prefer the lower equivalence label (e.g. `partial_overlap` instead of `paraphrase`).

4. **Label consistency**
   - Keep the same label for similar pairs throughout the dataset.
   - If multiple annotators are involved, align on the examples before starting full annotation.

## Annotation fields

The `gold_subset_2000.csv` file includes:

- `id`
- `question1`
- `question2`
- `is_duplicate`
- `semantic_label`
- `label_reason`
- `source_dataset`
- `split`
- `annotation_status`

Annotators should update `annotation_status` to `confirmed` or `corrected` after review.
