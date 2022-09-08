from app.api.main import app
from schemas.mongo_models.account_models import MongoCompany
from libs.authentication.user_token_auth import  TokenData, token_authentication
from fastapi.params import Depends

from schemas.mongo_models.device_models import MongoDevice

@app.post('/company/device_label',tags = ['Company'])
async def  add_label(label : str, device_id : int, tokenData : TokenData = Depends(token_authentication)):
    company_id = tokenData.company_id
    company = await MongoCompany.get(company_id)
    if company is None:
        raise Exception
    if not (label in company.labels):
        company.labels[label] = []
    device = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    if device is not None:
        if not device.id in company.labels[label]:
            company.labels[label].append(device.id)
    await company.save()

@app.delete('/company/device_label',tags = ['Company'])
async def  delete_label(label : str, device_id : int, tokenData : TokenData = Depends(token_authentication)):
    company_id = tokenData.company_id
    company = await MongoCompany.get(company_id)
    if company is None:
        raise Exception
    if not (label in company.labels):
        company.labels[label] = []
    device = await MongoDevice.find(MongoDevice.device_id == device_id).first_or_none()
    if device is not None:
        company.labels[label].remove(device.id)
    await company.save()

@app.post('/company/label',tags = ['Company'])
async def  add_comapny_label(label : str, tokenData : TokenData = Depends(token_authentication)):
    company_id = tokenData.company_id
    company = await MongoCompany.get(company_id)
    if company is None:
        raise Exception
    print(label)
    if label == "":
        raise Exception
    if not (label in company.labels):
        print(label)
        company.labels[label] = []
    print(list(company.labels.keys()))
    await company.save()


@app.delete('/company/label', tags = ['Company'])
async def delete_company_label(label : str, tokenData : TokenData = Depends(token_authentication)):
    company_id = tokenData.company_id
    company = await MongoCompany.get(company_id)
    if company is None:
        raise Exception
    labels = company.labels
    labels.pop(label)
    company.labels = labels
    await company.save()

@app.get('/company/labels', tags=['Company'], response_model=list[str])
async def get_labels(tokenData : TokenData = Depends(token_authentication)) -> list[str]:
    company_id = tokenData.company_id
    company = await MongoCompany.get(company_id)
    if company is None:
        raise Exception
    # print(list(company.labels.keys()))
    return list(company.labels.keys())
