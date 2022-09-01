from app.api.main import app
from app.api.authentication.authentication import TokenData, token_authentication
from schemas.device_mongo_models.account_models import MongoCompany


@app.post('/company/label',tags['Company'])
async def  add_label(label : str, tokenData : TokenData = Depends(token_authentication)):
    company_id = int(tokenData.company_id)
    company = await MongoCompany.find(company_id = company_id).first()
    company.labels.append(label)
