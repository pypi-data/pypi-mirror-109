import asyncio
import aiohttp
from hashlib import sha1
import os

from urllib.parse import quote_plus

from haveibeenpwned_asyncio.constants import haveibeenpwned, hashing


class haveIbeenPwnedClient(object):
    def __init__(self, semaphore_max: int = 10, api_key:str ="", truncate_response: bool = True):
        self.semaphore_max = semaphore_max
        self.semaphore = asyncio.Semaphore(10)
        self.api_version = haveibeenpwned.API_VERSION.value
        self.base_url = f"{haveibeenpwned.BASE_URL.value}{self.api_version}"
        self.api_key = None if not api_key else api_key
        self.truncate_response: bool = truncate_response
        self.loop = asyncio.get_event_loop()





    def generate_url(self, endpoint, object):
        return f"{self.base_url}/{endpoint}/{quote_plus(object)}"

    async def prep_headers(self, header_obj: dict):
        if not self.api_key:
            header_obj.pop("hibp-api-key", None)
        else:
            header_obj["hibp-api-key"] = self.api_key
            print(f"headers['hibp-api-key']: {header_obj['hibp-api-key'] }")
        return header_obj

    async def aiohttp_client_get(self, url:str, obj:str= ""):
        await self.semaphore.acquire()
        url = url + f"?truncateResponse={self.truncate_response}"
        print(url)
        headers = await self.prep_headers(haveibeenpwned.HTTP_HEADER.value)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    # return url, await resp.status
                    return obj, resp.status, await resp.text()
        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.semaphore.release()


    async def queue_all_requeusts(self, urls: list = []):
        asyncio_tasks = []
        for url in urls:
            asyncio_tasks.append(self.aiohttp_client_get(url=url[0], obj=url[1]))
        return asyncio_tasks


    async def gather_all_requests(self, asyncio_tasks: list = []):
        return await asyncio.gather(*asyncio_tasks)

class haveIbeenPwnedAccount(haveIbeenPwnedClient):
    def __init__(self, semaphore_max:int = 10, accounts: list = [], api_key:str =""):
        self.semaphore_max = semaphore_max
        super().__init__(accounts, api_key)
        self.endpoint = haveibeenpwned.ACCOUNT_ENDPOINT.value
        self.accounts = accounts


    async def query_accounts(self):
        urls = []
        for account in self.accounts:
            urls.append((self.generate_url(endpoint=self.endpoint, object=account), account))
        responses = await self.gather_all_requests(
            await self.queue_all_requeusts(urls=urls)
        )
        return responses

    def query_accounts_sync(self):
        coroutine = self.query_accounts()
        return self.loop.run_until_complete(coroutine)

class haveIbeenPwnedPastes(haveIbeenPwnedClient):
    def __init__(self, semaphore_max:int = 10, pastes: list = [], api_key:str =""):
        self.semaphore_max = semaphore_max
        super().__init__(pastes, api_key)
        self.endpoint = haveibeenpwned.PASTES_ENDPOINT.value
        self.pastes = pastes

    async def query_pastes(self):
        urls = []
        for paste in self.pastes:
            urls.append((self.generate_url(endpoint=self.endpoint, object=paste), paste))
        responses = await self.gather_all_requests(
            await self.queue_all_requeusts(urls=urls)
        )
        return responses

    def query_pastes_sync(self):
        coroutine = self.query_pastes()
        return self.loop.run_until_complete(coroutine)

class haveIbeenPwnedPasswords(haveIbeenPwnedClient):
    def __init__(self, semaphore_max:int = 10, passwords: list = [], api_key:str = ""):
        super().__init__(passwords, api_key)
        self.semaphore_max = semaphore_max
        self.endpoint = haveibeenpwned.PASSWORD_ENDPOINT.value
        self.passwords = passwords
        self.api_key = ''
        self.base_url=haveibeenpwned.PASSWORD_BASE_URL.value


    async def query_passwords(self):
        urls = []
        utf_passwords = [p.encode(hashing.ENCODING.value) for p in self.passwords]
        print(f"utf_passwords: {utf_passwords}")
        for password in utf_passwords:
            print(f"password {password} ")
            hash = sha1(password).hexdigest()
            urls.append(
                (self.generate_url(endpoint=self.endpoint, object=hash[:5]), password.decode("utf-8"))
            )
        responses = await self.gather_all_requests(
            await self.queue_all_requeusts(urls=urls)
        )
        return responses

    def query_passwords_sync(self):
        coroutine = self.query_passwords()
        return self.loop.run_until_complete(coroutine)