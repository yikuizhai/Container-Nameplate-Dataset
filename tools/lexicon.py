
file = open('/home/lixinru/devdata/code_env/DPText-DETR/datasets/evaluation/lexicons/ctw1500/ctw1500_lexicon.txt', 'r').readlines()
file_1 = open('/home/lixinru/devdata/code_env/DPText-DETR/datasets/evaluation/lexicons/ctw1500/ctw1500_pair_list.txt', 'w')
for i in file:
    text = i.split("\n")[0]
    file_1.write(text + " " + text + "\n")
file_1.close()