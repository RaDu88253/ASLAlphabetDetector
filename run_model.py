import torch
import torch.nn.functional as F

from train import HandMLP


class HandSignRecogniser:
    def __init__(self, model_path, class_names, threshold=0.6):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = HandMLP(len(class_names))
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        self.class_names = class_names
        self.threshold = threshold

    def predict(self, input_tensor):
        with torch.no_grad():
            logits = self.model(input_tensor.to(self.device))
            probs = F.softmax(logits, dim=1)
            conf, pred = torch.max(probs, dim=1)

            if conf.item() < self.threshold:
                return "undefined", conf.item()
            return self.class_names[pred.item()], conf.item()
