import io
from PIL import Image
from detect.detect import Detection
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, PlainTextResponse

app = FastAPI(
    title = "Detecção de Falhas em PCIs com YOLOv7",
    version = "0.0.1",
    contact = {
        "name": "Fabricio Guimaraes",
        "email": "fdcg@icomp.ufam.edu.br"
    }
)

detection = Detection(model_path="model/best.pt")

@app.get("/")
def index():

    return {
        "Title": "Detecção de Falhas em PCIs com YOLOv7",
        "Author": "Fabrício Guimarẽas",
        "Year": 2024,
        "GOTO": "http://localhost:4433/docs#/default/file_upload_predict_post"
    }

@app.post('/predict')
async def file_upload(
        my_file: UploadFile = File(...),
        to_txt: bool = False
):

    try:
        image = await my_file.read()

        image_PIL = Image.open(io.BytesIO(image))

        annotations = detection.load_image_to_prediction(
            image_PIL=image_PIL
        )

        annotated_img = detection.get_image_with_annotations(
            image_PIL=image_PIL, 
            annotations=annotations
        )

        imagem_byte = io.BytesIO()

        annotated_img.save(imagem_byte, format='PNG')
        
        imagem_byte.seek(0)    

    except Exception as e:
        return {"error": str(e)}
    
    else:
        if to_txt:
            content = [item for item in annotations['image_PIL']]
            content = "\n".join(content)
            return PlainTextResponse(content=content, media_type="text/plain")
        return StreamingResponse(content=imagem_byte, media_type="image/png")
    
    
# uvicorn main:app --reload --host 0.0.0.0 --port 4433
