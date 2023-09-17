from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from random import randint
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials


from array import array
import os
from PIL import Image
import sys
import time
import cv2

#========================================= azure_ocr_config ============================================


subscription_key = "ADD_KEY_HERE."
endpoint = "https://computervisionbankofbaroda.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(
    endpoint, CognitiveServicesCredentials(subscription_key))

#========================================= main_section ============================================


class auto:

    def __init__(self,img_inp):
        self.img_inp = img_inp

        
        ocr_dict = {}
        key_list = []
        value_list = []
        
        self.ocr_dict = ocr_dict
        self.key_list = key_list
        self.value_list = value_list
    
   
        # Image path
        read_image_path = os.path.join(self.img_inp)
        # Open image
        read_image = open(read_image_path, "rb")

        read_response = computervision_client.read_in_stream(read_image, raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]


        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status.lower() not in ['notstarted', 'running']:
                break
            time.sleep(10)


        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:

                    # appending dictonari

                    self.ocr_dict[line.text] = [(line.bounding_box[0], line.bounding_box[1]), (line.bounding_box[2], line.bounding_box[3]), (
                        line.bounding_box[4], line.bounding_box[5]), (line.bounding_box[6], line.bounding_box[7])]
                    # appending lsit

                    self.key_list.append(line.text)
                    

                    # appending values

                    self.value_list.append(
                        [(line.bounding_box[0], line.bounding_box[1]), (line.bounding_box[2], line.bounding_box[3]), (
                            line.bounding_box[4], line.bounding_box[5]), (line.bounding_box[6], line.bounding_box[7])]
                    )
                    
            


    def draw_annota(self):

        img = self.img_inp
        list_bb = self.value_list

        img = cv2.imread(img)

        # img_h, img_w = img.shape[:2]

        colors = (0, 0, 225)

        for i in list_bb:

            x0y0, x0y1, x1y1, x1y0 = i

            x0 = int(x0y0[0])
            y0 = int(x0y0[1])
            x1 = int(x1y1[0])
            y1 = int(x1y1[1])

            cv2.rectangle(img, (x0, y0), (x1, y1),
                        color=colors, thickness=2)

        cv2.imwrite('annoted.png', img)


    def search_bb_by_text(self,text):

        if text in self.key_list:
            return self.ocr_dict[text]
        else:
            if len(text.split()) != 1:
                count = 0
                for i in text.split():
                    for j in self.key_list:
                        if i in j:
                            count =+ 1
                if count >= 2:
                    return self.ocr_dict[text]

                else:
                    pass

                

    def find_date(self):
        
        bb_text = self.search_bb_by_text("CBS")

        x0y0, x0y1, x1y1, x1y0 = bb_text

        x0 = int(x0y0[0])
        y0 = int(x0y0[1])
        x1 = int(x1y1[0])
        y1 = int(x1y1[1])

        """ find bb of element whose x0 > x0 of 'CBS' and y0 in b/w y0 and y1 of elemet """

        for i in self.value_list:
            X0Y0, X0Y1, X1Y1, X1Y0 = i

            X0 = int(X0Y0[0])
            Y0 = int(X0Y0[1])
            X1 = int(X1Y1[0])
            Y1 = int(X1Y1[1])

            if X0 > x1 and (y0 in range(Y0,Y1+1) or y0 > Y1):
                date_bb = i
                
                for k, v in self.ocr_dict.items():
                    if v == i:
                        return k.strip()
                    else:
                        pass            
                    
            else:
                pass

            

    def find_ifsc(self):
        
        blk_text = "RTGS / NEFT IFSC CODE"
        for i in self.key_list:
            if blk_text in i:
                ifsc_list = i.split(":")
                return ifsc_list[1].strip()
                
            else:
                pass

            

    def find_pay(self):
        
        bb_text = self.search_bb_by_text("Pay")

        x0y0, x0y1, x1y1, x1y0 = bb_text

        x0 = int(x0y0[0])
        y0 = int(x0y0[1])
        x1 = int(x1y1[0])
        y1 = int(x1y1[1])

        """ find bb of element whose x0 > x0 of 'CBS' and y0 in b/w y0 and y1 of elemet """

        for i in self.value_list:
            X0Y0, X0Y1, X1Y1, X1Y0 = i

            X0 = int(X0Y0[0])
            Y0 = int(X0Y0[1])
            X1 = int(X1Y1[0])
            Y1 = int(X1Y1[1])

            if X0 > x1 and (y0 in range(Y0,Y1+1) or y1 in range(Y0,Y1+1)):
                date_bb = i
                
                for k, v in self.ocr_dict.items():
                    if v == i:
                        return k.strip()
                    else:
                        pass

        
                    
            elif X0 > x1 and (Y1 in range(y0,y1+1) or Y0 in range(y0,y1+1)) :
                date_bb = i
                
                for k, v in self.ocr_dict.items():
                    if v == i:
                        return k.strip()
                    else:
                        pass

                    
            else:
                pass


    def find_ammount_in_word(self):
        
        bb_text = self.search_bb_by_text("Rupees रुपये")

        x0y0, x0y1, x1y1, x1y0 = bb_text

        x0 = int(x0y0[0])
        y0 = int(x0y0[1])
        x1 = int(x1y1[0])
        y1 = int(x1y1[1])

        """ find bb of element whose x0 > x0 of 'CBS' and y0 in b/w y0 and y1 of elemet """

        for i in self.value_list:
            X0Y0, X0Y1, X1Y1, X1Y0 = i

            X0 = int(X0Y0[0])
            Y0 = int(X0Y0[1])
            X1 = int(X1Y1[0])
            Y1 = int(X1Y1[1])

            if X0 > x1 and (y0 in range(Y0,Y1+1) or y1 in range(Y0,Y1+1)):
                date_bb = i
                
                for k, v in slef.ocr_dict.items():
                    if v == i:
                        return k.strip()
                    else:
                        pass

        
                    
            elif X0 > x1 and (Y1 in range(y0,y1+1) or Y0 in range(y0,y1+1)) :
                date_bb = i
                
                for k, v in self.ocr_dict.items():
                    if v == i:
                        return k.strip()
                    else:
                        pass

                    
            else:
                pass

    def find_ammount_in_digit(self):
        bb_text = self.search_bb_by_text("₹")

        x0y0, x0y1, x1y1, x1y0 = bb_text

        x0 = int(x0y0[0])
        y0 = int(x0y0[1])
        x1 = int(x1y1[0])
        y1 = int(x1y1[1])

        """ find bb of element whose x0 > x0 of 'CBS' and y0 in b/w y0 and y1 of elemet """

        for i in self.value_list:
            X0Y0, X0Y1, X1Y1, X1Y0 = i

            X0 = int(X0Y0[0])
            Y0 = int(X0Y0[1])
            X1 = int(X1Y1[0])
            Y1 = int(X1Y1[1])

            if X0 > x1 and (y0 in range(Y0,Y1+1) or y1 in range(Y0,Y1+1)):
                date_bb = i
                
                for k, v in self.ocr_dict.items():
                    if v == i:
                        k = k.strip()
                        # try:
                        #     int(k)
                        #     return k
                        # except:
                        #     try:
                        #         k = int(k[0:len(k)-1])
                        #         return k
                        #     except:
                        #         return k

                        string_digit = ""
                        for i in k:
                            try:
                                if isinstance(int(i), int):
                                    string_digit += i 
                            except:
                                pass
                                
                        return(string_digit)
                            
                    else:
                        pass
    

        
                    
            elif X0 > x1 and (Y1 in range(y0,y1+1) or Y0 in range(y0,y1+1)) :
                date_bb = i
                
                for k, v in self.ocr_dict.items():
                    if v == i:
                        k = k.strip()

                        string_digit = ""
                        for i in k:
                            try:
                                if isinstance(int(i), int):
                                    string_digit += i 
                            except:
                                pass
                                
                        return(string_digit)
                    else:
                        pass
    
            else:
                pass


    def find_accno(self):
            
        bb_text1 = self.search_bb_by_text("खा. सं.")
        bb_text2 = self.search_bb_by_text("A/c No.")

        x0y0, x0y1, x1y1, x1y0 = bb_text1
        a0b0, a0b1, a1b1, a1v0 = bb_text2
        

        x0 = int(x0y0[0])
        y0 = int(x0y0[1])
        x1 = int(x1y1[0])
        y1 = int(x1y1[1])

        a0 = int(a0b0[0])
        b0 = int(a0b0[1])
        a1 = int(a1b1[0])
        b1 = int(a1b1[1])

        """ find bb of element whose x0 > x0 of 'CBS' and y0 in b/w y0 and y1 of elemet """

        for i in self.value_list:
            
            X0Y0, X0Y1, X1Y1, X1Y0 = i

            X0 = int(X0Y0[0])
            Y0 = int(X0Y0[1])
            X1 = int(X1Y1[0])
            Y1 = int(X1Y1[1])

            if X0 > x1 and (Y0 in range(y0,b1+1) or Y1 in range(y0,b1+1)):
                date_bb = i
                
                for k, v in self.ocr_dict.items():
                    if v == i:
                        return k.strip()
                    else:
                        pass


                    
            else:
                pass


    def find_cheque_no(self):

        depth = []
        temp = {}

        for i in self.value_list:
            x0y0, x0y1, x1y1, x1y0 = i
            
            y1 = int(x1y1[1])
            
            temp[y1] = i
            depth.append(y1)

        deepest = max(depth)
        bb_cheque_no = temp[deepest]

        for k,v in self.ocr_dict.items():
            if v == bb_cheque_no:
                return k.strip()
            else:
                pass



# if __name__ == '__main__':

#     k = auto("./images/cheque.png")
#     k.draw_annota()
#     print(k.find_cheque_no())
#     print(k.find_accno())
#     print(k.find_date())
#     print(k.find_ammount_in_digit())
#     print(k.find_pay())
#     print(k.find_ifsc())
