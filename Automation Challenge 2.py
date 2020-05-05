import tableauserverclient as TSC
import csv
from pathlib import Path
from tableauhyperapi import HyperProcess, Telemetry, \
    Connection, CreateMode, \
    NOT_NULLABLE, NULLABLE, SqlType, TableDefinition, \
    Inserter, \
    escape_name, escape_string_literal, \
    HyperException

tableau_auth = TSC.TableauAuth('zak.g.data@gmail.com', 'Tr1force@', 'betatestingfortableauserver')
server = TSC.Server('https://10ax.online.tableau.com')
file_path = r'C:\Users\Zak\Desktop\Workbook_Info.hyper'
project_id = '61be71a8-e85d-462a-8ac7-c794344f0394'

# TABLEAU SERVER CLIENT LIBRARY TO GET AND STORE WORKBOOK / OWNER DETAILS

with server.auth.sign_in(tableau_auth):
    all_workbooks, pagination_item = server.workbooks.get()

    x = []
    y = []
    z = []

    for workbook in all_workbooks:
        x.append(workbook.name) 
        y.append(workbook.owner_id) 

    for users in y:
        z.append(server.users.get_by_id(users))

with open('workbook_info.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(zip(x, y, z))

# HYPER API TO CREATE HYPER FILE

Workbook_Info_table = TableDefinition(
    table_name="Workbook_Info",
    columns=[
        TableDefinition.Column("Workbook Name", SqlType.text(), NOT_NULLABLE),
        TableDefinition.Column("Workbook LUID", SqlType.text(), NOT_NULLABLE),
        TableDefinition.Column("Owner Info", SqlType.text(), NOT_NULLABLE)
    ]
)

def run_create_hyper_file_from_csv():

    path_to_database = Path("Workbook_Info.hyper")

    process_parameters = {
        "log_file_max_count": "2",
        "log_file_size_limit": "100M"
    }

    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU, parameters=process_parameters) as hyper:

        connection_parameters = {"lc_time": "en_US"}

        with Connection(endpoint=hyper.endpoint,
                        database=path_to_database,
                        create_mode=CreateMode.CREATE_AND_REPLACE,
                        parameters=connection_parameters) as connection:

            connection.catalog.create_table(table_definition=Workbook_Info_table)

            path_to_csv = str(Path(__file__).parent / "workbook_info.csv")

            count_in_Workbook_Info_table = connection.execute_command(
                command=f"COPY {Workbook_Info_table.table_name} from {escape_string_literal(path_to_csv)} with "
                f"(format csv, NULL 'NULL', delimiter ',', header)")

if __name__ == '__main__':
    try:
        run_create_hyper_file_from_csv()
    except HyperException as ex:
        print(ex)
        exit(1)

# TABLEAU SERVER CLIENT LIBRARY TO PUBLISH DATA SOURCE

with server.auth.sign_in(tableau_auth):
    new_datasource = TSC.DatasourceItem(project_id)

    new_datasource = server.datasources.publish(
                        new_datasource, file_path, 'Overwrite')