import os
import numpy as np
from scipy import signal
#from scipy.ndimage import correlate
from PIL import Image


def SSD(ref, templ, silent):
    '''
    ref e templ are np.array()
    '''
    if silent == 'False': print("np.max(ref)", np.max(ref))
    if silent == 'False': print("np.min(ref)", np.min(ref))
    if silent == 'False': print("np.max(templ)", np.max(templ))
    if silent == 'False': print("np.min(templ)", np.min(templ))
    
    ref_row = ref.shape[0]
    ref_col = ref.shape[1]
    templ_row = templ.shape[0]
    templ_col = templ.shape[1]
    
    ssd_matrix = np.empty((ref_row-templ_row+1, ref_col-templ_col+1))
    ssd_row = ssd_matrix.shape[0]
    ssd_col = ssd_matrix.shape[1]
    
    for r in range(0, ssd_row):
        for c in range(0, ssd_col):
            ref_cut = ref[r:r+templ_row, c:c+templ_col]
           
            #ref_cut -= ref_cut.mean()
            #ref_cut = ref_cut / np.std(ref_cut)
            #print("ref_cut.mean(), ref_cut.std()", ref_cut.mean(), ref_cut.std())
            #templ -= templ.mean()
            #templ = templ / np.std(templ)            
            #print("templ.mean(), templ.std()", templ.mean(), templ.std())

            ssd = np.sum((ref_cut-templ)**2)
            ssd_matrix[r,c] = ssd
    
    if silent == 'False': print("ssd_matrix.shape", ssd_matrix.shape)
    if silent == 'False': print("np.max(ssd_matrix)", np.max(ssd_matrix))
    if silent == 'False': print("np.min(ssd_matrix)", np.min(ssd_matrix))
    y, x = np.unravel_index(np.argmin(ssd_matrix), ssd_matrix.shape)  # find the match
    
    ssd_matrix = ssd_matrix / np.max(ssd_matrix) * 255.0
    ssd_matrix = Image.fromarray(ssd_matrix)
    if silent == 'False': ssd_matrix.show()
    
    
    ref[y+int((templ_row-1)/2), x+int((templ_col-1)/2)] = 0
    ref = Image.fromarray(ref)
    if silent == 'False': ref.show()
    
    y, x = y+int((templ_row-1)/2), x+int((templ_col-1)/2)
    
    return y, x


def NCC(ref, templ, silent):
    '''
    Normalized Cross Correlation
    https://www.researchgate.net/profile/Wen-Gao-11/publication/224641323_Image_Matching_by_Normalized_Cross-Correlation/links/54bd11b40cf218da939104e0/Image-Matching-by-Normalized-Cross-Correlation.pdf?_sg%5B0%5D=qZzyt3qsKS2Kg4gAL54pYHhZZIB8cWBRHcSn3oWGuhOw6o6P-IS_9ZXQR9vAKMvN2wkYaZtXdRQ8Xq5W9Jfi9w.ldWU6W6eYOJSXpIDeayWWUJynXRI6OZsrVESkcvhU8jOag4-6WzOFgrj304tLXxI7Krpd3cQIp7bDT71bLMVTA&_sg%5B1%5D=TbrqXOluFMOFLDUiKsVKrjcanxWzzfGKtmCl857vQqJoOsAkarKbCxeYKYou5eUpU9pQoBlo3OGQzaLRZ5MlamYYKZJfqyER5SUC_j-8MY9Z.ldWU6W6eYOJSXpIDeayWWUJynXRI6OZsrVESkcvhU8jOag4-6WzOFgrj304tLXxI7Krpd3cQIp7bDT71bLMVTA&_iepl=
    '''
    if silent == 'False': print("np.max(ref)", np.max(ref))
    if silent == 'False': print("np.min(ref)", np.min(ref))
    if silent == 'False': print("np.max(templ)", np.max(templ))
    if silent == 'False': print("np.min(templ)", np.min(templ))
    
    ref_row = ref.shape[0]
    ref_col = ref.shape[1]
    templ_row = templ.shape[0]
    templ_col = templ.shape[1]
    
    ncc_matrix = np.empty((ref_row-templ_row+1, ref_col-templ_col+1))
    ssd_row = ncc_matrix.shape[0]
    ssd_col = ncc_matrix.shape[1]
    
    for r in range(0, ssd_row):
        for c in range(0, ssd_col):
            ref_cut = ref[r:r+templ_row, c:c+templ_col]
           
            #ref_cut -= ref_cut.mean()
            #ref_cut = ref_cut / np.std(ref_cut)
            #print("ref_cut.mean(), ref_cut.std()", ref_cut.mean(), ref_cut.std())
            #templ -= templ.mean()
            #templ = templ / np.std(templ)            
            #print("templ.mean(), templ.std()", templ.mean(), templ.std())

            ncc = np.sum((ref_cut-ref_cut.mean())*(templ-templ.mean()))/(ref_cut.std()*templ.std()) # Manca normalizzazione rispetto alla dimensione della finestra al denominatore, vedere paper
            ncc_matrix[r,c] = ncc
    
    if silent == 'False': print("ncc_matrix.shape", ncc_matrix.shape)
    if silent == 'False': print("np.max(ncc_matrix)", np.max(ncc_matrix))
    if silent == 'False': print("np.min(ncc_matrix)", np.min(ncc_matrix))
    y, x = np.unravel_index(np.argmax(ncc_matrix), ncc_matrix.shape)  # find the match
    
    ncc_matrix = ncc_matrix / np.max(ncc_matrix) * 255.0
    ncc_matrix = Image.fromarray(ncc_matrix)
    if silent == 'False': ncc_matrix.show()
    
    
    ref[y+int((templ_row-1)/2), x+int((templ_col-1)/2)] = 0
    ref = Image.fromarray(ref)
    if silent == 'False': ref.show()
    
    y, x = y+int((templ_row-1)/2), x+int((templ_col-1)/2)
    
    return y, x

################################################################################
# MAIN
def main():
    print("Patch Cross Correlation")
    patch1_path = r"C:\Users\Luscias\Desktop\Graz\details\patch\0151.png"
    patch2_path = r"C:\Users\Luscias\Desktop\Graz\details\patch\0152.png"
    #patch1_path = r"C:\Users\Luscias\Desktop\Graz\details\patch\prova1.png"
    #patch2_path = r"C:\Users\Luscias\Desktop\Graz\details\patch\prova2.png"
    patch1 = Image.open(patch1_path)
    patch1 = patch1.convert("L")
    #patch1 = patch1.resize((1000,1000),Image.BICUBIC)
    #patch1 = patch1.crop((0, 0, 10, 10))
    patch1.show()
    
    patch2 = Image.open(patch2_path)
    
    patch2 = patch2.convert("L")
    #patch2 = patch2.crop((0, 0, 4, 4))
    patch2.show()
    
    patch1 = np.array(patch1, dtype = 'float')
    patch2 = np.array(patch2, dtype = 'float')
    
    #patch1 -= patch1.mean()
    #patch2 -= patch2.mean()
    
    #SSD(patch1, patch2)
    NCC(patch1, patch2)
    quit()
    
    
    
    print("patch1.shape", patch1.shape)
    print("np.max(patch1)", np.max(patch1))
    print("np.min(patch1)", np.min(patch1))
    print("patch2.shape", patch2.shape)
    print("np.max(patch2)", np.max(patch2))
    print("np.min(patch2)", np.min(patch2))
    #corr = signal.correlate(patch1, patch2, mode='valid')
    corr = signal.correlate2d(patch1, patch2, mode = 'same')
    y, x = np.unravel_index(np.argmax(corr), corr.shape)  # find the match
    print("y, x", y, x)
    #corr = correlate(patch1, patch2)
    print("corr.shape", corr.shape)
    print("np.max(corr)", np.max(corr))
    print("np.min(corr)", np.min(corr))
    corr = Image.fromarray(corr)
    corr.show()

    
    corr = np.array(corr)
    M = np.max(corr)
    with np.nditer(corr, op_flags=['readwrite']) as c:
        for x in c:
            if x == M:
                x[...] = 255
            else:
                x[...] = 100
    corr = Image.fromarray(corr)
    corr.show()

################################################################################
# DRIVER FUNCTION 
if __name__=="__main__": 
    main()