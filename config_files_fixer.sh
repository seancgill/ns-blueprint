#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error: $1" >&2
    exit 1
}

# Create private key file
echo "-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgcm474csbnbmQTpHJ
W7zXGmkBf3niiUZcaUfqDi8aJp+gCgYIKoZIzj0DAQehRANCAAT2IPM5HO6LSPxF
sVMNOBtKViTnqEwmjHw13PkWmg+Ynoh5hMnczqDRsqb2quH09lOv+o2rapIZ8NGg
/xhKIYNm
-----END PRIVATE KEY-----" > /etc/netsapiens/AuthKey_AKH943K68Y.p8 || handle_error "Failed to create private key file."

# Modify API configuration file
{
    grep -q "Configure::write('VoiceservicesUrl'" /etc/netsapiens/api_config.php || \
        echo "Configure::write('VoiceservicesUrl', 'https://voice-services.netsapiens.com:8000/v1');" >> /etc/netsapiens/api_config.php

    grep -q "Configure::write('VoiceservicesLicense'" /etc/netsapiens/api_config.php || \
        echo "Configure::write('VoiceservicesLicense', '855b6169-78b7-4a3c-8cc4-a3bea37c996d');" >> /etc/netsapiens/api_config.php

    grep -q "Configure::write('APNS.SNAPmobile.key'" /etc/netsapiens/api_config.php || \
        echo "Configure::write('APNS.SNAPmobile.key' , '/etc/netsapiens/AuthKey_AKH943K68Y.p8');" >> /etc/netsapiens/api_config.php

    grep -q "Configure::write('APNS.SNAPmobile.keyId'" /etc/netsapiens/api_config.php || \
        echo "Configure::write('APNS.SNAPmobile.keyId' , 'AKH943K68Y');" >> /etc/netsapiens/api_config.php

    grep -q "Configure::write('APNS.SNAPmobile.bundleId'" /etc/netsapiens/api_config.php || \
        echo "Configure::write('APNS.SNAPmobile.bundleId' , 'com.netsapiens.SNAPmobile');" >> /etc/netsapiens/api_config.php

    grep -q "Configure::write('APNS.SNAPmobile.teamId'" /etc/netsapiens/api_config.php || \
        echo "Configure::write('APNS.SNAPmobile.teamId' , '7LN53XL4QL');" >> /etc/netsapiens/api_config.php

    grep -q "Configure::write('Sfu.license_token'" /etc/netsapiens/api_config.php || \
        echo "Configure::write('Sfu.license_token' , '9f81994b8cf538fe820164b7df44d949');" >> /etc/netsapiens/api_config.php
} || handle_error "Script failed to execute properly."


echo "Starting the images application..."
# Execute Images script
python3 images.py

