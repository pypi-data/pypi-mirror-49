pyapksigner
============================================================
| pyapksigner can sign the apk file and run signed apk to your device.
|

.. code:: sh

  $ pip install pyapksigner

  $ pyapksigner --sign [apk_path]
  > [signed_apk_path]
  $ pyapksigner --sign --key_path="sample.jks" --key_alias="sample" --key_pass="sample_key" --ks_pass="sample_ks"
  > [signed_apk_path]

