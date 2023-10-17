from fastapi import FastAPI
from api.models.dropoffPoint import DropoffPoint
import uvicorn

app = FastAPI()

@app.get("/points/", response_model=list[DropoffPoint])
def get_all_points() -> list[DropoffPoint]:
    return [
        {"name": "Reitoria", "location": "Departamento 25", "coordinates": "40.631417730224, -8.657526476133642", "image": "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_3090.jpg&width=1200"},
        {"name": "CP", "location": "Departamento 23", "coordinates": "40.62957166653202, -8.655231694880136", "image": "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F001%2F838%2Foriginal.jpg&width=1200"},
        {"name": "DETI", "location": "Departamento 4", "coordinates": "40.63331148617483, -8.659589862642955", "image": "https://api-assets.ua.pt/files/imgs/000/000/380/original.jpg"},
        {"name": "Cantina de Santiago", "location": "Departamento 6", "coordinates": "40.630659968175124, -8.659097986459223", "image": "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_12306.jpg&width=1200"},
        {"name": "Cantina do Crasto", "location": "Departamento M", "coordinates": "40.62450887522072, -8.656864475040406", "image": "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_2828.JPG&width=1200"},
        {"name": "Pavilhão Aristides Hall", "location": "Departamento E", "coordinates": "40.63000326980208, -8.654180591479575", "image": "https://d1bvpoagx8hqbg.cloudfront.net/originals/bem-vindos-a-ua-399bd8560914b519d0dca3fc57bd0afe.jpg"},
    ]

if __name__  == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)