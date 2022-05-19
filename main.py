from email.mime import image
from fastapi import FastAPI,File, UploadFile
from fastapi.responses import Response, RedirectResponse, StreamingResponse
import aiofiles
import cv2
import io


app = FastAPI()
count =[1]

@app.get("/")
async def root():
    return RedirectResponse("http://127.0.0.1:8000/docs")

@app.post("/upload_file")
async def upload_file(file : UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        new_filename = str(count[0]) + ".jpg"
        file_location = f"images/{new_filename}"
        count[0] = count[0] + 1 
        async with aiofiles.open(file_location, 'wb') as file_object:
            content = await file.read()       # async read
            await file_object.write(content)  # async write
        return {"Succeed upload image": new_filename , "saved at" : file_location}

@app.get("/get_file")
async def get_file(number):
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    res, res_data = cv2.imencode(".jpg", data_image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")

@app.get("/Flip")
async def image_Flip(number, type):
    if type == "v" :          #means vertically
        target_filename = str(number) + ".jpg"
        file_location = f"images/{target_filename}"
        data_image = cv2.imread(file_location)

        image = cv2.flip(data_image, 0)

        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")
    elif type == "h" :         #means Horizontally
        target_filename = str(number) + ".jpg"
        file_location = f"images/{target_filename}"
        data_image = cv2.imread(file_location)

        image = cv2.flip(data_image, 1)

        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.get("/Rotate")
async def image_Rotate(number, degree):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)

    height, width = data_image.shape[:2]
    center = (width/2, height/2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle = int(degree), scale=1)
    image = cv2.warpAffine(src = data_image, M = rotate_matrix, dsize=(width, height))

    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.get("/FixedGrayscale")
async def image_Fixed_Grayscale(number):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)

    image = cv2.cvtColor(data_image, cv2.COLOR_BGR2GRAY)

    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")

@app.get("/SpecifiedGrayscale")
async def image_Specified_Grayscale(number, Red, Green, Bule):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)

    gray =  0.0000
    gray += 0.2989 * int(Red)
    gray += 0.5870 * int(Green)
    gray += 0.1140 * int(Bule)
    image = cv2.cvtColor(data_image, int(gray))

    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


