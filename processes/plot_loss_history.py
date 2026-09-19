from pathlib import Path
import pickle
import sys
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def plot_model_loss(model_name):
    h_params = pickle.load(open((PROJECT_ROOT / "trained_models" / model_name / "h_params.pkl"), "rb"))
    loss_history = h_params["LOSS_HISTORY"]

    train_history = [loss_tuple[0] for loss_tuple in loss_history]
    train_history, val_history = zip(*loss_history)

    x = range(len(loss_history))

    # print(f"Train History: {train_history}")
    # print(f"Test History: {val_history}")

    fig, ax = plt.subplots()
    ax.plot(x, train_history, label="Training Loss")
    ax.plot(x, val_history, label="Validation Loss")
    ax.set(xlabel="Epochs", ylabel="Total Loss", title=f"{model_name} Loss History:")
    plt.legend()
    plt.savefig(PROJECT_ROOT / "trained_models" / model_name / "loss_history.png")
    # plt.show()

if __name__ == "__main__":
    plot_model_loss("lossy")