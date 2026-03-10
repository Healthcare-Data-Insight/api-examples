/*
EDI Converter Lambda function without an S3 trigger for manual invocation.
*/
variable "run_test_events" {
  description = "Set to true to run Lambda test invocations from the events directory"
  type        = bool
  default     = false
}

locals {
  # Load test payload files for manual Lambda invocations
  manual_lambda_event_paths = sort(fileset("${path.module}/events", "*.json"))
  manual_lambda_test_events = [
    for event_path in local.manual_lambda_event_paths : jsondecode(file("${path.module}/events/${event_path}"))
  ]
}

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
# Run test events, only if run_test_events is True
resource "aws_lambda_invocation" "edi_converter_manual_test_events" {
  for_each = var.run_test_events ? {
    for idx, event_payload in local.manual_lambda_test_events : idx => event_payload
  } : {}

  function_name = aws_lambda_function.edi_converter_function_manual.function_name
  input         = jsonencode(each.value)

  depends_on = [aws_lambda_function.edi_converter_function_manual]
}
