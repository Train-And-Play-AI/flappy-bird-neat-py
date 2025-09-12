import os.path

from ai.neat_trainer import run_neat
from ai.watcher import run_with_ai

if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    print("Select from below options")
    print("1. Train")
    print("2. Eval")
    choice = input("Enter your choice:")

    if choice == "1" :
        run_neat(config_path)
    if choice == "2" :
        run_with_ai(config_path)

    input("Press enter to exit...")