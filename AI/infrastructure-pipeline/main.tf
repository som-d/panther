terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}
provider "azurerm" {
  features {}
}
resource "azurerm_resource_group" "main" {
  name     = "rg-beastmode-dev-001"
  location = "eastus"
  tags = {
    environment = "dev"
    managed_by  = "terraform"
    project     = "beast-mode"
  }
}