# Container Nameplate Text Recognition: Large-Scale Annotated Dataset and Advanced Detection Network
<img width="411" alt="image" src="https://github.com/user-attachments/assets/32ce5c88-1f29-4135-8a54-b4548ed836fa">\\


<img width="415" alt="image" src="https://github.com/user-attachments/assets/86ea1ee0-2fc7-414e-a385-ebcfcb1c014c">

  To obtain the Container Nameplate dataset: 1. Use the school's email address (edu, stu, etc.) and send an email to: yikuizhai@126.com 2. Sign the relevant agreement to ensure that it will only be used for scientific research and not for commercial purposes.A scanned version of the agreement that requires a handwritten signature. Both Chinese and English signatures are acceptable. 3. Authorization will be obtained in 1-3 days. (Notice: If you use this dataset as the benchmark dataset for your paper, please cite the paper in eula.pdf)

#The text detection benchmark of CNP dataset

Method|Label|Backbone|Hmean|Precision|Recall

PCENet|Polygon|Resnet50|0.833|0.838|0.828

SAST|Polygon|Resnet50|0.855|0.831|0.882

EAST|Polygon|Resnet50|0.892|0.886|0.898

Deformable DETR|Rectangular|Resnet50|0.747|0.821|0.783

RT-DETR|Rectangular|Resnet50|0.758|0.815|0.785

Ours|Polygon Point|Resnet50|0.963|0.959|0.966



#The text recognition benchmark of CNP dataset

Method|Optimizer|Backbone|Accuracy

SVTR|Adam|Resnet50|0.921

NRTR|Adam|NRTR_MTB|0.890

ABI-Net|Adam|Resnet45|0.942

Star-Net|Adam|MobileNetv3|0.873

SRN-Net|Adam|Resnet50|0.960

The code will be released soon.
