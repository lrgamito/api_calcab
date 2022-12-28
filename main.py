from fastapi import FastAPI
from pydantic import BaseModel
from math import ceil

app = FastAPI()

# Create model input
class Project(BaseModel):
    major_hor_dist: float
    minor_hor_dist: float
    assent: float
    descent: float
    telec_leftover: float
    worksp_leftover: float
    quantity: int
    security_percent: float | None = None
    price_per_meter: float | None = None
    box_qtt_in_meters: float | None = None

#Create model output
class Output(BaseModel):
    cable_qtt_in_meters: float
    box_quantity: int | None = None
    total_price: float | None = None

#Calculate
def calculate(input: Project):
    
    calc = (((input.major_hor_dist + input.minor_hor_dist) / 2 ) + input.assent + input.descent + input.telec_leftover + input.worksp_leftover) * input.quantity
    calc += (calc * input.security_percent / 100)

    bc = ceil(calc / input.box_qtt_in_meters)
    tp = calc * input.price_per_meter

    out = Output(cable_qtt_in_meters = calc, box_quantity = bc, total_price = "{:.2f}".format(tp))
      
    return out

#Default Route
@app.post("/", response_model=Output)
async def root(project: Project):

    # Calculate and return
    c = calculate(project)

    return c