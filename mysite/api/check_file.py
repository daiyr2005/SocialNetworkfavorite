from fastapi import APIRouter, File, HTTPException, UploadFile, status
from mysite.nn_model.model import predict_image

router = APIRouter(prefix="/check", tags=["Check"])

# В CIFAR-10 класс самолета называется "plane", а не "airplane"
FORBIDDEN_CLASSES = {"plane", "car", "bird"}


@router.post("/")
async def check_file(file: UploadFile = File(...)):
  # Передаем файловый поток file.file напрямую без чтения в bytes
  predicted_class = predict_image(file.file)

  if predicted_class in FORBIDDEN_CLASSES:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Мындай контенти жуктогону болбойт",
    )

  return {"result": "Успешно", "class": predicted_class}