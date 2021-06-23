import argparse
import csv
import iterm2


def load_service_list_from_csv(csvpath):
    with open(csvpath, 'r') as f:
        return [row for row in csv.DictReader(f)]


def get_configured_service_runner(service_list):
    async def service_runner(connection):
        app = await iterm2.async_get_app(connection)
        window = await iterm2.Window.async_create(connection)
        startNewTab = False
        for service in service_list:
            if startNewTab is True:
                tab = await window.async_create_tab()
            else:
                tab = window.current_tab
                startNewTab = True
            await tab.async_set_title(service["name"])
            session = tab.current_session
            await session.async_send_text(f'cd {service["path"]}\n')
            await session.async_send_text(f'{service["action"]}\n')
    return service_runner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("services_csv", help="The path to the csv file detailing the ons services to start.")
    args = parser.parse_args()
    service_list = load_service_list_from_csv(args.services_csv)
    service_runner = get_configured_service_runner(service_list)
    iterm2.run_until_complete(service_runner)


if __name__=="__main__":
    main()
