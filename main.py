from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse, StreamingResponse
import aiofiles , cv2 , io, numpy


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
        # Save as count++.jpg way
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
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg, charset=UTF-8")


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
async def image_Specified_Grayscale(number, Red, Green, Blue):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    gray =  (int(Red) + int(Green) + int(Blue))/3
    image = cv2.cvtColor(data_image, int(gray))
    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.get("/Saturate")
async def image_Saturate(number, factor : float):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    mean = numpy.uint8(cv2.mean(cv2.cvtColor(data_image, cv2.COLOR_BGR2GRAY))[0])
    img_deg = numpy.ones_like(numpy) * mean
    image = cv2.addWeighted(data_image, factor, img_deg, 1 - factor, 0.0)
    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.get("/Resize_X_Y")
async def image_Resize_X_Y(number, X : int , Y : int):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    image = cv2.resize(data_image, (X, Y))
    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.get("/Resize_Percent")
async def image_Resize_Percent(number, percent : float):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    new_width = int(data_image.shape[1] * (percent/100))
    new_height = int(data_image.shape[0] * (percent/100))
    image = cv2.resize(data_image, (new_width, new_height))
    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.get("/thumbnail")
async def image_thumbnail(number):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    image = cv2.resize(data_image,(256,256))
    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg") 


@app.get("/Rotate_left")
async def image_Rotate_left(number):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    image = cv2.rotate(data_image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")     


@app.get("/Rotate_right")
async def image_Rotate_right(number):          
    target_filename = str(number) + ".jpg"
    file_location = f"images/{target_filename}"
    data_image = cv2.imread(file_location)
    image = cv2.rotate(data_image, cv2.cv2.ROTATE_90_CLOCKWISE)
    res, res_data = cv2.imencode(".jpg", image)
    return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")       


@app.post("/api_flip")
async def api_flip(file : UploadFile , type):
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if type == "v":
            image = cv2.flip(data_image, 0)
        elif type =="h":
            image = cv2.flip(data_image, 1)
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_Rotate")
async def api_Rotate(file : UploadFile , degree): 
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        height, width = data_image.shape[:2]
        center = (width/2, height/2)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle = int(degree), scale=1)
        image = cv2.warpAffine(src = data_image, M = rotate_matrix, dsize=(width, height))
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")
    

@app.post("/api_FixedGrayscale")
async def api_FixedGrayscale(file : UploadFile): 
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(data_image, cv2.COLOR_BGR2GRAY)
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_SpecifiedGrayscale")
async def api_SpecifiedGrayscale(file : UploadFile, Red, Green, Blue):   
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray =  (int(Red) + int(Green) + int(Blue))/3
        image = cv2.cvtColor(data_image, int(gray))
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_Saturate")
async def api_Saturate(file : UploadFile, factor : float):    
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        mean = numpy.uint8(cv2.mean(cv2.cvtColor(data_image, cv2.COLOR_BGR2GRAY))[0])
        img_deg = numpy.ones_like(numpy) * mean
        image = cv2.addWeighted(data_image, factor, img_deg, 1 - factor, 0.0)
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_Resize_X_Y")
async def api_Resize_X_Y(file : UploadFile, X : int , Y : int):    
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.resize(data_image, (X, Y))
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_Resize_Percent")
async def api_Resize_Percent(file : UploadFile, percent : float):     
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        new_width = int(data_image.shape[1] * (percent/100))
        new_height = int(data_image.shape[0] * (percent/100))
        image = cv2.resize(data_image, (new_width, new_height))
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_thumbnail")
async def api_thumbnail(file : UploadFile):     
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.resize(data_image,(256,256))
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_Rotate_left")
async def api_Rotate_left(file : UploadFile):     
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.rotate(data_image, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")


@app.post("/api_Rotate_right")
async def api_Rotate_right(file : UploadFile):     
    if not file:
        return {"message": "No upload file sent"}
    elif file.content_type != "image/jpeg" :
        return {"Must be in jpg or jpeg, Here is your image type": file.content_type}
    else:
        content = await file.read()
        nparr = numpy.fromstring(content, numpy.uint8)
        data_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.rotate(data_image, cv2.cv2.ROTATE_90_CLOCKWISE)
        res, res_data = cv2.imencode(".jpg", image)
        return StreamingResponse(io.BytesIO(res_data.tobytes()), media_type="image/jpg")
    
