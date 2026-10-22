"""Fine-tune an ImageNet ResNet-18 to classify LGG MRI slices as tumour / no tumour."""
import json
import os

import numpy as np
import torch
import torch.nn.functional as F

from common import (CHECKPOINT, DEVICE, RESULTS_DIR, RUN_DIR, SEED, build_model,
                    load_patients, patient_split, to_tensor)
from metrics import binary_metrics

EPOCHS = 12
BATCH_SIZE = 32
LR = 1e-4


def augment(x):
    """Random horizontal flip and small translation, applied per batch on the GPU."""
    flip = torch.rand(x.shape[0], device=x.device) < 0.5
    x = torch.where(flip.view(-1, 1, 1, 1), x.flip(-1), x)
    dx, dy = np.random.randint(-12, 13, size=2)
    return torch.roll(x, shifts=(int(dy), int(dx)), dims=(-2, -1))


@torch.no_grad()
def predict(model, x, batch_size=128):
    model.eval()
    probs = []
    for i in range(0, len(x), batch_size):
        logits = model(x[i:i + batch_size].to(DEVICE))
        probs.append(F.softmax(logits, dim=1)[:, 1].cpu())
    return torch.cat(probs).numpy()


def main():
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    split = patient_split()
    data = {}
    for name, patients in split.items():
        images, _, labels, _ = load_patients(patients)
        data[name] = (to_tensor(images), torch.from_numpy(labels))
        print(f"{name}: {len(patients)} patients, {len(labels)} slices, {labels.mean():.1%} tumour")

    model = build_model(pretrained=True).to(DEVICE)
    optimiser = torch.optim.Adam(model.parameters(), lr=LR)
    x_train, y_train = data["train"]
    pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    class_weights = torch.tensor([1.0, float(pos_weight)], device=DEVICE)

    best_auc, history = -1.0, []
    for epoch in range(EPOCHS):
        model.train()
        order = torch.randperm(len(x_train))
        total_loss = 0.0
        for i in range(0, len(order), BATCH_SIZE):
            idx = order[i:i + BATCH_SIZE]
            x = augment(x_train[idx].to(DEVICE))
            loss = F.cross_entropy(model(x), y_train[idx].to(DEVICE), weight=class_weights)
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()
            total_loss += loss.item() * len(idx)
        val = binary_metrics(data["val"][1].numpy(), predict(model, data["val"][0]))
        history.append({"epoch": epoch + 1, "train_loss": total_loss / len(order), **{f"val_{k}": v for k, v in val.items()}})
        print(history[-1])
        if val["auc"] > best_auc:
            best_auc = val["auc"]
            os.makedirs(RUN_DIR, exist_ok=True)
            torch.save(model.state_dict(), CHECKPOINT)

    model.load_state_dict(torch.load(CHECKPOINT))
    test = binary_metrics(data["test"][1].numpy(), predict(model, data["test"][0]))
    print("test:", test)
    with open(os.path.join(RESULTS_DIR, "train_metrics.json"), "w") as f:
        json.dump({"history": history, "best_val_auc": best_auc, "test": test,
                   "slices": {k: int(len(v[1])) for k, v in data.items()}}, f, indent=2)


if __name__ == "__main__":
    main()
