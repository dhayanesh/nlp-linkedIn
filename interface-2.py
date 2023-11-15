from flask import Flask, request, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

model = GPT2LMHeadModel.from_pretrained('./trained_model')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

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
    max_length=200,
    num_return_sequences=1,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == '__main__':
    app.run(debug=True)
