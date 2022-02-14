#!/usr/bin/env bash

set -x


AZURE_GROUP_NAME=""
AZURE_CONTAINER_NAME="pawoo-rt"

az container create --resource-group "$AZURE_GROUP_NAME" --file setup.yaml

sleep 5.0
az container show --resource-group "$AZURE_GROUP_NAME" \
    --name "$AZURE_CONTAINER_NAME" \
    --query "{FQDN:ipAddress.fqdn,PublicIP:ipAddress.ip,ProvisioningState:provisioningState}" \
    --output table
