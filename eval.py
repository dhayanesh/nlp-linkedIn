from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./trained_model')
tokenizer = GPT2Tokenizer.from_pretrained('./trained_model')

# Sample prompt
prompt = "Can you give advice on how to stay motivated and overcome challenges when pursuing personal goals?"

# Generate text
inputs = tokenizer.encode(prompt, return_tensors='pt')
outputs = model.generate(inputs, max_length=50)
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Reference text (an original post)
reference = ["""Whenever you find yourself slipping, remember everyone who underestimated you.

When you harness negative feelings and turn them into positive energy, you're going to get significantly further.

The Tom Brady effect, if you will.

So, when you're feeling down in the dumps or struggling to continue moving your business forward, do three things:

1. Reflect on Your 'Why': 

Go back to the reason you started. Your core motivation is your anchor - it can pull you back from the brink and give you a renewed sense of purpose.

2. Seek Out Constructive Feedback: 

Reach out to a mentor, a peer, or your audience. Constructive criticism can be a powerful catalyst for growth.

3. Set a Small, Achievable Goal: 

Sometimes, the big picture can be overwhelming. Break it down. Set a small, achievable goal and give it your all. 

Remember, setbacks are not failures, they're just opportunities to come back stronger. 

Push, grow, and let the doubt fuel your drive to succeed.
"""]

# Apply smoothing function
smoothie = SmoothingFunction().method4

# Calculate BLEU score with smoothing
score = sentence_bleu([reference[0].split()], generated_text.split(), smoothing_function=smoothie)
print(score)
