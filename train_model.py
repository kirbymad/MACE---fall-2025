from ase.io import read, write

db = read('data/Y_BaZrO3_input_data.xyz', ':')
write('data/Y_BaZrO3_input_data_train.xyz', db[:100]) #first 100 configs
write('data/Y_BaZrO3_input_data_test.xyz', db[-34:]) #last 34 configs