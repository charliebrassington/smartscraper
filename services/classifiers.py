from domain import models

from sklearn.neural_network import MLPClassifier


class ClassifierService:

    def __init__(self, trained_model: models.TrainedModel):
        self.trained_model = trained_model

    def classify_text(self, unclassified_text: str) -> str | None:
        vectorized_text = self.trained_model.count_vectorizer.transform([unclassified_text])
        predicted_probability = self.trained_model.model.predict_proba(vectorized_text)[0]

        predicted_label_index = predicted_probability.argmax()
        probability = predicted_probability[predicted_label_index]

        if probability < 0.7:
            return None

        return self.trained_model.label_encoder.inverse_transform([predicted_label_index])[0]
