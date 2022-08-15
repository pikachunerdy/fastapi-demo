import asyncio

async def remove_label_from_devices(label : str, company_id : int):
    ...
    
import asyncio
@celery.task(name="remove_label_from_devices_task")
def remove_label_from_devices_task(label : str, company_id : int):
    asyncio.run(remove_label_from_devices(label, company_id))