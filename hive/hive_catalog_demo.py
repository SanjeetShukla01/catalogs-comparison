import thriftpy2
from thriftpy2.rpc import make_client
from thriftpy2.transport import TFramedTransportFactory
from thriftpy2.protocol import TBinaryProtocolFactory

# Load the Hive Metastore Thrift file
hive_metastore_thrift = thriftpy2.load("hive_metastore.thrift", module_name="hive_metastore_thrift")


def connect_to_metastore(host='localhost', port=10002):
    client = make_client(
        hive_metastore_thrift.ThriftHiveMetastore,
        host,
        port,
        proto_factory=TBinaryProtocolFactory(),
        trans_factory=TFramedTransportFactory(),
    )
    return client


def get_all_databases(client):
    return client.get_all_databases()


def get_all_tables(client, db_name):
    return client.get_all_tables(db_name)


def get_table_metadata(client, db_name, table_name):
    return client.get_table(db_name, table_name)


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
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
