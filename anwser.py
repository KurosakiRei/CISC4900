import os

file = open('anwser.txt', 'w')
image_name_list = [ each for each in os.listdir(r'./images')]
for each in image_name_list:
    image_id = each.split('/')[-1].split('.')[0]
    file.write(str(image_id) + '\n')
file.close()