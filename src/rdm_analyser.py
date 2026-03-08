import config
import json
import os
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- 1. MODEL LOADING ---
print("--- STEP 1: Initialization ---")
print(f"[INFO] Loading model: {config.MODEL_ID}")

tokenizer = AutoTokenizer.from_pretrained(
    pretrained_model_name_or_path=config.MODEL_ID,
    trust_remote_code=config.TRUST_REMOTE_CODE
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id

model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=config.MODEL_ID,
    dtype=torch.float32,
    device_map=config.DEVICE_MAP,
    trust_remote_code=config.TRUST_REMOTE_CODE,
    low_cpu_mem_usage=True,
)

print("[SUCCESS] Model loaded into memory.")

# --- 2. ANALYSIS FUNCTION ---
def is_a_README(readme):
    readme_content = readme[:1200] if readme else ""
    
    prompt = f"""
    Analyze the following README text. 
    Is this project strictly a "Digital Twin" (simulation + bidirectional connection)?
    Answer ONLY with "YES" or "NO".
    
    README:
    {readme_content}
    
    Answer:
    """
    
    messages = [{'role': 'user', 'content': prompt}]
    
    # input_ids is a direct Tensor here
    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors='pt',
        add_generation_prompt=True
    ).to(model.device)
    
    # FIX: Manually creating the mask (filled with 1s)
    attention_mask = torch.ones_like(input_ids)
    
    with torch.no_grad():
        output = model.generate(
            input_ids,
            attention_mask=attention_mask, # Passing the created mask
            max_new_tokens=10, 
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    raw_answer = tokenizer.decode(
        output[0][input_ids.shape[-1]:],
        skip_special_tokens=True,
    ).strip().lower()
    
    print(f"   (AI output: '{raw_answer}')", end=" ")

    # Evaluating the answer (kept French keywords in condition just in case, per original logic)
    if "oui" in raw_answer or "yes" in raw_answer:
        return True
    elif "non" in raw_answer or "no" in raw_answer:
        return False
    return None

# --- 3. DATA PROCESSING ---
def process_dataset():
    print("--- STEP 2: Data processing ---")
    input_file = "data/dataset_final.jsonl"
    output_csv = "data/dataset_analyzed_local.csv"
    
    if not os.path.exists(input_file):
        print(f"[ERROR] The file {input_file} was not found.")
        return

    analyzed_data = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"[INFO] Number of projects to analyze: {len(lines)}")
    
    for i, line in enumerate(lines):
        try:
            repo = json.loads(line)
            print(f"[{i+1}/{len(lines)}] {repo['name']} ...", end=" ", flush=True)
            
            is_valid = is_a_README(repo.get('readme', ''))
            
            if is_valid is True:
                print("-> YES")
            elif is_valid is False:
                print("-> NO")
            else:
                print("-> UNCERTAIN")
            
            analyzed_data.append({
                "name": repo['name'],
                "url": repo['url'],
                "search_query": repo.get('search_query', ''),
                "is_digital_twin": is_valid,
                "description": repo.get('description', '')
            })
            
        except Exception as e:
            print(f"\n[ERROR] {e}")

    if analyzed_data:
        df = pd.DataFrame(analyzed_data)
        df.sort_values(by="is_digital_twin", ascending=False, inplace=True)
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"\n[SUCCESS] Results saved to: {output_csv}")

if __name__ == "__main__":
    process_dataset()