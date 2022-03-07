import argparse

from src.mutations_train import run_training
from src.mutations_predict import run_prediction


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("config", default=None, help="Path to config file.")

    args = parser.parse_args()

    run_name, model_dir, model_type = run_training(args.config)

    # run_prediction(
    #     config=args.config,
    #     run_name=run_name,
    #     model_output_dir=model_dir,
    #     model_type=model_type,
    # )
