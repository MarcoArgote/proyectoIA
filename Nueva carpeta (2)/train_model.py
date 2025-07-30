from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, TrainingArguments, Trainer
import torch

# Cargar la versión 13 de Common Voice en español
print("Cargando dataset...")
dataset = load_dataset("mozilla-foundation/common_voice_13_0", "es", split="train[:1%]") # Usar 1% para ejemplo rápido
print("Ejemplo:", dataset[0])

# Preprocesamiento de datos (simplificado)
def speech_file_to_array_fn(batch):
    import soundfile as sf
    speech_array, sampling_rate = sf.read(batch["audio"]["path"])
    batch["speech"] = speech_array
    batch["sampling_rate"] = sampling_rate
    batch["target_text"] = batch["sentence"]
    return batch

dataset = dataset.map(speech_file_to_array_fn)

# Cargar modelo y procesador pre-entrenados
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")

def prepare_dataset(batch):
    inputs = processor(batch["speech"], sampling_rate=batch["sampling_rate"], return_tensors="pt", padding="longest")
    with processor.as_target_processor():
        labels = processor(batch["target_text"], return_tensors="pt", padding="longest").input_ids
    batch["input_values"] = inputs.input_values[0]
    batch["labels"] = labels[0]
    return batch

dataset = dataset.map(prepare_dataset)

# Argumentos de entrenamiento
training_args = TrainingArguments(
    output_dir="./wav2vec2-spanish-demo",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    logging_steps=10,
    save_steps=10,
    fp16=True,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

print("Entrenando modelo...")
trainer.train()
print("Entrenamiento finalizado.")
