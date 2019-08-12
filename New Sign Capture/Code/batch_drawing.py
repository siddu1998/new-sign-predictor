import cv2
import pandas as pd
import argparse
import os

# ap = argparse.ArgumentParser()
# ap.add_argument("-s_path_fr", "--sign_inventory_path_fr", help = "Enter the sign inventory path for right images")
# ap.add_argument("-s_path_fc", "--sign_inventory_path_fc", help = "Enter the sign inventory path for center images")
# ap.add_argument("-img_path_fr","--image_path_fr",help="Enter path for front right images")
# ap.add_argument("-img_path_fr","--image_path_fc",help="Enter path for front camera images")


#args = vars(ap.parse_args())

#loading fr invento
sign_inventory_fr='../FL_I-575_North_2_output.csv'
df=pd.read_csv(sign_inventory_fr)




image_list=[]

def get_image_list(img_path):
    image_list=[]
    sub_folders = sorted(os.listdir(img_path))
    jpg_cnt = sum(1 for f in sub_folders if f.endswith(".jpg"))
    if jpg_cnt == 0:
        # frames are in the sub-directories
        file_list = []
        for sub_folder in sub_folders:
            img_path= img_path
            temp_list = (os.listdir(os.path.join(img_path,sub_folder)))
            temp_list = [os.path.join(sub_folder, f) for f in temp_list if f.endswith(".jpg")]
            file_list = file_list + temp_list
            
        file_list.sort()
        return file_list
    else:
        # frames are in the folder
        image_list = sub_folders

    return image_list

images=get_image_list('../575Norh')

for row in df.iterrows():
    index=row[0]
    value=row[1]
    if value['frame_id_2018']=='None':
        print('None')    
    else:
        print(value['frame_id_2018'])
        img_path='../'+value['frame_path_2018']
        print(img_path)
        img=cv2.imread(img_path)
        img=cv2.rectangle(img, (int(float(value['bbox_x1'])),int(float(value['bbox_y1']))), (int(float(value['bbox_x2'])),int(float(value['bbox_y2']))), (255,0,0),-1)
        cv2.imwrite(img_path,img)
print('Done')