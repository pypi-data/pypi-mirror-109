import requests

from pgsaw.Store import Store

class AldiUS(Store):
	__csrfToken = None
	__instacartSessionId = None
	__storeId = None
	__userAgent = None

	def __init__(self, csrfToken, instacartSessionId,
				 userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"):
		# TODO Generate these parameters automatically
		"""
		:param csrfToken: This is passed as "x-csrf-token" in some requests
		:param instacartSessionId: Instacart session Id
		"""
		super().__init__()
		self.__csrfToken = csrfToken
		self.__instacartSessionId = instacartSessionId
		self.__userAgent = userAgent

	def __setStore(self, storeId):
		url = "https://shop.aldi.us/v3/bundle"

		payload = f"{{\"warehouse_location_id\":\"{storeId}\"}}"
		headers = {
			'x-csrf-token': self.__csrfToken,
			'cookie': f"_instacart_session_id={self.__instacartSessionId}",
			'user-agent': self.__userAgent,
			'Content-Type': 'text/plain'
		}

		response = requests.request("PUT", url, headers=headers, data=payload)
		print(response.text)
		self.__storeId = storeId

	def getItem(self, identifier, storeIdentifier):
		"""
		:param identifier: The product (not to be confused with the item)
		:param storeIdentifier: Store number
		:return:
		"""
		if self.__storeId is None or self.__storeId is not storeIdentifier:
			self.__setStore(storeIdentifier)
		# First thing is to get the item given the product
		url = f"https://shop.aldi.us/v3/containers/products/{identifier}"

