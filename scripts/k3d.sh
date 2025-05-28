#!/bin/bash

set -euo pipefail
set -x

CLUSTER_NAME="dev"
VAR_DIR="$HOME/Data/var"

# Assume dev cluster exists due to backend.  See weightr-backend/scripts/k3d.sh for details.
CLUSTERS=$(k3d cluster list)
echo "CLUSTERS=$CLUSTERS"

if ! echo $CLUSTERS | grep -q "$CLUSTER_NAME"; then
  echo "Cluster '$CLUSTER_NAME' doest not exist.  Create it first!"
  exit 1
fi

if [ -z "${GPG_PASSPHRASE}" ]; then
  echo "*** ERROR: GPG_PASSPHRASE is not set!!! Set this before running the script!"
  exit 1
fi

echo "Encrypting configuration..."
rm -f $VAR_DIR/conf/weightr-frontend/.env.dev.docker.gpg
cat "$VAR_DIR/conf/weightr-frontend/.env.dev.docker"| \
     gpg --symmetric --cipher-alg AES256 \
         --batch --passphrase "$GPG_PASSPHRASE" \
         -o "$VAR_DIR/conf/weightr-frontend/.env.dev.docker.gpg"

# Note: you can decrypt using
# gpg --batch --yes --passphrase $GPG_PASSPHRASE \
#     -o var/conf/weightr-frontend/.env.dev.docker.decrypted \
#     -d var/conf/weightr-frontend/.env.dev.docker.gpg


echo "Building docker image..."
docker build -t weightr-frontend:latest .

echo "Importing docker image..."
k3d image import weightr-frontend:latest -c $CLUSTER_NAME

echo "Deploying resources to k3d..."
helm upgrade --install weightr-frontend ./helm

echo "Restarting deployment..."
kubectl rollout restart deployment weightr-frontend

echo "Development cluster '$CLUSTER_NAME' is ready."
