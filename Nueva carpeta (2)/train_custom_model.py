from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, TrainingArguments, Trainer
import torch
import soundfile as sf

# 1. Importar el dataset Common Voice español
print("Importando dataset...")
dataset = load_dataset("mozilla-foundation/common_voice_13_0", "es", split="train[:1%]") # Usar 1% para ejemplo rápido
print("Ejemplo:", dataset[0])

# 2. Preprocesar los datos

def speech_file_to_array_fn(batch):
    speech_array, sampling_rate = sf.read(batch["audio"]["path"])
    batch["speech"] = speech_array
    batch["sampling_rate"] = sampling_rate
    batch["target_text"] = batch["sentence"]
    return batch

dataset = dataset.map(speech_file_to_array_fn)

# 3. Cargar modelo y procesador base
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-spanish")

# 4. Preparar datos para entrenamiento

def prepare_dataset(batch):
    inputs = processor(batch["speech"], sampling_rate=batch["sampling_rate"], return_tensors="pt", padding="longest")
    with processor.as_target_processor():
        labels = processor(batch["target_text"], return_tensors="pt", padding="longest").input_ids
    batch["input_values"] = inputs.input_values[0]
    batch["labels"] = labels[0]
    return batch

dataset = dataset.map(prepare_dataset)

# 5. Argumentos de entrenamiento
training_args = TrainingArguments(
    output_dir="./wav2vec2-spanish-custom",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    logging_steps=10,
    save_steps=10,
    fp16=True,
)

# 6. Entrenador
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

print("Entrenando modelo...")
trainer.train()
print("Entrenamiento finalizado.")

# 7. Guardar modelo entrenado
model.save_pretrained("./wav2vec2-spanish-custom")
processor.save_pretrained("./wav2vec2-spanish-custom")
print("Modelo guardado en ./wav2vec2-spanish-custom")
