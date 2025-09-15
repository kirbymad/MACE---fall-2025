from mace.cli.eval_configs import main as mace_eval_configs_main
import sys

def eval_mace(configs, model, output):
    sys.argv = ["program", "--configs", configs, "--model", model, "--output", output]
    mace_eval_configs_main()
#evaluate the training set
eval_mace(configs="/home/melissasanseverino/maceML/MakeInput/Y_BaZrO3_input_data_train.xyz",
          model="/home/melissasanseverino/maceML/MakeInput/MACE_models/mace01_run-123_stagetwo.model",
          output="/home/melissasanseverino/maceML/MakeInput/tests/mace01/Y_BaZrO3_train.xyz")

#evaluate the test set
eval_mace(configs="/home/melissasanseverino/maceML/MakeInput/Y_BaZrO3_input_data_test.xyz",
          model="/home/melissasanseverino/maceML/MakeInput/MACE_models/mace01_run-123_stagetwo.model",
          output="/home/melissasanseverino/maceML/MakeInput/tests/mace01/Y_BaZrO3_test.xyz")