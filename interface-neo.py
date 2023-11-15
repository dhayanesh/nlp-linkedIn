from flask import Flask, request, render_template
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

app = Flask(__name__)

model = GPTNeoForCausalLM.from_pretrained("./trained_model_neo")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        generated_post = generate_post(user_input)

        return render_template('index.html', generated_post=generated_post)
    return render_template('index.html')

def generate_post(user_input):
    inputs = tokenizer.encode(user_input, return_tensors='pt')

    outputs = model.generate(
        inputs,
        max_length=500,
        num_return_sequences=1,
        temperature=0.7,
        top_k=200,
        top_p=0.95,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == '__main__':
    app.run(debug=True)
