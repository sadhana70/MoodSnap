from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import numpy as np
from PIL import Image
import io
import tensorflow as tf  # Assuming you're using TensorFlow for your model

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load your pre-trained model
model = tf.keras.models.load_model("model/imageclassifiernew.h5")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    # Read and preprocess the image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.resize((256, 256))  # Adjust size according to your model's input
    image_array = np.asarray(image)  # Convert to numpy array
    
# Check if the image is grayscale and convert to RGB if necessary
    if len(image_array.shape) == 2:  # Grayscale
        image_array = np.stack((image_array,) * 3, axis=-1)  # Convert to RGB

    # Ensure the image has 3 color channels
    if image_array.shape[-1] != 3:
        raise ValueError("Input image must have 3 color channels (RGB)")



    # Normalize the image (0-1 range)
    image_array = image_array / 255.0  
   
    image_array = np.expand_dims(image_array, axis=0)
    print("image shape:", image_array.shape)
    # Make prediction
    prediction = model.predict(image_array)
    result = "Sad" if prediction[0][0] > 0.5 else "Happy"

    return {"result": result, "image_url": f"/static/uploads/{file.filename}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)