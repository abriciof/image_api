import yolov7
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class Detection:
    def __init__(
            self, 
            model_path = "best.pt",
            conf = 0.25, 
            iou = 0.45, 
            classes = None
        ):

        self.model_path = model_path
        self.conf = conf
        self.iou = iou
        self.classes = classes
        self.load_model()
        self.categorias = {
            '0': 'nothing',
            '1': 'missing_hole',
            '2': 'mouse_bite',
            '3': 'open_circuit',
            '4': 'short',
            '5': 'spur',
            '6': 'spurious_copper'
        }

    def load_model(self):
        self.model = yolov7.load(self.model_path)
        self.model.conf = self.conf  
        self.model.iou = self.iou
        self.model.classes = self.classes

    def prediction_to_annotations(
            self,
            predictions, 
            pathname, 
            size, 
            to_file = False,
            output_dir = "annotations",
    ):

        results = []

        for prediction in predictions:

            x1, y1, x2, y2, score, category = prediction

            img_width, img_height = size

            x_center = (x1 + x2) / 2 / img_width
            y_center = (y1 + y2) / 2 / img_height
            width = (x2 - x1) / img_width
            height = (y2 - y1) / img_height

            result = f"{int(category)} {x_center} {y_center} {width} {height}"

            results.append(f"{result}")

        if to_file:

            Path(output_dir).mkdir(parents=True, exist_ok=True)

            annotation_file = f"{output_dir}/{pathname}.txt"
    
            with open(annotation_file, 'w') as f:
                
                for linha in results:

                    f.write(f"{linha}\n")

        return results

    def load_image_to_prediction(
            self, 
            image_PIL: Image = None, 
            image_filename: str = "images/01_mouse_bite_02.jpg"
    ):
       
        if not image_PIL: image_PIL = Image.open(Path(image_filename))
        
        imgs_pils = [image_PIL]
        imgs_sizes = [image_PIL.size]
        imgs_paths = ["image_PIL"]
        image_filename = "image_PIL"

        results = self.model(imgs_pils, size=640, augment=False)

        annotations = {}

        for pathname, size, prediction in zip(
            imgs_paths, 
            imgs_sizes, 
            results.pred
        ):
            annotations[image_filename] = self.prediction_to_annotations(
                predictions=prediction, 
                pathname=pathname, 
                size=size,
                to_file=True
            )

        return annotations
    
    def get_image_with_annotations(self, image_PIL: Image, annotations: dict):

        img = image_PIL.convert('RGB')

        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 50)

        except IOError:
            font = ImageFont.load_default()

        for line in annotations['image_PIL']:
            
            category, x_center, y_center, width, height = map(
                float, 
                line.strip().split()
            )

            category_tag = self.categorias[str(int(category))]

            img_width, img_height = img.size

            x_center *= img_width
            y_center *= img_height
            width *= img_width
            height *= img_height

            x1 = x_center - width / 2
            y1 = y_center - height / 2
            x2 = x_center + width / 2
            y2 = y_center + height / 2

            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x2, y2), category_tag, fill="red", font=font)
        
        return img

if __name__ == "__main__":
    
    # Objetos
    dt = Detection()
    
    # Minha imagem PIL
    imagem = Path("detect/images/01_mouse_bite_02.jpg")
    imagem = Image.open(imagem)

    # Obtendo anotações
    annotations = dt.load_image_to_prediction(
        image_PIL=imagem
    )
    
    # Desenhando resultados
    annotated_img = dt.get_image_with_annotations(
        image_PIL=imagem, 
        annotations=annotations
    )
    
    # Mostrando no Fotos
    annotated_img.show()
