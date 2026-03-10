/*
Shared Terraform resources used by both lambda variants.
*/

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.21.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

locals {
  # Shared environment variables for both Lambda functions
  edi_converter_lambda_environment = {
    EDI_LICENSE_KEY = "Ic5OXgAAABoAAAACAAAACwAAAANlbnRpdGxlbWVudEVESQAAABoAAAALAAAACmV4cGlyYXRpb24AAAGdIyY2AAAAAJwAAAABAAAAEAAAAIBsaWNlbnNlU2lnbmF0dXJlNNiFGndeVeM9X4kxO9SFf7U0Gq7K9LLKEKPEhW5TTqZvFEB2QyKb1A7/8BjddgIZUAnNxRSykCMj6u34YlBeibVwkHqyg2p31qHRwYGtVO4O6YTEsveZ15gH5yOS1vZI6ztxI7MWsOXn7bupiezerY4/0MLMHuWqC6V1+kQVVLQAAAAiAAAAAgAAAA8AAAAHc2lnbmF0dXJlRGlnZXN0U0hBLTUxMg=="
    OUTPUT_WARNINGS = "True"
    OUT_BUCKET      = "edi-out"
    OUT_FORMAT      = "JSON"
  }
}

# Shared lambda execution role
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

# Shared IAM policy for S3 access
resource "aws_iam_policy" "lambda_s3_access_policy" {
  name        = "lambda_s3_full_access"
  description = "Lambda functions can access all S3 buckets"

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

output "edi_converter_trigger_function_name" {
  value = aws_lambda_function.edi_converter_function_trigger.function_name
}

output "edi_converter_manual_function_name" {
  value = aws_lambda_function.edi_converter_function_manual.function_name
}
