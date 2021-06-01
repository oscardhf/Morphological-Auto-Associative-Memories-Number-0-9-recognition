import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import walk
import skimage.io
import numpy as np
from skimage.transform import rescale, resize
from skimage.color import rgb2gray

def morph_max(W,x):
    C = np.zeros((W.shape[0],1))
    temp = np.zeros(W.shape[1])
    for i in range(W.shape[0]):
        for j in range(1):
            for k in range(W.shape[1]):
                temp[k] = W[i,k] + x[k]
            C[i,j] = np.max(temp)
    return C
def morph_min(W,x):
    C = np.zeros((W.shape[0],1))
    temp = np.zeros(W.shape[1])
    for i in range(W.shape[0]):
        for j in range(1):
            for k in range(W.shape[1]):
                temp[k] = W[i,k] + x[k]
            C[i,j] = np.min(temp)
    return C
def morph_product(x,y):
   
    temp = np.zeros((y.shape[0],y.shape[0]))
    for i in range(y.shape[0]):
        for j in range(y.shape[0]): 
             temp[j,i]=y[i] +x[j]                             
    return temp    

file_path = 'image' #folder name to contain image files

_, _, filenames = next(walk(file_path)) #get the names of image files

num_images = len(filenames) #number of image files
P = np.zeros((2500, num_images));#input array

print('working..Please wait...')
for i in range(num_images):
        
    img = skimage.io.imread(fname=file_path +'/' + filenames[i]) # read image
    gray = rgb2gray(img)
       
    s = gray.shape #get the size of image
    P[:,i] =  2*gray.reshape(s[0]*s[1])-1; #normalizes data to be either -1 or 1 #input array



temp = np.zeros((s[0]*s[1],s[0]*s[1],num_images))    
 

#calculate Morphological Auto Associative Memories(min)
for i in range(num_images):
    temp[:,:,i] = morph_product(P[:,i], -P[:,i].T)

W = np.min(temp, axis=2) #Morphological Auto Associative Memories
M =  np.max(temp,axis = 2) #Morphological Auto Associative Memories(max)
# test  with noisy inputs

#for i in range(num_images):
for i in range(10):    
    P[:,i] = P[:,i] - np.random.randint(2, size=P[:,i].shape)*0.3# add noise
    noise_image = P[:,i].reshape(s)
    
    y1 = morph_max(W,P[:,i])
    y2 = morph_min(M,P[:,i])

    out_image1 = y1.reshape(s)
    out_image2 = y2.reshape(s)
    
     
    plt.Figure()
    
    plt.subplot(1, 3, 1)
    plt.imshow(noise_image, cmap='gray')
    plt.gca().set_title('noise image')
    
    plt.subplot(1, 3, 2)
    plt.imshow(out_image1, cmap='gray')
    plt.gca().set_title('min matrix image')
    
    plt.subplot(1, 3, 3)
    plt.imshow(out_image2, cmap='gray')
    plt.gca().set_title('max matrix image')    

    plt.show()


print('done')









































