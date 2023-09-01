from fastapi import FastAPI, HTTPException, Path, UploadFile, Form, File
from fastapi.responses import FileResponse, Response, StreamingResponse
from PIL import Image
import io
app = FastAPI()

@app.get("/")
def index():
    
    return {"Author":"Fabrício Guimarẽas",
            "Year": 2023,}

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


    return {
        "name": my_file.filename,
        "first": first,
        "second": second
    }

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
    with open("/home/fabricioguimaraes/Documentos/fabricio/archive/PCB_DATASET/images/Missing_hole/01_missing_hole_02.jpg", "rb") as image:
        f = image.read()
        # b = bytearray(f).decode()


    image_bytes: bytes = f
    # ❌ Don't d = io.BytesIO(image_bytes)
    return Response(content=image_bytes, media_type="image/png")
