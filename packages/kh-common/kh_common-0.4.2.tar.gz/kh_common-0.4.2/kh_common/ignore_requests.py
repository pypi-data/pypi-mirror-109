from aiohttp import ClientTimeout, request as async_request


async def post(url: str, json=None, data=None, timeout=30, retries=3) :
	for attempt in range(retries) :
		try :
			async with async_request('POST', url, json=json, data=data, timeout=ClientTimeout(timeout)) as response :
				response.raise_for_status()
				return response

		except :
			if attempt + 1 >= retries :
				raise


async def get(url: str, timeout=30, retries=3) :
	for attempt in range(retries) :
		try :
			async with async_request('GET', url, timeout=ClientTimeout(timeout)) as response :
				response.raise_for_status()
				return response

		except :
			if attempt + 1 >= retries :
				raise
