import module
import csv
import os



# k = module.auto("./images/cheque.png")

# k.draw_annota()
# print(k.find_cheque_no())
# print(k.find_accno())
# print(k.find_date())
# print(k.find_ammount_in_digit())
# print(k.find_pay())
# print(k.find_ifsc())


path = './images'
img_list = []
dir_list = os.listdir(path)

for i in dir_list:
    if i.endswith(".png") or i.endswith(".jpg") or i.endswith(".jpeg"):
        print(i)
        img_list.append(i)



for i in img_list:
    new_path = path + "/" + i
   
    k = module.auto(new_path)
    l = [k.find_accno(), k.find_date(), k.find_cheque_no(), k.find_ammount_in_digit(), k.find_pay(), k.find_ifsc()]
    with open('data.csv', 'a', newline ='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(x for x in l)
       
