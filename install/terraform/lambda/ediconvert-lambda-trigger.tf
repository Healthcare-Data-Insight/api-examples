/*
EDI Converter Lambda function with a trigger on an input S3 bucket.
*/
resource "aws_lambda_function" "edi_converter_function_trigger" {
  environment {
    variables = local.edi_converter_lambda_environment
  }

  ephemeral_storage {
    size = "1024"
  }

  function_name = "EdiConverterFromTrigger"
  # Handler for the trigger
  handler       = "hdi.aws.ConverterTriggerEventHandler::handleRequest"

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
}

resource "aws_s3_bucket" "edi_in_bucket" {
  bucket = "edi-in"
}

resource "aws_s3_bucket_notification" "s3_lambda_trigger" {
  bucket = aws_s3_bucket.edi_in_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.edi_converter_function_trigger.arn
    events             = ["s3:ObjectCreated:*"]
    filter_prefix      = ""
    filter_suffix      = ""
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke]
}

resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.edi_converter_function_trigger.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.edi_in_bucket.arn
}
