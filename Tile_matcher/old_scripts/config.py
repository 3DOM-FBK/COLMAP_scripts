### UTILIZZO
# >conda activate opencv
# >cd C:\Users\Luscias\Desktop\3DOM\Python_scripts\CNN_Python
# >python 3domPipeline.py

import os

### INPUT IMAGES
image_set = []
# Specifica le immagini
image_set = os.listdir(r"C:\Users\Luscias\Desktop\buttare\prova\imgs")
#image_set = image_set[0:10]
#image_set = ["1.png", "2.png"]
#image_set = ['IMG_8847.JPG','IMG_8848.JPG','IMG_8849.JPG','IMG_8850.JPG','IMG_8851.JPG','IMG_8852.JPG','IMG_8853.JPG','IMG_8854.JPG','IMG_8855.JPG','IMG_8856.JPG','IMG_8857.JPG','IMG_8858.JPG','IMG_8859.JPG','IMG_8860.JPG','IMG_8868.JPG','IMG_8869.JPG','IMG_8870.JPG','IMG_8871.JPG','IMG_8872.JPG','IMG_8873.JPG','IMG_8874.JPG','IMG_8875.JPG','IMG_8876.JPG','IMG_8877.JPG','IMG_8878.JPG','IMG_8879.JPG','IMG_8880.JPG','IMG_8881.JPG','IMG_8882.JPG','IMG_8883.JPG','IMG_8884.JPG','IMG_8885.JPG','IMG_8886.JPG','IMG_8887.JPG','IMG_8888.JPG','IMG_8889.JPG','IMG_8890.JPG','IMG_8891.JPG','IMG_8892.JPG','IMG_8893.JPG','IMG_8894.JPG','IMG_8895.JPG','IMG_8896.JPG','IMG_8897.JPG','IMG_8898.JPG','IMG_8899.JPG','IMG_8900.JPG','IMG_8901.JPG','IMG_8902.JPG','IMG_8903.JPG','IMG_8904.JPG','IMG_8905.JPG','IMG_8906.JPG','IMG_8907.JPG','IMG_8908.JPG','IMG_8909.JPG','IMG_8910.JPG','IMG_8911.JPG','IMG_8912.JPG','IMG_8913.JPG','IMG_8914.JPG','IMG_8915.JPG','IMG_8916.JPG','IMG_8918.JPG','IMG_8919.JPG','IMG_8920.JPG','IMG_8921.JPG','IMG_8922.JPG','IMG_8923.JPG','IMG_8924.JPG','IMG_8925.JPG','IMG_8926.JPG','IMG_8927.JPG','IMG_8928.JPG','IMG_8929.JPG','IMG_8930.JPG','IMG_8931.JPG','IMG_8932.JPG','IMG_8933.JPG','IMG_8934.JPG','IMG_8935.JPG','IMG_8936.JPG','IMG_8937.JPG','IMG_8938.JPG','IMG_8939.JPG','IMG_8940.JPG','IMG_8941.JPG','IMG_8942.JPG','IMG_8943.JPG','IMG_8944.JPG','IMG_8945.JPG','IMG_8946.JPG','IMG_8947.JPG','IMG_8948.JPG','IMG_8949.JPG','IMG_8950.JPG','IMG_8951.JPG','IMG_8952.JPG','IMG_8953.JPG','IMG_8954.JPG','IMG_8955.JPG','IMG_8956.JPG','IMG_8957.JPG','IMG_8958.JPG','IMG_8959.JPG','IMG_8960.JPG','IMG_8961.JPG','IMG_8962.JPG','IMG_8963.JPG','IMG_8964.JPG','IMG_8965.JPG','IMG_8966.JPG','IMG_8967.JPG','IMG_8968.JPG','IMG_8969.JPG','IMG_8970.JPG','IMG_8971.JPG','IMG_8972.JPG','IMG_8973.JPG','IMG_8974.JPG','IMG_8975.JPG','IMG_8976.JPG','IMG_8977.JPG','IMG_8978.JPG','IMG_8979.JPG','IMG_8980.JPG','IMG_8981.JPG','IMG_8982.JPG','IMG_8983.JPG','IMG_8984.JPG','IMG_8985.JPG','IMG_8986.JPG','IMG_8987.JPG','IMG_8988.JPG','IMG_8989.JPG','IMG_8990.JPG','IMG_8991.JPG','IMG_8992.JPG','IMG_8993.JPG','IMG_8994.JPG','IMG_8995.JPG','IMG_8996.JPG','IMG_8998.JPG','IMG_8999.JPG','IMG_9000.JPG','IMG_9001.JPG','IMG_9002.JPG','IMG_9003.JPG','IMG_9004.JPG','IMG_9005.JPG','IMG_9006.JPG','IMG_9007.JPG','IMG_9008.JPG','IMG_9009.JPG','IMG_9010.JPG','IMG_9011.JPG','IMG_9012.JPG','IMG_9013.JPG','IMG_9014.JPG','IMG_9015.JPG','IMG_9016.JPG','IMG_9017.JPG','IMG_9018.JPG','IMG_9019.JPG','IMG_9020.JPG','IMG_9021.JPG','IMG_9022.JPG','IMG_9023.JPG','IMG_9024.JPG','IMG_9025.JPG','IMG_9026.JPG','IMG_9027.JPG','IMG_9028.JPG','IMG_9029.JPG','IMG_9030.JPG','IMG_9031.JPG','IMG_9032.JPG','IMG_9033.JPG','IMG_9034.JPG','IMG_9035.JPG','IMG_9036.JPG','IMG_9037.JPG','IMG_9038.JPG','IMG_9039.JPG','IMG_9040.JPG','IMG_9041.JPG','IMG_9042.JPG','IMG_9043.JPG','IMG_9044.JPG','IMG_9045.JPG','IMG_9046.JPG','IMG_9047.JPG','IMG_9048.JPG','IMG_9049.JPG','IMG_9050.JPG','IMG_9051.JPG','IMG_9052.JPG','IMG_9053.JPG','IMG_9054.JPG','IMG_9055.JPG','IMG_9056.JPG','IMG_9057.JPG','IMG_9058.JPG','IMG_9059.JPG','IMG_9060.JPG','IMG_9061.JPG','IMG_9062.JPG','IMG_9063.JPG','IMG_9064.JPG','IMG_9065.JPG','IMG_9066.JPG','IMG_9067.JPG','IMG_9068.JPG','IMG_9069.JPG','IMG_9070.JPG','IMG_9071.JPG','IMG_9072.JPG','IMG_9073.JPG','IMG_9074.JPG','IMG_9075.JPG','IMG_9076.JPG','IMG_9077.JPG','IMG_9078.JPG','IMG_9079.JPG','IMG_9080.JPG','IMG_9081.JPG','IMG_9082.JPG','IMG_9083.JPG','IMG_9084.JPG','IMG_9085.JPG','IMG_9086.JPG','IMG_9087.JPG','IMG_9088.JPG','IMG_9089.JPG','IMG_9090.JPG','IMG_9091.JPG','IMG_9092.JPG','IMG_9093.JPG','IMG_9094.JPG','IMG_9095.JPG','IMG_9096.JPG','IMG_9097.JPG','IMG_9098.JPG','IMG_9099.JPG','IMG_9100.JPG','IMG_9101.JPG','IMG_9102.JPG','IMG_9103.JPG','IMG_9104.JPG','IMG_9105.JPG','IMG_9106.JPG','IMG_9107.JPG','IMG_9108.JPG','IMG_9109.JPG','IMG_9110.JPG','IMG_9111.JPG','LEO_8459_acr.jpg','LEO_8460_acr.jpg','LEO_8461_acr.jpg','LEO_8462_acr.jpg','LEO_8463_acr.jpg','LEO_8464_acr.jpg','LEO_8465_acr.jpg','LEO_8466_acr.jpg','LEO_8467_acr.jpg','LEO_8468_acr.jpg','LEO_8469_acr.jpg','LEO_8470_acr.jpg','LEO_8471_acr.jpg','LEO_8472_acr.jpg','LEO_8473_acr.jpg','LEO_8474_acr.jpg','LEO_8475_acr.jpg','LEO_8476_acr.jpg','LEO_8477_acr.jpg','LEO_8478_acr.jpg','LEO_8479_acr.jpg','LEO_8480_acr.jpg','LEO_8481_acr.jpg','LEO_8482_acr.jpg','LEO_8483_acr.jpg','LEO_8484_acr.jpg','LEO_8485_acr.jpg','LEO_8486_acr.jpg','LEO_8487_acr.jpg','LEO_8488_acr.jpg','LEO_8489_acr.jpg','LEO_8490_acr.jpg','LEO_8491_acr.jpg','LEO_8492_acr.jpg','LEO_8493_acr.jpg','LEO_8494_acr.jpg','LEO_8495_acr.jpg','LEO_8496_acr.jpg','LEO_8497_acr.jpg','LEO_8498_acr.jpg','LEO_8499_acr.jpg','LEO_8500_acr.jpg','LEO_8501_acr.jpg','LEO_8502_acr.jpg','LEO_8503_acr.jpg','LEO_8504_acr.jpg','LEO_8505_acr.jpg','LEO_8506_acr.jpg','LEO_8507_acr.jpg','LEO_8508_acr.jpg','LEO_8509_acr.jpg','LEO_8510_acr.jpg','LEO_8511_acr.jpg','LEO_8512_acr.jpg','LEO_8513_acr.jpg','LEO_8514_acr.jpg','LEO_8515_acr.jpg','LEO_8516_acr.jpg','LEO_8517_acr.jpg','LEO_8518_acr.jpg','LEO_8519_acr.jpg','LEO_8520_acr.jpg','LEO_8521_acr.jpg','LEO_8522_acr.jpg','LEO_8523_acr.jpg','LEO_8524_acr.jpg','LEO_8525_acr.jpg','LEO_8526_acr.jpg','LEO_8527_acr.jpg','LEO_8528_acr.jpg','LEO_8529_acr.jpg','LEO_8530_acr.jpg','LEO_8531_acr.jpg','LEO_8532_acr.jpg','LEO_8533_acr.jpg','LEO_8534_acr.jpg','LEO_8535_acr.jpg','LEO_8536_acr.jpg','LEO_8537_acr.jpg','LEO_8538_acr.jpg','LEO_8539_acr.jpg','LEO_8540_acr.jpg','LEO_8541_acr.jpg','LEO_8542_acr.jpg','LEO_8543_acr.jpg','LEO_8544_acr.jpg','LEO_8545_acr.jpg','LEO_8546_acr.jpg','LEO_8547_acr.jpg','LEO_8548_acr.jpg','LEO_8549_acr.jpg','LEO_8550_acr.jpg','LEO_8551_acr.jpg','LEO_8552_acr.jpg','LEO_8553_acr.jpg','LEO_8554_acr.jpg','LEO_8555_acr.jpg','LEO_8556_acr.jpg','LEO_8557_acr.jpg','LEO_8558_acr.jpg','LEO_8559_acr.jpg','LEO_8560_acr.jpg','LEO_8561_acr.jpg','LEO_8562_acr.jpg','LEO_8563_acr.jpg','LEO_8564_acr.jpg','LEO_8565_acr.jpg','LEO_8566_acr.jpg','LEO_8567_acr.jpg','LEO_8568_acr.jpg','LEO_8569_acr.jpg','LEO_8570_acr.jpg','LEO_8571_acr.jpg','LEO_8572_acr.jpg','LEO_8573_acr.jpg','LEO_8574_acr.jpg','LEO_8575_acr.jpg','LEO_8576_acr.jpg','LEO_8577_acr.jpg','LEO_8578_acr.jpg','LEO_8579_acr.jpg','LEO_8580_acr.jpg','LEO_8581_acr.jpg','LEO_8582_acr.jpg','LEO_8583_acr.jpg','LEO_8584_acr.jpg','LEO_8585_acr.jpg','LEO_8586_acr.jpg','LEO_8587_acr.jpg','LEO_8588_acr.jpg','LEO_8589_acr.jpg','LEO_8590_acr.jpg','LEO_8591_acr.jpg','LEO_8592_acr.jpg','LEO_8593_acr.jpg','LEO_8594_acr.jpg','LEO_8595_acr.jpg','LEO_8596_acr.jpg','LEO_8597_acr.jpg','LEO_8598_acr.jpg','LEO_8599_acr.jpg','LEO_8600_acr.jpg','LEO_8601_acr.jpg','LEO_8602_acr.jpg','LEO_8603_acr.jpg','LEO_8604_acr.jpg','LEO_8605_acr.jpg','LEO_8606_acr.jpg','LEO_8607_acr.jpg','LEO_8608_acr.jpg','LEO_8609_acr.jpg','LEO_8610_acr.jpg','LEO_8611_acr.jpg','LEO_8612_acr.jpg','LEO_8613_acr.jpg','LEO_8614_acr.jpg','LEO_8615_acr.jpg','LEO_8616_acr.jpg','LEO_8617_acr.jpg','LEO_8618_acr.jpg','LEO_8619_acr.jpg','LEO_8620_acr.jpg','LEO_8621_acr.jpg','LEO_8622_acr.jpg','LEO_8623_acr.jpg','LEO_8624_acr.jpg','LEO_8625_acr.jpg','LEO_8626_acr.jpg','LEO_8627_acr.jpg','LEO_8628_acr.jpg','LEO_8629_acr.jpg','LEO_8630_acr.jpg','LEO_8631_acr.jpg','LEO_8632_acr.jpg','LEO_8633_acr.jpg','LEO_8634_acr.jpg','LEO_8635_acr.jpg','LEO_8636_acr.jpg','LEO_8637_acr.jpg','LEO_8638_acr.jpg','LEO_8639_acr.jpg','LEO_8640_acr.jpg','LEO_8641_acr.jpg','LEO_8642_acr.jpg','LEO_8643_acr.jpg','LEO_8644_acr.jpg','LEO_8645_acr.jpg','LEO_8646_acr.jpg','LEO_8647_acr.jpg','LEO_8648_acr.jpg','LEO_8649_acr.jpg','LEO_8650_acr.jpg','LEO_8651_acr.jpg','LEO_8652_acr.jpg','LEO_8653_acr.jpg','LEO_8654_acr.jpg','LEO_8655_acr.jpg','LEO_8656_acr.jpg','LEO_8657_acr.jpg','LEO_8658_acr.jpg','LEO_8659_acr.jpg','LEO_8660_acr.jpg','LEO_8661_acr.jpg','LEO_8662_acr.jpg','LEO_8663_acr.jpg','LEO_8664_acr.jpg','LEO_8665_acr.jpg','LEO_8666_acr.jpg','LEO_8667_acr.jpg','LEO_8668_acr.jpg','LEO_8669_acr.jpg','LEO_8670_acr.jpg','LEO_8671_acr.jpg','LEO_8672_acr.jpg','LEO_8673_acr.jpg','LEO_8674_acr.jpg','LEO_8675_acr.jpg','LEO_8676_acr.jpg','LEO_8677_acr.jpg','LEO_8678_acr.jpg','LEO_8679_acr.jpg','LEO_8680_acr.jpg','LEO_8681_acr.jpg','LEO_8682_acr.jpg','LEO_8683_acr.jpg','LEO_8684_acr.jpg','LEO_8685_acr.jpg','LEO_8686_acr.jpg','LEO_8687_acr.jpg','LEO_8688_acr.jpg','LEO_8689_acr.jpg','LEO_8690_acr.jpg','LEO_8691_acr.jpg','LEO_8692_acr.jpg','LEO_8693_acr.jpg','LEO_8694_acr.jpg','LEO_8695_acr.jpg','LEO_8696_acr.jpg','LEO_8697_acr.jpg','LEO_8698_acr.jpg','LEO_8699_acr.jpg','LEO_8700_acr.jpg','LEO_8701_acr.jpg','LEO_8702_acr.jpg','LEO_8703_acr.jpg','LEO_8704_acr.jpg','LEO_8705_acr.jpg','LEO_8706_acr.jpg','LEO_8707_acr.jpg','LEO_8708_acr.jpg','LEO_8709_acr.jpg','LEO_8710_acr.jpg','LEO_8711_acr.jpg','LEO_8712_acr.jpg','LEO_8713_acr.jpg','LEO_8714_acr.jpg','LEO_8715_acr.jpg','LEO_8716_acr.jpg','LEO_8717_acr.jpg','LEO_8718_acr.jpg','LEO_8719_acr.jpg','LEO_8720_acr.jpg','LEO_8721_acr.jpg','LEO_8722_acr.jpg','LEO_8723_acr.jpg','LEO_8724_acr.jpg','LEO_8725_acr.jpg','LEO_8726_acr.jpg','LEO_8727_acr.jpg','LEO_8728_acr.jpg','LEO_8729_acr.jpg','LEO_8730_acr.jpg','LEO_8731_acr.jpg','LEO_8732_acr.jpg','LEO_8733_acr.jpg','LEO_8734_acr.jpg','LEO_8735_acr.jpg','LEO_8736_acr.jpg','LEO_8737_acr.jpg','LEO_8738_acr.jpg','LEO_8739_acr.jpg','LEO_8740_acr.jpg','LEO_8741_acr.jpg','LEO_8742_acr.jpg','LEO_8743_acr.jpg','LEO_8744_acr.jpg','LEO_8745_acr.jpg','LEO_8746_acr.jpg','LEO_8747_acr.jpg','LEO_8748_acr.jpg','LEO_8749_acr.jpg','LEO_8750_acr.jpg','LEO_8751_acr.jpg','LEO_8752_acr.jpg','LEO_8753_acr.jpg','LEO_8754_acr.jpg','LEO_8755_acr.jpg','LEO_8756_acr.jpg','LEO_8757_acr.jpg','LEO_8758_acr.jpg','LEO_8759_acr.jpg','LEO_8760_acr.jpg','LEO_8761_acr.jpg','LEO_8762_acr.jpg','LEO_8763_acr.jpg','LEO_8764_acr.jpg','LEO_8765_acr.jpg','LEO_8766_acr.jpg','LEO_8767_acr.jpg','LEO_8768_acr.jpg','LEO_8769_acr.jpg','LEO_8770_acr.jpg','LEO_8771_acr.jpg','LEO_8772_acr.jpg','LEO_8773_acr.jpg','LEO_8774_acr.jpg','LEO_8775_acr.jpg','LEO_8776_acr.jpg','LEO_8777_acr.jpg','LEO_8778_acr.jpg','LEO_8779_acr.jpg','LEO_8780_acr.jpg','LEO_8781_acr.jpg','LEO_8782_acr.jpg','LEO_8783_acr.jpg','LEO_8784_acr.jpg','LEO_8785_acr.jpg','LEO_8786_acr.jpg','LEO_8787_acr.jpg','LEO_8788_acr.jpg','LEO_8789_acr.jpg','LEO_8790_acr.jpg','LEO_8791_acr.jpg','LEO_8792_acr.jpg','LEO_8793_acr.jpg','LEO_8794_acr.jpg','LEO_8795_acr.jpg','LEO_8796_acr.jpg','LEO_8797_acr.jpg','LEO_8798_acr.jpg','LEO_8799_acr.jpg','LEO_8800_acr.jpg','LEO_8801_acr.jpg','LEO_8802_acr.jpg','LEO_8803_acr.jpg','LEO_8804_acr.jpg','LEO_8805_acr.jpg']

#for n in range(4927,4930):
#    image_set.append("DSC_{}_acr.jpg".format(n))
#for n in range(4931,4948):
#    image_set.append("DSC_{}_acr.jpg".format(n))
#for n in range(4951,4987):
#    image_set.append("DSC_{}_acr.jpg".format(n))
#for n in range(4990,5035):
#    image_set.append("DSC_{}_acr.jpg".format(n))
#for n in range(5038,5064):
#    image_set.append("DSC_{}_acr.jpg".format(n))
#for n in range(5188,5216):
#    image_set.append("DSC_{}_acr.jpg".format(n))
    
    
### Oppure utilizza un ciclo
### Primo dataset
#for n in range(9001,9006):
#    image_set.append("IMG_{}.jpg".format(n)) 
#### Secondo dataset
#for n in range(9065,9072):
#    image_set.append("IMG_{}.jpg".format(n)) 
#### Terzo dataset
#for n in range(8540,8566):
#    image_set.append("LEO_{}_acr.jpg".format(n)) 
#### Quarto dataset
#for n in range(8585,8611):
#    image_set.append("LEO_{}_acr.jpg".format(n)) 



### INPUT FOLDERS
desc_path_folder = r'C:\Users\Luscias\Desktop\buttare\prova\desc'
image_path_folder = r'C:\Users\Luscias\Desktop\buttare\prova\imgs'
gcp_path_folder = r'C:\Users\Luscias\Desktop\buttare\prova\empty'

### OUTPUT FOLDERS
converted_desc_path_folder = r'C:\Users\Luscias\Desktop\buttare\prova\colmap_desc'
raw_matches_folder = r'C:\Users\Luscias\Desktop\buttare\prova\matches'

### OTHER OPTIONS
res_factor = 1/1 #1500/6048 # Rapporto tra la larghezza dell'immagine usata in COLMAP e la larghezza dell'immagine su cui sono stati individuati i GCP
gcp_bool = False
descriptor = 'KeyNet' # 'D2Net' 'LFNet', 'ASLFeat', 'R2D2', 'KeyNet', 'SIFTopenCV', 'SuperPoint' or 'ORBopenCV' or 'PhotoMatch3DOM'
matching = 'BruteForce'
matching_distance = 'L2' # 'L2' or 'NORM_HAMMING'
matching_strategy = 'intersection' # 'intersection' or 'union' or 'unidirectional'
ratio_thresh_LRT = 0.999
print_debug = False
check = 'without_Lowe_ratio_test' # 'without_Lowe_ratio_test' or 'Lowe_ratio_test'
nmatches = 100000
crossCheck_bool = True
n_kp_input_SIFT = 8000 # Only with 'descriptor flag' = 'SIFTopenCV'
n_kp_input_ORB = 8000 # Only with 'descriptor flag' = 'ORBopenCV'



def main():
    print('image_set:  {}'.format(image_set))
  

# driver function 
if __name__=="__main__": 
    main()