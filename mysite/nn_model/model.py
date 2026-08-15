import io
from pathlib import Path
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / 'model.pth'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

test_transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
])


class CifarCheckforward(nn.Module):

  def __init__(self):
    super().__init__()
    self.first = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(32, 64, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(64, 128, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
    )
    self.second = nn.Sequential(
        nn.Flatten(),
        nn.Linear(128 * 4 * 4, 256),
        nn.ReLU(),
        nn.Linear(256, 100),
    )

  def forward(self, image):
    image = self.first(image)
    image = self.second(image)
    return image


model = CifarCheckforward().to(device)

if MODEL_PATH.exists():
  model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
  model.eval()
else:
  raise FileNotFoundError(f'Файл весов не найден по пути: {MODEL_PATH}')


def predict_image(image_source):
  """Принимает путь к файлу (str/Path), файловый объект или bytes."""
  # Если переданы сырые байты (из await file.read()), оборачиваем в BytesIO
  if isinstance(image_source, bytes):
    image_source = io.BytesIO(image_source)

  img = Image.open(image_source).convert('RGB')
  img_tensor = test_transform(img).unsqueeze(0).to(device)

  with torch.no_grad():
    output = model(img_tensor)
    _, predicted_idx = torch.max(output, 1)

  return predicted_idx.item()


# Добавьте кортеж классов CIFAR-10 (если его ещё нет в файле)
classes = (
    'plane',
    'car',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck',
)


def predict_image(image_source):
  if isinstance(image_source, bytes):
    image_source = io.BytesIO(image_source)

  img = Image.open(image_source).convert('RGB')
  img_tensor = test_transform(img).unsqueeze(0).to(device)

  with torch.no_grad():
    output = model(img_tensor)
    _, predicted_idx = torch.max(output, 1)

  idx = predicted_idx.item()

  # Возвращаем имя класса по индексу
  if idx < len(classes):
    return classes[idx]
  return str(idx)  # Запасной вариант, если индекс больше 9