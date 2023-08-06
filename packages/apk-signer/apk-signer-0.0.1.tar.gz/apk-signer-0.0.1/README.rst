pyapksigner
============================================================
| pyapksigner can sign the apk file.

.. code:: sh

  $ pip install pyapksigner
  $ pyapksigner {APK_PATH} --default
  > {SIGNED_APK_PATH}
  $ pyapksigner {APK_PATH} 
  > [Warning] Signing with default keystore.
  > [Warning] Please pass --key_path, --key_alias, --key_pass, --ks_pass parameter, if you want to use your keystore
  > {SIGNED_APK_PATH}
  $ pyapksigner --key_path="sample.jks" --key_alias="sample" --key_pass="sample_key" --ks_pass="sample_ks"
  > {SIGNED_APK_PATH}


