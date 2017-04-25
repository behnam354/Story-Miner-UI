'''
input : a text file, N: number of output chunks
output : separate the input file into N number of chunks.
'''

input_file = "../../data/Vaccination/sents_separated_clean.txt"
output_loc = "../../data/Vaccination/mothering_chunks_sent_sep_clean/"

chunk_ind = 1
num_chunks = 200

data = []

with open(input_file,"r") as f:
    for i, line in enumerate(f):
        if line.strip():
            data.append(line)


num_lines = len(data)

for i in range(num_chunks):
    output_file = output_loc+"sents_"+str(i+1)+".txt"
    startInd = i*(num_lines/num_chunks)
    endInd = (i+1)*(num_lines/num_chunks)
    with open(output_file,"w") as f:
        #if i > 0:
        f.write("text\n")
        f.writelines(data[startInd:endInd])

