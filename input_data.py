#The aim of this project is to use TensorFlow to process our own data.
#    - input_data.py:  read in data and generate batches
#    - model: build the model architecture
#    - training: train

# I used Anaconda3 with Python 3.6, TensorFlow 1.0*, other OS should also be good.
# With current settings, 10000 traing steps needed 50 minutes on my laptop.


# data: cats vs. dogs from Kaggle
# Download link: https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition/data
# data size: ~540M

# How to run?
# 1. run the training.py once
# 2. call the run_training() in the console to train the model.

# Note: 
# it is suggested to restart your kenel to train the model multiple times 
#(in order to clear all the variables in the memory)
# Otherwise errors may occur: conv1/weights/biases already exist......


#%%
#
import tensorflow as tf
import numpy as np
import os
#%%

# you need to change this to your data directory
#train_dir = 'F:/deepLearningProgramExcise/tensorflow/cats_vs_dogs/data/train'

def get_files(file_dir):
    '''
    Args:
        file_dir: file directory
    Returns:
        list of images and labels
    '''
    cats = []
    label_cats = []
    dogs = []
    label_dogs = []
    for file in os.listdir(file_dir):
        name = file.split(sep = '.')
        if name[0] =='cat':
            cats.append(file_dir + '/' + file)
            label_cats.append(0)
        else:
            dogs.append(file_dir + '/' +file)
            label_dogs.append(1)
    print('There are %d cats\nThere are %d dogs' %(len(cats),len(dogs)))

    image_list = np.hstack((cats,dogs))
    label_list = np.hstack((label_cats,label_dogs))

    temp = np.array([image_list,label_list])
    temp = temp.transpose()
    np.random.shuffle(temp)

    image_list = list(temp[:,0])
    label_list= list(temp[:,1])
    label_list = [int(i) for i in label_list]

    return image_list,label_list
#%%

def get_batch(image, label, image_W, image_H, batch_size, capacity):
    '''
    Args:
        image: list type, returned by get_files(file_dir)
        label: list type,returned by get_files(file_dir)
        image_W: image width
        image_H: image height
        batch_size: batch size
        capacity: the maximum elements in queue
    Returns:
        image_batch: 4D tensor [batch_size, width, height, 3], dtype=tf.float32
        label_batch: 1D tensor [batch_size], dtype=tf.int32
    '''
    # transfer to tf can recognize
    image = tf.cast(image, tf.string)
    label = tf.cast(label, tf.int32)

    # make an input queue,combine the image and its label in a list
    # tf.train.slice_input_producer(
#     tensor_list,
#     num_epochs=None,
#     shuffle=True,
#     seed=None,
#     capacity=32,
#     shared_name=None,
#     name=None
# )
    input_queue = tf.train.slice_input_producer([image, label])
    # get data from input_queue
    label = input_queue[1]
    image_contents = tf.read_file(input_queue[0])  # read the image use the tf.read_file()
    # use tf.image.decoder_jpeg() to decoder image,if the image format is not jpeg,transfer
    image = tf.image.decode_jpeg(image_contents, channels=3)
    
    ######################################
    # data argumentation should go to here
    # here did not do this work
    ######################################
    # tf.image.resize_image_with_crop_or_pad(image, target_height, target_width):
    # crop or pad from center;you can also use resize_images() to scale
    #image = tf.image.resize_image_with_crop_or_pad(image, image_W, image_H)

    image = tf.image.resize_images(image, [image_H, image_W], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    image = tf.cast(image, tf.float32)
    
    # if you want to test the generated batches of images, you might want to comment the following line.
    # image = tf.image.per_image_standardization(image) will give the Error:
    #ValueError: Floating point image RGB values must be in the 0..1 range,you can comment this line
    # But do not comment it when trainning
    image = tf.image.per_image_standardization(image)# subtract mean,then divided by var
    # generate the batches: tf.train.batch() or tf.train.shuffle_batch(),the second will harm the order
    image_batch, label_batch = tf.train.batch([image, label],
                                                batch_size= batch_size,
                                                num_threads= 64,
                                                capacity = capacity)
    
    #you can also use shuffle_batch 
#    image_batch, label_batch = tf.train.shuffle_batch([image,label],
#                                                      batch_size=BATCH_SIZE,
#                                                      num_threads=64,
#                                                      capacity=CAPACITY,
#                                                      min_after_dequeue=CAPACITY-1)
    
    label_batch = tf.reshape(label_batch, [batch_size])
    image_batch = tf.cast(image_batch, tf.float32)
    
    return image_batch, label_batch


 
#%% TEST
# To test the generated batches of images
# When training the model, DO comment the following codes




#import matplotlib.pyplot as plt
#
#BATCH_SIZE = 2
#CAPACITY = 256
#IMG_W = 208
#IMG_H = 208
#
##train_dir ='F:\deepLearningProgramExcise\tensorflow\cats_vs_dogs\data\train'
#train_dir = 'F:/deepLearningProgramExcise/tensorflow/cats_vs_dogs/data/train'
#
#
#image_list, label_list = get_files(train_dir)
#image_batch, label_batch = get_batch(image_list, label_list, IMG_W, IMG_H, BATCH_SIZE, CAPACITY)
#
#with tf.Session() as sess:
#   i = 0 # set the index to control the number of image,because too many iamges
#   # tf.train.Coordinator() and tf.train.start_queue_runners() :watch the state the queue,dequeue
#   # and inqueue repeatly
#   coord = tf.train.Coordinator()
#   threads = tf.train.start_queue_runners(coord=coord)
#
#   try:
#       while not coord.should_stop() and i<1:
#
#           img, label = sess.run([image_batch, label_batch])
#
#           # just test one batch
#           for j in np.arange(BATCH_SIZE):
#               print('label: %d' %label[j])
#               plt.imshow(img[j,:,:,:])
#               plt.show()
#           i+=1
#
#   except tf.errors.OutOfRangeError:
#       print('done!')
#   finally:
#       coord.request_stop()
#   coord.join(threads)



#%%
#
#
#

