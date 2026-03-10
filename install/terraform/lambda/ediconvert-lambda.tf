/*
EDI Converter Lambda function without an S3 trigger for manual invocation.
*/
resource "aws_lambda_function" "edi_converter_function_manual" {
  environment {
    variables = local.edi_converter_lambda_environment
  }

  ephemeral_storage {
    size = "512"
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
  publish      = true

  # Increase timeout if processing large files
  timeout = "300"

  # Note: this only works if the ephemeral storage is 512
  snap_start {
    apply_on = "PublishedVersions"
  }
}
