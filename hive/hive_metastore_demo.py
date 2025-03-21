import thriftpy2
from thriftpy2.rpc import make_client
hive_metastore_thrift = thriftpy2.load("hive_metastore.thrift", module_name="hive_metastore_thrift")


def connect_to_metastore(host='localhost', port=10002):
    client = make_client(
        hive_metastore_thrift.ThriftHiveMetastore,
        host,
        port,
        proto_factory=thriftpy2.thrift.TBinaryProtocolFactory(),
        trans_factory=thriftpy2.transport.TFramedTransportFactory(),
    )
    return client

# Fetch all databases
def get_all_databases(client):
    return client.get_all_databases()

# Fetch all tables in a database
def get_all_tables(client, db_name):
    return client.get_all_tables(db_name)

# Fetch table metadata
def get_table_metadata(client, db_name, table_name):
    return client.get_table(db_name, table_name)

# Main function
def main():
    try:
        client = connect_to_metastore()
        databases = get_all_databases(client)
        print("Databases:", databases)

        if databases:
            db_name = databases[0]
            tables = get_all_tables(client, db_name)
            print(f"Tables in database '{db_name}':", tables)

            if tables:
                table_name = tables[0]
                table_metadata = get_table_metadata(client, db_name, table_name)
                print(f"Metadata for table '{table_name}':", table_metadata)

        client.close()
    except thriftpy2.thrift.TException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
