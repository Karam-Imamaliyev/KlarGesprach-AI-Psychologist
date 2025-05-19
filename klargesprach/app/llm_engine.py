from llama_cpp import Llama

# Model path
MODEL_PATH = "/home/karam/Desktop/KlarGespräch - AI Psychologist/klargesprach/model/Nous-Hermes-2-Mistral-7B-DPO-GGUF/Nous-Hermes-2-Mistral-7B-DPO.Q3_K_S.gguf"


# Load model globally (single instance)
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,         #  lowered it, the system runs more stable
    verbose=False,
    n_threads=4         # CPU'n kaçsa ona göre (4 çekirdek öneri)
)

def make_prompt(user_message):
    sys_msg = "You are a helpful psychologist."
    return (
        "<|im_start|>system\n"
        f"{sys_msg}\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{user_message.strip()}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

def query_llm(user_message: str, max_tokens: int = 256) -> str:
    prompt = make_prompt(user_message)
    output = llm(
        prompt,
        max_tokens=max_tokens,
        stop=["<|im_end|>", "<|im_start|>"],
        echo=False
    )
    # Return only the text part, not all JSON
    try:
        if isinstance(output, dict) and "choices" in output:
            return output["choices"][0]["text"].strip()
        return str(output)
    except Exception as e:
        return f"Error parsing LLM output: {e}"
