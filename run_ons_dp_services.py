import argparse
import csv
import iterm2
import os


def load_service_list_from_csv(csvfilename):
    with open(csvfilename, 'r') as f:
        return [row for row in csv.DictReader(f)]


def get_configured_service_runner(service_list_name, service_list):
    async def service_runner(connection):
        app = await iterm2.async_get_app(connection)
        window = await iterm2.Window.async_create(connection)
        tabs = []
        for service in service_list:
            if len(tabs) == 0:
                tab = window.current_tab
            else:
                tab = await window.async_create_tab()
            await tab.async_set_title(service["name"])
            session = tab.current_session
            await session.async_send_text(f'cd {service["path"]}\n')
            await session.async_send_text(f'{service["action"]}\n')
            tabs.append(tab)
        input(f'ONS services detailed in {service_list_name} running in new terminal window. Press any key to quit.')
        for tab in tabs:
            session = tab.current_session
            tab_name = await tab.async_get_variable('titleOverride')
            job_name = await session.async_get_variable('jobName')
            job_pid = await session.async_get_variable('jobPid')
            print(f"Sending SIGTERM 15 to {job_name} (pid: {job_pid}) in tab {tab_name}")
            os.kill(job_pid, 15)
    return service_runner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "services_csv",
        help="The name of the csv file detailing the ons services to start (assumed in same folder as this script)."
    )
    args = parser.parse_args()
    service_list = load_service_list_from_csv(args.services_csv)
    tabs = []
    service_runner = get_configured_service_runner(args.services_csv, service_list)
    iterm2.run_until_complete(service_runner)


if __name__=="__main__":
    main()
