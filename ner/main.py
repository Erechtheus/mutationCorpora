import argparse

from src.mutations_train import run_training
from src.mutations_predict import run_prediction


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("config", default=None, help="Path to config file.")
    parser.add_argument("--predict", default=False, action="store_true")
    parser.add_argument("--train", default=True, action="store_true")

    args = parser.parse_args()

    if args.train:
        run_name, model_dir, model_type = run_training(
            args.config, final_eval_on_val=True
        )

    if args.predict:

        run_prediction(
            config=args.config,
            run_name=run_name,
            model_output_dir=model_output_dir,
            model_type=model_type,
        )
