from src.llm_augmentation import generate_paraphrases_with_ollama

question = 'How do I reset my password?'
result = generate_paraphrases_with_ollama(question, model='qwen3.5', max_tokens=120, timeout=180)
print(question)
for item in result:
    print('-', item)
