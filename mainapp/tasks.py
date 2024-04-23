import os.path as osp
import cv2
import numpy as np
import torch 
from .RRDBNet_arch import RRDBNet
from celery import shared_task
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import io
from .models import Photo

model_path = os.path.join(os.getcwd(), 'mainapp', 'esrgan_model.pth')
device = torch.device('cpu')


model = RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()
model = model.to(device)
  
@shared_task(bind=True)  
def predict_image(self, data):
    path = os.path.join(os.getcwd(), 'media', 'low_res', data['low_res'].split("/")[-1])
    base = osp.splitext(osp.basename(path))[0]
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    
    output_image = cv2.imencode('.png', output)[1].tostring()
    file_buffer = io.BytesIO(output_image)
    file = InMemoryUploadedFile(file=file_buffer, field_name=None, name='{}.png'.format(base), content_type='image/png', size=len(output_image), charset=None)
    instance = Photo.objects.get(pk=data['id'])
    instance.status=True
    instance.high_res.save('{}.png'.format(base), file, save=True)
    return "Done"
