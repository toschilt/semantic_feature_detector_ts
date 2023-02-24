import json
import numpy as np
import matplotlib.pyplot as plt

def get_training_data(file_name):
    training_data = None
    with open(file_name, "r") as input:
        training_data = json.load(input)

    epochs = []
    lr = []
    loss = []
    loss_classifier = []
    loss_box_reg = []
    loss_mask = []
    loss_objectness = []
    loss_rpn_box_reg = []

    for epoch in training_data:
        epochs.append(int(epoch))
        epoch_data = training_data[epoch]
        
        lr.append(epoch_data['lr'])
        loss.append(epoch_data['loss'])
        loss_classifier.append(epoch_data['loss_classifier'])
        loss_box_reg.append(epoch_data['loss_box_reg'])
        loss_mask.append(epoch_data['loss_mask'])
        loss_objectness.append(epoch_data['loss_objectness'])
        loss_rpn_box_reg.append(epoch_data['loss_rpn_box_reg'])

    return {'epochs': epochs, 
            'lr':lr,
            'loss':loss,
            'loss_classifier':loss_classifier,
            'loss_box_reg':loss_box_reg,
            'loss_mask':loss_mask,
            'loss_objectness': loss_objectness,
            'loss_rpn_box_reg': loss_rpn_box_reg}

def get_testing_data(file_name):
    testing_data = None
    with open(file_name, "r") as input:
        testing_data = json.load(input)

    epochs = []
    bbox = []
    segm = []

    for epoch in testing_data:
        epochs.append(int(epoch))
        bbox.append(testing_data[epoch]['bbox'])
        segm.append(testing_data[epoch]['segm'])

    return {'epochs': epochs,
            'bbox': np.array(bbox),
            'segm': np.array(segm)}

def plot_training_loss_metrics_separated(training_data):
    plt.figure()
    plt.suptitle('Training losses', fontsize=18)
    plt.subplots_adjust(top=0.935,
                        bottom=0.06,
                        left=0.04,
                        right=0.96,
                        hspace=0.26,
                        wspace=0.155)
                        
    loss_metrics = list(training_data.keys())[2:]
    for i, loss_metric in zip(range(len(loss_metrics)), loss_metrics):
        plt.subplot(3, 2, i + 1)
        plt.plot(training_data['epochs'], training_data[loss_metric])
        plt.title(loss_metric)

    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

def plot_training_loss_metrics_together(training_data):
    plt.figure()
    plt.suptitle('Training losses', fontsize=18)
    
    loss_metrics = list(training_data.keys())[2:]
    for loss_metric in loss_metrics:
        plt.plot(training_data['epochs'], training_data[loss_metric], label=loss_metric)
        
    plt.legend()
    plt.show()

def plot_training_loss_and_lr(training_data):
    fig, ax1 = plt.subplots()
    plt.suptitle('Training losses and learning rate', fontsize=18)
    
    loss_metrics = list(training_data.keys())[2:]
    for loss_metric in loss_metrics:
        ax1.plot(training_data['epochs'], training_data[loss_metric], label=loss_metric)

    ax1.legend()

    ax2=ax1.twinx()
    ax2.set_yscale('log')
    ax2.plot(training_data['epochs'], training_data['lr'], 'b', label='lr')
        
    ax2.legend(loc=0)
    plt.show()

def plot_learning_rate(training_data):
    plt.figure()
    plt.suptitle('Learning rate', fontsize=18)
    plt.plot(training_data['epochs'], training_data['lr'])
    plt.yscale('log')
    plt.show()

#type = 'bbox' or 'segm'
def plot_testing_metrics(type, testing_data):
    plt.figure()
    if type == 'bbox':
        plt.suptitle('Bounding box testing metrics', fontsize=18)
    elif type == 'segm':
        plt.suptitle('Segmentation mask testing metrics', fontsize=18)
    
    plt.subplots_adjust(top=0.935,
                        bottom=0.06,
                        left=0.04,
                        right=0.96,
                        hspace=0.26,
                        wspace=0.155)

    plt.subplot(3, 2, 1)
    plt.plot(testing_data['epochs'], testing_data[type][:,0])
    plt.title('AP at IoU=.50:.05:.95')

    plt.subplot(3, 2, 3)
    plt.plot(testing_data['epochs'], testing_data[type][:,1])
    plt.title('AP at IoU=.50')

    plt.subplot(3, 2, 5)
    plt.plot(testing_data['epochs'], testing_data[type][:,2])
    plt.title('AP at IoU=.75')

    plt.subplot(3, 2, 2)
    plt.plot(testing_data['epochs'], testing_data[type][:,6])
    plt.title('AR given 1 detection per image')

    plt.subplot(3, 2, 4)
    plt.plot(testing_data['epochs'], testing_data[type][:,7])
    plt.title('AR given 10 detections per image')

    plt.subplot(3, 2, 6)
    plt.plot(testing_data['epochs'], testing_data[type][:,8])
    plt.title('AR given 100 detections per image')
    
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

def plot_testing_metrics_comparatively(type, testing_data):
    plt.figure()
    
    if type == 'bbox':
        plt.suptitle('Bounding box testing metrics', fontsize=18)
    elif type == 'segm':
        plt.suptitle('Segmentation mask testing metrics', fontsize=18)

    plt.subplot(2, 1, 1)
    plt.plot(testing_data['epochs'], testing_data[type][:,0], label='AP at IoU=.50:.05:.95')
    plt.plot(testing_data['epochs'], testing_data[type][:,1], label='AP at IoU=.50')
    plt.plot(testing_data['epochs'], testing_data[type][:,2], label='AP at IoU=.75')
    plt.title('Average Precision (AP)')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(testing_data['epochs'], testing_data[type][:,6], label='AR given 1 detection per image')
    plt.plot(testing_data['epochs'], testing_data[type][:,7], label='AR given 10 detections per image')
    plt.plot(testing_data['epochs'], testing_data[type][:,8], label='AR given 100 detections per image')
    plt.title('Average Recall (RP)')
    plt.legend()
    
    plt.show()

if __name__ == "__main__":
    training_data = get_training_data("train_log.json")
    testing_data = get_testing_data("test_log.json")

    plot_training_loss_metrics_separated(training_data)
    plot_training_loss_metrics_together(training_data)
    plot_training_loss_and_lr(training_data)
    plot_learning_rate(training_data)
    plot_testing_metrics('bbox', testing_data)
    plot_testing_metrics('segm', testing_data)
    plot_testing_metrics_comparatively('bbox', testing_data)
    plot_testing_metrics_comparatively('segm', testing_data)