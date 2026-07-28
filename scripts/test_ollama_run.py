from src.llm_augmentation import generate_paraphrases_with_ollama

questions = [
    "How do I reset my password?",
    "What is the capital of France?",
    "How can I improve model accuracy?",
]

for q in questions:
    try:
        paras = generate_paraphrases_with_ollama(q, model='qwen3.5', max_tokens=120, timeout=180)
        print('QUESTION:', q)
        print('PARAPHS:')
        for p in paras[:5]:
            print('-', p)
        print('-'*60)
    except Exception as e:
        print('ERROR for question:', q, '->', e)
