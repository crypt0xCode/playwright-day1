import asyncio
from playwright.async_api import async_playwright, expect
from config import logger, EXTENSION_PATH, MM_PASSWORD
from logo import LOGO


async def recovery_wallet(seed: list) -> None:
    """
    Recovery created MetaMask wallet from seed phrase.
    :param seed: list of seed words.
    :return: none.
    """
    logger.debug('Starting wallet recovery.')
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=[
                f"--disable-extensions-except={EXTENSION_PATH}",
                f"--load-extension={EXTENSION_PATH}",
            ]
        )

        if len(context.service_workers) == 0:
            background_page = await context.wait_for_event('serviceworker')
        else:
            background_page = context.service_workers[0]

        titles = [await p.title() for p in context.pages]
        while 'MetaMask' not in titles:
            titles = [await p.title() for p in context.pages]

        logger.debug('Opening MetaMask page.')
        mm_page = context.pages[1]
        await mm_page.wait_for_load_state()

        # -------------------- согласиться с условиями использования и восстановить существующий кошелек --------------------
        logger.debug('Accept MetaMask agreements.')
        checkbox = mm_page.locator('//*[@id="onboarding__terms-checkbox"]')
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        import_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-import-wallet')
        await expect(import_wallet_btn).to_be_enabled()
        await import_wallet_btn.click()

        # -------------------- отказаться от сбора информации --------------------
        logger.debug('Decline information collecting.')
        i_dont_agree_btn = mm_page.get_by_test_id(test_id='metametrics-no-thanks')
        await expect(i_dont_agree_btn).to_be_attached()
        await i_dont_agree_btn.click()

        # -------------------- ввести seed из 12 слов --------------------
        logger.debug('Entering recovery phrase.')
        for i in range(12):
            word = mm_page.get_by_test_id(test_id=f'import-srp__srp-word-{i}')
            await word.fill(seed[i])

        accept_bttn = mm_page.get_by_test_id(test_id='import-srp-confirm')
        await expect(accept_bttn).to_be_enabled()
        await accept_bttn.click()

        # -------------------- ввести пароль --------------------
        logger.debug('Entering MetaMask wallet password.')
        passwd_1 = mm_page.get_by_test_id(test_id='create-password-new')
        passwd_2 = mm_page.get_by_test_id(test_id='create-password-confirm')
        checkbox = mm_page.get_by_test_id(test_id='create-password-terms')
        import_wallet_btn = mm_page.get_by_test_id(test_id='create-password-import')
        await expect(passwd_1).to_be_attached()
        await passwd_1.fill(MM_PASSWORD)
        await passwd_2.fill(MM_PASSWORD)
        await checkbox.click()

        await expect(import_wallet_btn).to_be_enabled()
        await import_wallet_btn.click()

        # -------------------- нажать "выполнено" --------------------
        import_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-complete-done')
        await expect(import_wallet_btn).to_be_attached()
        await import_wallet_btn.click()

        # -------------------- нажать "далее" --------------------
        import_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-next')
        await expect(import_wallet_btn).to_be_attached()
        await import_wallet_btn.click()

        # -------------------- нажать "выполнено" --------------------
        import_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-done')
        await expect(import_wallet_btn).to_be_attached()
        await import_wallet_btn.click()
        logger.debug('Opening MetaMask main page.')
        await asyncio.sleep(10)

        # -------------------- закрыть страничку --------------------
        logger.debug('Close browser.')
        await mm_page.close()
        await context.close()


async def create_wallet() -> list:
    """
    Create new wallet in MetaMask by Playwright.
    :return: list of seed words.
    """
    seed: list = []
    logger.debug('Starting Playwright.')
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=[
                f"--disable-extensions-except={EXTENSION_PATH}",
                f"--load-extension={EXTENSION_PATH}",
            ],
            slow_mo=600
        )

        if len(context.service_workers) == 0:
            background_page = await context.wait_for_event('serviceworker')
        else:
            background_page = context.service_workers[0]

        titles = [await p.title() for p in context.pages]
        while 'MetaMask' not in titles:
            titles = [await p.title() for p in context.pages]

        logger.debug('Opening MetaMask page.')
        mm_page = context.pages[1]
        await mm_page.wait_for_load_state()

        # -------------------- согласиться с условиями использования и создать новый кошелек --------------------
        logger.debug('Accept MetaMask agreements.')
        checkbox = mm_page.locator('//*[@id="onboarding__terms-checkbox"]')
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-create-wallet')
        await expect(create_wallet_btn).to_be_enabled()
        await create_wallet_btn.click()

        # -------------------- отказаться от сбора информации --------------------
        logger.debug('Decline information collecting.')
        i_dont_agree_btn = mm_page.get_by_test_id(test_id='metametrics-no-thanks')
        await expect(i_dont_agree_btn).to_be_attached()
        await i_dont_agree_btn.click()

        # -------------------- ввести пароль --------------------
        logger.debug('Entering MetaMask wallet password.')
        passwd_1 = mm_page.get_by_test_id(test_id='create-password-new')
        passwd_2 = mm_page.get_by_test_id(test_id='create-password-confirm')
        checkbox = mm_page.get_by_test_id(test_id='create-password-terms')
        create_wallet_btn = mm_page.get_by_test_id(test_id='create-password-wallet')
        await expect(passwd_1).to_be_attached()
        await passwd_1.fill(MM_PASSWORD)
        await passwd_2.fill(MM_PASSWORD)
        await checkbox.click()

        await expect(create_wallet_btn).to_be_enabled()
        await create_wallet_btn.click()

        # -------------------- защитить кошелек --------------------
        logger.debug('Enable wallet security.')
        protect_wallet_btn = mm_page.get_by_test_id(test_id='secure-wallet-recommended')
        await expect(protect_wallet_btn).to_be_attached()
        await protect_wallet_btn.click()

        # -------------------- показать секретную фразу --------------------
        logger.debug('Check secret phrase (seed).')
        show_seed_btn = mm_page.get_by_test_id(test_id='recovery-phrase-reveal')
        await expect(show_seed_btn).to_be_attached()
        await show_seed_btn.click()

        for i in range(12):
            seed.append(
                await mm_page.get_by_test_id(test_id=f'recovery-phrase-chip-{i}').inner_text()
            )
        print(f'Seed: {seed}')

        continue_btn = mm_page.get_by_test_id(test_id='recovery-phrase-next')
        await continue_btn.click()

        # -------------------- подтвердить секретную фразу --------------------
        logger.debug('Entering recovery phrase.')
        seed_field = mm_page.get_by_test_id(test_id='recovery-phrase-input-2')
        await expect(seed_field).to_be_attached()

        await mm_page.get_by_test_id(test_id='recovery-phrase-input-2').fill(seed[2])
        await mm_page.get_by_test_id(test_id='recovery-phrase-input-3').fill(seed[3])
        await mm_page.get_by_test_id(test_id='recovery-phrase-input-7').fill(seed[7])

        confirm_btn = mm_page.get_by_test_id(test_id='recovery-phrase-confirm')
        await expect(confirm_btn).to_be_enabled()
        await confirm_btn.click()

        # -------------------- нажать "понятно" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-complete-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- нажать "далее" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-next')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- нажать "выполнено" --------------------
        create_wallet_btn = mm_page.get_by_test_id(test_id='pin-extension-done')
        await expect(create_wallet_btn).to_be_attached()
        await create_wallet_btn.click()

        # -------------------- закрыть страничку --------------------
        logger.debug('Close browser.')
        await mm_page.close()
        await context.close()

    return seed


async def main():
    seed: list = await create_wallet()
    await recovery_wallet(seed)


if __name__ == '__main__':
    print(LOGO)
    logger.info('Starting program.')
    asyncio.run(main())