# MDE-batch-message

Sesam Microservice to batch MDE messages in template defined format

Batch size is determined by defined batch size in Sesam pipe feeding the microservice.


### Config example
*Notice that the `template` property is an escaped json string.*

`batch_payload_key` is the key for the value that should be replaced with the list of entities posted to the service.

```json
{
  "_id": "mde-batch",
  "docker": {
    "environment": {
      "batch_payload_key": "PayloadEstimated",
      "headers": {
        "Ocp-Apim-Subscription-Key": "$SECRET(mde-rest-apikey)"
      },
      "template": "{\r\n  \"Header\": {\r\n    \"CompanyName\": \"My company\",\r\n    \"CompanyRole\": \"ABC\",\r\n    \"CorrelationID\": \"\",\r\n    \"CreatedDateTime\": \"{{ now }}\",\r\n    \"DocumentType\": \"E58\",\r\n    \"EventCategory\": \"meteringvalues\",\r\n    \"MessageID\": \"{{ uuid }}\",\r\n    \"Noun\": \"EstimatedConsumptionSet\",\r\n    \"Receiver\": \"ELHUB\",\r\n    \"ReferenceID\": \"\",\r\n    \"ReplyAddress\": \"\",\r\n    \"Revision\": \"2.0\",\r\n    \"Sender\": \"1234567891234\",\r\n    \"Source\": \"MDE\",\r\n    \"Verb\": \"Request\"\r\n  },\r\n  \"Payload\": {\r\n    \"Header\": {\r\n      \"CreatedDateTime\": \"{{ now }}\",\r\n      \"DocumentType\": {\r\n        \"Code\": \"E58\",\r\n        \"Source\": \"260\"\r\n      },\r\n      \"JuridicalRecipientEnergyParty\": {\r\n        \"SourceIdentifier\": {\r\n          \"Code\": \"987654321123\",\r\n          \"Source\": \"9\"\r\n        }\r\n      },\r\n      \"JuridicalSenderEnergyParty\": {\r\n        \"SourceIdentifier\": {\r\n          \"Code\": \"1234567891234\",\r\n          \"Source\": \"9\"\r\n        }\r\n      },\r\n      \"MRID\": \"{{ uuid }}\",\r\n      \"PhysicalSenderEnergyParty\": {\r\n        \"SourceIdentifier\": {\r\n          \"Code\": \"1245686531\",\r\n          \"Source\": \"9\"\r\n        }\r\n      }\r\n    },\r\n    \"PayloadEstimated\": [],\r\n    \"Process\": {\r\n      \"EnergyBusinessProcess\": {\r\n        \"Code\": \"BRS-NO-317\",\r\n        \"Source\": \"89\"\r\n      },\r\n      \"EnergyBusinessProcessRole\": {\r\n        \"Code\": \"DDM\",\r\n        \"Source\": \"6\"\r\n      },\r\n      \"EnergyIndustryClassification\": {\r\n        \"Code\": \"23\"\r\n      }\r\n    }\r\n  }\r\n}",
      "endpoint_url": "MeterValue/EstimatedConsumption/V2/UpdateEstimatedAnnualConsumption"
    },
    "image": "andebor/mde-batch-message:latest",
    "memory": 512,
    "port": 5001
  },
  "type": "system:microservice",
  "verify_ssl": true
}
```


The template value is the following json after escaping all quotes with [this tool](https://www.freeformatter.com/json-escape.html) :
```json
{
  "Header": {
    "CompanyName": "My company",
    "CompanyRole": "ABC",
    "CorrelationID": "",
    "CreatedDateTime": "{{ now }}",
    "DocumentType": "E58",
    "EventCategory": "meteringvalues",
    "MessageID": "{{ uuid }}",
    "Noun": "EstimatedConsumptionSet",
    "Receiver": "ELHUB",
    "ReferenceID": "",
    "ReplyAddress": "",
    "Revision": "2.0",
    "Sender": "1234567891234",
    "Source": "MDE",
    "Verb": "Request"
  },
  "Payload": {
    "Header": {
      "CreatedDateTime": "{{ now }}",
      "DocumentType": {
        "Code": "E58",
        "Source": "260"
      },
      "JuridicalRecipientEnergyParty": {
        "SourceIdentifier": {
          "Code": "987654321123",
          "Source": "9"
        }
      },
      "JuridicalSenderEnergyParty": {
        "SourceIdentifier": {
          "Code": "1234567891234",
          "Source": "9"
        }
      },
      "MRID": "{{ uuid }}",
      "PhysicalSenderEnergyParty": {
        "SourceIdentifier": {
          "Code": "1245686531",
          "Source": "9"
        }
      }
    },
    "PayloadEstimated": [],
    "Process": {
      "EnergyBusinessProcess": {
        "Code": "BRS-NO-317",
        "Source": "89"
      },
      "EnergyBusinessProcessRole": {
        "Code": "DDM",
        "Source": "6"
      },
      "EnergyIndustryClassification": {
        "Code": "23"
      }
    }
  }
}
```