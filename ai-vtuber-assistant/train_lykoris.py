import os
os.environ["UNSLOTH_COMPILE_DISABLE"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32"

import torch
import torch._inductor.config

# --- DER ERWEITERTE HACKER-WORKAROUND ---
for i in range(1, 8):
    if not hasattr(torch, f"int{i}"):
        setattr(torch, f"int{i}", torch.int8)
# ----------------------------------------

from unsloth import FastLanguageModel

# --- DER NEUE BOSS-HACK: WIR SCHALTEN DIE UNSLOTH-PANIK AB ---
import unsloth_zoo.fused_losses.cross_entropy_loss
# Wir zwingen Unsloth, die Berechnung in 4 winzige Häppchen zu teilen, anstatt den Speicher zu prüfen!
unsloth_zoo.fused_losses.cross_entropy_loss.get_chunk_size = lambda *args, **kwargs: 4
# -------------------------------------------------------------

from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth.chat_templates import get_chat_template
import gc

# 1. Grundeinstellungen
max_seq_length = 512 # Wieder auf 512, damit deine 350 Wörter nicht abgeschnitten werden!
dtype = None 
load_in_4bit = True 

print("Lade das Basismodell...")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

print("Modell geladen! Pflanze jetzt das LoRA-Lernmodul ein...")

model = FastLanguageModel.get_peft_model(
    model,
    r = 8,
    target_modules = ["q_proj", "v_proj"],
    lora_alpha = 8,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth", 
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

print("Bereite die Trainingsdaten vor...")

tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3",
)

dataset = load_dataset("json", data_files="lykoris_training.jsonl", split="train")

def formatting_prompts_func(examples):
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False) for convo in convos]
    return { "text" : texts, }

dataset = dataset.map(formatting_prompts_func, batched = True)

print("Räume den Speicher auf, bevor wir starten...")
gc.collect()
torch.cuda.empty_cache()

print("Starte das Training! Lykoris lernt jetzt...")

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8,
        warmup_steps = 5,
        num_train_epochs = 3, 
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "paged_adamw_8bit", 
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "lykoris_checkpoints",
    ),
)

trainer.train()

print("Training abgeschlossen! Speichere Lykoris ab...")
model.save_pretrained("lykoris_fertig")
tokenizer.save_pretrained("lykoris_fertig")
print("Herzlichen Glückwunsch! Deine eigene KI ist geboren.")