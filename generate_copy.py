from transformers import pipeline

# Initialize the text-generation pipeline with GPT-2
generator = pipeline('text-generation', model='gpt2')

def generate_marketing_copy(prompt):
    outputs = generator(prompt, max_length=100, num_return_sequences=1)
    return outputs[0]['generated_text']

if __name__ == "__main__":
    prompt = "Write a marketing copy for an organic energy drink with an excited tone targeting college students:"
    copy = generate_marketing_copy(prompt)
    print("\nGenerated Marketing Copy:\n")
    print(copy)
