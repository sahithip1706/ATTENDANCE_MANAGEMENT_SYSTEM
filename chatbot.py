from transformers import AutoTokenizer,AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft /DialoGPT-medium")
def generate_response(user_input):
    input_ids = tokenizer.encode(user_input +tokenizer.eos_token,return_tensors="pt")
    chat_history_ids = model.generate(input_ids,max_length=1000,pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:,input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye", "exit"]:
        print("Chatbot: Goodbye!")
        break
    response = generate_response(user_input)
    print("Chatbot:", response)