import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor, maskrcnn_resnet50_fpn

from PIL import Image

import numpy as np

from detection import utils
from detection.engine import train_one_epoch, evaluate
from data.ts_load_dataset import TerraSentiaFrontalCameraDataset
from torchvision.transforms import PILToTensor
from torchvision.utils import draw_segmentation_masks
import torchvision.transforms.functional as F

from matplotlib import pyplot as plt

plt.rcParams["savefig.bbox"] = 'tight'
def show(imgs):
    if not isinstance(imgs, list):
        imgs = [imgs]
    fig, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = F.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

def get_model_instance_segmentation(num_classes):
    #Load an instance segmentation model pre-trained on COCO
    model = maskrcnn_resnet50_fpn(weights="DEFAULT")

    #Get the number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    #Replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    #Get the number of input features for the mask classifier
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    #Replace the mask predictor with a new one
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                       hidden_layer,
                                                       num_classes)

    return model

def inference():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print("Using device: ", device)

    num_classes = 2

    model = get_model_instance_segmentation(num_classes)
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, \
                                lr=0.005, 
                                momentum=0.9, 
                                weight_decay=0.0005)

    checkpoint = torch.load("models/model_500")
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']

    model.eval()

    img = Image.open("PNGImages/left006527.png").convert("RGB")
    img_tensor = PILToTensor()(img).unsqueeze_(0)/255
    predictions = model(img_tensor)
    
    masks = predictions[0]['masks'].detach().cpu().numpy()
    scores = predictions[0]['scores'].detach().cpu().numpy()
    
    selected_masks = np.zeros_like(masks[0])
    for i in range(len(masks[:20])):
        selected_masks += masks[i]

    f, axarr = plt.subplots(1, 2, figsize = (10, 20))
    axarr[0].imshow(img)
    axarr[1].imshow(selected_masks[0])
    plt.show()

    bool_selected_masks = selected_masks > 0.5
    plt.imshow(np.uint8(bool_selected_masks[0]))
    plt.show()

    show(draw_segmentation_masks(PILToTensor()(img), masks=torch.tensor(bool_selected_masks), alpha=0.7))
    plt.show()

if __name__ == "__main__":
    inference()