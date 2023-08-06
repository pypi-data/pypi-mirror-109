table_settings = {
    "Ticker": {
        "key_schema": [
            {
                "AttributeName": "timestamp",
                "KeyType": "HASH"
            }
        ],
        "attribute_definitions": [
            {
                "AttributeName": "timestamp",
                "AttributeType": "S"
            }
        ],
        "provision_throughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    },
    "Ohlcv": {
        "key_schema": [
            {
                "AttributeName": "timestamp",
                "KeyType": "HASH"
            }
        ],
        "attribute_definitions": [
            {
                "AttributeName": "timestamp",
                "AttributeType": "S"
            }
        ],
        "provision_throughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    }
}
