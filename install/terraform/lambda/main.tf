/*
EDI Converter Lambda function with a trigger on an input S3 bucket
 */

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}


resource "aws_lambda_function" "edi_converter_function" {

  environment {
    variables = {
      # Replace with your key, the key below has expired
      EDI_LICENSE_KEY = "Ic5OXgAAABoAAAACAAAACwAAAANlbnRpdGxlbWVudEVESQAAABoAAAALAAAACmV4cGlyYXRpb24AAAGadm9YgAAAAJwAAAABAAAAEAAAAIBsaWNlbnNlU2lnbmF0dXJlRsqEQItRpwCXDXeor0dJOtbLApxQmJ7A2hzUY2jdzTncOO0K5Gy/U0DIdqXhYwRcVzo4KipXAF70sObluAjTQSvBc17DMRqh2NjER0JJV5+/KjROS/JHzyhRIGvlUB0WH11scrEDLhuGndI5dEk/v6sVgA8G7hqfINkW9BMt4V0AAAAiAAAAAgAAAA8AAAAHc2lnbmF0dXJlRGlnZXN0U0hBLTUxMg=="
      # Include parser's warnings in the output
      OUTPUT_WARNINGS = "True"
      # name of the output bucket
      OUT_BUCKET      = "ediout"
      # JSON, JSONL, CSV, EXCEL
      OUT_FORMAT      = "JSON"
    }
  }

  # Increase storage if processing large files
  ephemeral_storage {
    size = "1024"
  }

  function_name = "EdiConverter"
  # Handler for the trigger
  handler       = "hdi.aws.ConverterTriggerEventHandler::handleRequest"
  # Handler for direct events
  #handler       = "hdi.aws.ConverterEventHandler::handleRequest"

  # The code is deployed from this public bucket
  s3_bucket     = "ediconverter"
  s3_key        = "ediconvert-lambda-2.14.zip"

  memory_size                    = "512"
  package_type                   = "Zip"
  role                           = aws_iam_role.lambda_exec_role.arn
  runtime                        = "java21"

  # Increase timeout if processing large files
  timeout = "180"

}

# Your input bucket with EDI files for the trigger
resource "aws_s3_bucket" "edi_in_bucket" {
  bucket = "edi-in"
}

# Trigger on the input bucket
resource "aws_s3_bucket_notification" "s3_lambda_trigger" {
  bucket = aws_s3_bucket.edi_in_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.edi_converter_function.arn
    events = ["s3:ObjectCreated:*"]
    filter_prefix       = ""
    filter_suffix       = ""
  }
  depends_on = [aws_lambda_permission.allow_s3_invoke]
}

# Lambda function role
resource "aws_iam_role" "lambda_exec_role" {
  name = "java_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy allowing full access to all S3 buckets in your account
# Customize it to only include the buckets that you use
# The function reads from input bucket and outputs to another bucket
resource "aws_iam_policy" "lambda_s3_access_policy" {
  name        = "lambda_s3_full_access"
  description = "Lambda function can access all S3 buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::*",
          "arn:aws:s3:::*/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_s3_access_policy.arn
}

resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.edi_converter_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.edi_in_bucket.arn
}