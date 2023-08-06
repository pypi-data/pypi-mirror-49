apk-cheater
============================================================
| Memory editor with frida-gadget

.. code:: sh

  $ pip install frida-gadget 
  $ frida-gadget {APK_PATH}
  > Gadget APK: {GADGET_APK_PATH}
  ... singing and running your usb device
  $ apk-cheater
  > [Warning] Signing with default keystore.
  > [Warning] Please pass --key_path, --key_alias, --key_pass, --ks_pass parameter, if you want to use your keystore
  > {SIGNED_APK_PATH}
  $ pyapksigner --key_path="sample.jks" --key_alias="sample" --key_pass="sample_key" --ks_pass="sample_ks"
  > {SIGNED_APK_PATH}


