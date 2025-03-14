provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "data_lake" {
  bucket = "enterprise-data-lake"
}

resource "aws_redshift_cluster" "analytics" {
  cluster_identifier = "analytics-cluster"
  node_type = "dc2.large"
  number_of_nodes = 2
  database_name = "customer_data"
}

resource "kubernetes_deployment" "ml_api" {
  metadata { name = "ml-api" }
  spec {
    replicas = 3
    selector { match_labels = { app = "ml-api" } }
    template {
      metadata { labels = { app = "ml-api" } }
      spec {
        container {
          name  = "ml-api"
          image = "ml-api:latest"
        }
      }
    }
  }
}
