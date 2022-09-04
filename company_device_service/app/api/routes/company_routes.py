from app.api.main import app
from schemas.mongo_models.account_models import MongoCompany
from libs.authentication.user_token_auth import  TokenData, token_authentication
from fastapi.params import Depends

@app.post('/company/label',tags = ['Company'])
async def  add_label(label : str, tokenData : TokenData = Depends(token_authentication)):
    company_id = int(tokenData.company_id)
    company = await MongoCompany.find(company_id = company_id).first_or_none()
    if company is None:
        raise Exception
    if not (label in company.labels):
        company.labels.append(label)
    await company.save()

@app.delete('/company/label', tags = ['Company'])
async def delete_label(label : str, tokenData : TokenData = Depends(token_authentication)):
    company_id = int(tokenData.company_id)
    company = await MongoCompany.find(company_id = company_id).first_or_none()
    if company is None:
        raise Exception
    labels = company.labels
    labels.remove(label)
    company.labels = labels
    # TODO add a task to remove labels from all devices
    await company.save()

@app.get('/company/labels', tags=['Company'], response_model=list[str])
async def get_labels(tokenData : TokenData = Depends(token_authentication)) -> list[str]:
    company_id = int(tokenData.company_id)
    company = await MongoCompany.find(company_id = company_id).first_or_none()
    if company is None:
        raise Exception
    return company.labels
