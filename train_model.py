from ase.io import read, write

db = read('/home/melissasanseverino/maceML/MakeInput/Y_BaZrO3_input_data.xyz', ':')
write('/home/melissasanseverino/maceML/MakeInput/Y_BaZrO3_input_data_train.xyz', db[:100]) #first 200 configs plus the 3 E0s
write('/home/melissasanseverino/maceML/MakeInput/Y_BaZrO3_input_data_test.xyz', db[-34:]) #last 1000 configs