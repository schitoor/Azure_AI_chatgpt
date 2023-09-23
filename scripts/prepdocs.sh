 #!/bin/sh

. ./scripts/loadenv.sh

echo 'Running "prepdocs.py"'

if [ -n "$AZURE_ADLS_GEN2_STORAGE_ACCOUNT" ]; then
  adlsGen2FilesystemPathArg=""
  if [ -n "$AZURE_ADLS_GEN2_FILESYSTEM_PATH" ]; then
    adlsGen2FilesystemPathArg="--datalakefilesystempath $AZURE_ADLS_GEN2_FILESYSTEM_PATH"
  fi
  adlsGen2FilesystemArg=""
  if [ -n "$AZURE_ADLS_GEN2_FILESYSTEM" ]; then
    adlsGen2FilesystemArg="--datalakefilesystem $AZURE_ADLS_GEN2_FILESYSTEM"
  fi
  ./scripts/.venv/bin/python ./scripts/prepdocs.py --datalakestorageaccount "$AZURE_ADLS_GEN2_STORAGE_ACCOUNT" $adlsGen2FilesystemArg $adlsGen2FilesystemPathArg --useacls  --storageaccount "$AZURE_STORAGE_ACCOUNT" --container "$AZURE_STORAGE_CONTAINER" --searchservice "$AZURE_SEARCH_SERVICE" --openaiservice "$AZURE_OPENAI_SERVICE" --openaideployment "$AZURE_OPENAI_EMB_DEPLOYMENT" --openaimodelname "$AZURE_OPENAI_EMB_MODEL_NAME" --index "$AZURE_SEARCH_INDEX" --formrecognizerservice "$AZURE_FORMRECOGNIZER_SERVICE" --openaimodelname "$AZURE_OPENAI_EMB_MODEL_NAME" --tenantid "$AZURE_TENANT_ID" -v
else
  ./scripts/.venv/bin/python ./scripts/prepdocs.py './data/*' --storageaccount "$AZURE_STORAGE_ACCOUNT" --container "$AZURE_STORAGE_CONTAINER" --searchservice "$AZURE_SEARCH_SERVICE" --openaiservice "$AZURE_OPENAI_SERVICE" --openaideployment "$AZURE_OPENAI_EMB_DEPLOYMENT" --openaimodelname "$AZURE_OPENAI_EMB_MODEL_NAME" --index "$AZURE_SEARCH_INDEX" --formrecognizerservice "$AZURE_FORMRECOGNIZER_SERVICE" --openaimodelname "$AZURE_OPENAI_EMB_MODEL_NAME" --tenantid "$AZURE_TENANT_ID" -v
fi
