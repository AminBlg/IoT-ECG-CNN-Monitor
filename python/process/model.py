import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import load_model
import numpy as np
from sklearn import preprocessing
import pandas
import warnings
warnings.filterwarnings("ignore")


MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'best_model.h5')


class Proc:
    def __init__(self, model_path=MODEL_PATH):
        """Load the CNN model once at initialization."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = load_model(model_path)

    def run(self, ecg):
        """Run CNN inference on an ECG signal array.

        The signal is segmented into 186-sample windows, normalized,
        and classified using the pre-loaded Keras model.

        Args:
            ecg: numpy array of ECG samples.

        Returns:
            Averaged prediction probabilities across all windows,
            or None if inference fails.
        """
        try:
            ecg1 = ecg.copy()

            if len(ecg1) >= 186:
                ecg1 = ecg1[:186 * (len(ecg1) // 186)]
            else:
                ecg1 = np.pad(ecg1, (0, 186 - len(ecg1)), mode='constant')

            # Reshape into 186-sample windows FIRST, then normalize each independently
            ecg1 = ecg1.reshape(-1, 186)
            ecg1 = preprocessing.normalize(ecg1)
            ecg1 = ecg1.reshape(-1, 186, 1)

            return np.mean(self.model.predict(ecg1), axis=0)

        except (TypeError, ValueError) as e:
            print(f"Inference error: {e}")
            return None


if __name__ == '__main__':
    proc = Proc()
    try:
        data = pandas.read_csv(
            os.path.join(os.path.dirname(__file__), '..', 'data.csv'),
            sep=r'\s*,\s*', engine='python'
        )
        result = proc.run(data['ecg'].to_numpy())
        print(result)
    except KeyboardInterrupt:
        print("Proc interrupted, closing...")
