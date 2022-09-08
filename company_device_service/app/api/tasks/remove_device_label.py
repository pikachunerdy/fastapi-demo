# from app.api.main import celery

# from schemas.mongo_models.device_models import MongoDevice


# async def remove_label_from_devices(label : str, company_id : int):
#     mongo_devices = MongoDevice.find(MongoDevice.company_id == company_id)
#     async for mongo_device in mongo_devices:
#         mongo_device.labels.remove(label)
#         mongo_device.save()

# @celery.task(name="remove_label_from_devices_task")
# async def remove_label_from_devices_task(label : str, company_id : int):
#     await remove_label_from_devices(label, company_id)
