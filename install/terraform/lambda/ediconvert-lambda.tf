/*
EDI Converter Lambda function without an S3 trigger for manual invocation.
*/
resource "aws_lambda_function" "edi_converter_function_manual" {
  environment {
    variables = {
      # Replace with your key
      EDI_LICENSE_KEY = "Ic5OXgAAABoAAAACAAAACwAAAANlbnRpdGxlbWVudEVESQAAABoAAAALAAAACmV4cGlyYXRpb24AAAGdIyY2AAAAAJwAAAABAAAAEAAAAIBsaWNlbnNlU2lnbmF0dXJlNNiFGndeVeM9X4kxO9SFf7U0Gq7K9LLKEKPEhW5TTqZvFEB2QyKb1A7/8BjddgIZUAnNxRSykCMj6u34YlBeibVwkHqyg2p31qHRwYGtVO4O6YTEsveZ15gH5yOS1vZI6ztxI7MWsOXn7bupiezerY4/0MLMHuWqC6V1+kQVVLQAAAAiAAAAAgAAAA8AAAAHc2lnbmF0dXJlRGlnZXN0U0hBLTUxMg=="
      # Include parser's warnings in the output
      OUTPUT_WARNINGS = "True"
      # name of the output bucket
      OUT_BUCKET      = "edi-out"
      # JSON, JSONL, CSV, EXCEL
      OUT_FORMAT      = "JSON"
    }
  }

  ephemeral_storage {
    size = "1024"
  }

  function_name = "EdiConverter"
  # Handler for direct/manual invoke
  handler       = "hdi.aws.ConverterEventHandler::handleRequest"

  # The code is deployed from this public bucket
  s3_bucket     = "ediconverter"
  s3_key        = "ediconvert-lambda-2.14.zip"

  memory_size = "512"
  package_type = "Zip"
  role         = aws_iam_role.lambda_exec_role.arn
  runtime      = "java25"

  # Increase timeout if processing large files
  timeout = "180"
}

