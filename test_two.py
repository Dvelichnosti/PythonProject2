import pytest
from playwright.async_api import async_playwright, Page, Browser
from constants import EMAIL, PASSWORD, BROWSERS  # Импорт констант из constants.py


# Page Object для страницы авторизации
class AuthPage:
    def __init__(self, page: Page):
        self.page = page

    async def navigate(self):
        await self.page.goto('https://my.cryptocopy.org/en/auth/')

    async def login(self):
        await self.page.fill("input[type='email']", EMAIL)
        await self.page.fill("input[type='password']", PASSWORD)
        await self.page.get_by_role(role='button', name='Continue').click()

    async def is_logged_in(self):
        try:
            await self.page.locator("h1").wait_for(timeout=5000)
            return True
        except Exception:
            return False


# Page Object для главной страницы
class HomePage:
    def __init__(self, page: Page):
        self.page = page

    async def go_to_home(self):
        await self.page.locator("xpath=//main/div//*[text()='Home']").click()
        await self.page.locator("xpath=//main/div//*[text()='Home']").wait_for(timeout=5000)


# Page Object для страницы подписки
class SubscriptionPage:
    def __init__(self, page: Page):
        self.page = page

    async def go_to_subscription(self):
        await self.page.get_by_role('link', name='About tariffs and subscriptions').click()
        await self.page.wait_for_load_state()


# Асинхронный тестовый класс
@pytest.mark.asyncio
class TestCryptoCopy:

    @pytest.mark.parametrize("browser_type", BROWSERS)  # Параметризованный запуск для всех браузеров
    async def test_cryptocopy(self, browser_type):
        async with async_playwright() as p:
            browser: Browser = await p[browser_type].launch(headless=False)
            page = await browser.new_page()
            auth_page = AuthPage(page)
            home_page = HomePage(page)
            subscription_page = SubscriptionPage(page)

            await auth_page.navigate()
            await auth_page.login()

            if not await auth_page.is_logged_in():
                print(f"Не удалось авторизоваться! Скриншот: screenshot_{browser_type}.png")
                await page.screenshot(path=f"screenshot_{browser_type}.png")
                await browser.close()
                return

            await home_page.go_to_home()
            await subscription_page.go_to_subscription()

            try:
                await page.get_by_role(role='button', name='Subscription is activated').wait_for(timeout=5000) #подписка уже активированна, по этому мы проверяем, что мы подписаны
                print('все видно')
            except Exception as e:
                print(f"Проверка кнопки подписки не удалась: {e}")
                await page.screenshot(path=f"screenshot_{browser_type}_error.png")

            await browser.close()


