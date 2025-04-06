import numpy as np
import random
from transformers import pipeline

print("ATTEMPTING TO LOAD MODEL IN MODELING FILE.")
MODEL = "CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-all-age"


pipe = pipeline("audio-classification", model=MODEL)
print("PIPELINE LOADED FROM MODEL CLASS.")


TEST_AUDIO = "test_audio.mp3"


# Helper functions.
def norm_probs(probabilities):
    total = sum(probabilities)
    return [p/total for p in probabilities]


def create_predict_dict(labels, probabilities):
    """Used to format the output."""
    neg_prob = 0
    pos_prob = 0
    neu_prob = 0

    for label, prob in zip(labels, probabilities):

        if label == "NEGATIVE":
            neg_prob += prob
        elif label == "POSITIVE":
            pos_prob += prob
        elif label == "NEUTRAL":
            neu_prob += prob

    result = {
        "POSITIVE": pos_prob,
        "NEGATIVE": neg_prob,
        "NEUTRAL": neu_prob
    }

    return result


class SerModel():

    def __init__(self):
        self.model_id = "CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-elderly" 

    def predict(self, audio_file: str):
        raw_model_output = pipe(audio_file, device=0)
        label_list = [
            'sadness',
            'fear',
            'angry',
            'happiness',
            'disgust',
            'neutral',
            'surprise',
            'positive',
            'negative',
            'excitement',
            'frustrated',
            'other',
            'unknown'
        ]

        negative = [
            'sadness',
            'fear',
            'angry',
            'disgust',
            'negative',
            "frustrated"
        ]

        positive = [
            "happiness",
            "surprise",
            "positive",
            "excitement"
        ]

        neutral = [
            "neutral",
            "other",
            "unknown"
        ]

        labels = []
        probas = []

        for item in raw_model_output:

            # Extracting the position of the label in the raw output. 
            label_index = int(item['label'].split('_')[1])

            # Saving the label.
            item['emotion'] = label_list[label_index]

            # Resetting the label.
            label = None

            # Sorting the label.
            if item['emotion'] in negative:
                label = "NEGATIVE"
            elif item['emotion'] in positive:
                label = "POSITIVE"
            elif item['emotion'] in neutral:
                label = "NEUTRAL"

            labels.append(label)
            probas.append(item["score"])

        normed_probs = norm_probs(probas)

        result = create_predict_dict(labels, normed_probs)

        print(result)

        return result

    def dummy_predict(self, audio_array: np.array = None):
        """
        Used to generate fake probabilities for testing and dev 
        purposes.
        """
        # Generate three random numbers
        random_nums = [random.random() for _ in range(3)]

        # Normalize them so they sum to 1
        total = sum(random_nums)
        normalized_probs = [x / total for x in random_nums]

        # Create the dictionary with probabilities
        prob_dict = {
            "POSITIVE": normalized_probs[0],
            "NEGATIVE": normalized_probs[1],
            "NEUTRAL": normalized_probs[2]
        }

        return prob_dict


def main():
    model = SerModel()

    print(model.predict(TEST_AUDIO))

    # print(model.dummy_predict())


if __name__ == "__main__":
    main()
