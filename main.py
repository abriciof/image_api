from fastapi import FastAPI, HTTPException, Path, UploadFile, Form, File
from fastapi.responses import FileResponse, Response, StreamingResponse
from PIL import Image
import io
from augmentation.utils.dataaugmentation import *

app = FastAPI(
    title="PCI Api",
    version= "0.0.1",
    contact={
        "name": "Fabricio Guimaraes",
        "email": "fdcg@icomp.ufam.edu.br"
    }
)

@app.get("/")
def index():
    return {"Author":"Fabrício Guimarẽas",
            "Year": 2024,}

@app.post('/file')
async def file_upload(
        my_file: UploadFile = File(...),
):
        #     first: str = Form(...),
        # second: str = Form("default value  for second")
    try:
        image = await my_file.read()
        # image_PIL = Image.open(io.BytesIO(image))
        # image_PIL.thumbnail((50,50))
        # # image_bytes = io.BytesIO()
        # image_PIL.save(image, format="PNG")
        # image.seek(0)
# 

    except Exception as e:
        return {"error": str(e)}
    

    return Response(content=image, media_type="image/png")


    # return {
    #     "name": my_file.filename,
    #     "first": first,
    #     "second": second
    # }

@app.get("/image",
         responses={
             200 : {
                "content" :
                    {
                        "image/png" : {}
                     }
                }
        }, 
        response_class=Response
)
def get_image():
    with open("D:\\fabri\\Documentos\\Databases\\PCB_DATASET\\images\\Missing_hole\\01_missing_hole_01.jpg", "rb") as image:
        f = image.read()
        # b = bytearray(f).decode()


    image_bytes: bytes = f
    # ❌ Don't d = io.BytesIO(image_bytes)
    return Response(content=image_bytes, media_type="image/png")

@app.post('/augmentation')
def augmentation(images_path: str, labels_path: str, output_path: str, nprocess: int = 2):
    data_augmentation = Data_Augmentation(output_path)
    data_augmentation.load_data(
    images_path, labels_path)
    data_augmentation.run(n_processing=nprocess)
    data_augmentation.save_data()
    return {
        "message":"augmentation ok"
    }