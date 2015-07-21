# Apache Ambari integration for Spring XD

```text
$ ./gradlew clean dist
```

Task `dist` will create rpm files for both `PHD` and `HDP`
under `build/distributions`. Use files `springxd-plugin-phd-1.2-1.noarch.rpm`
or `springxd-plugin-hdp-1.2-1.noarch.rpm` respectively.

More detailed instructions using Ambari with PHD and HDP:

[Preparing a CentOS single-node VM for use with Ambari](src/docs/asciidoc/PreparingVMforAmbari.asciidoc)

[Installing Pivotal HD 3.0 on single-node VM using Ambari](src/docs/asciidoc/InstallingPHDwithAmbari.asciidoc)

[Installing Hortonworks HDP 2.2 on single-node VM using Ambari](src/docs/asciidoc/InstallingHDPwithAmbari.asciidoc)

[Installing Spring XD using Ambari](src/docs/asciidoc/InstallingXDwithAmbari.asciidoc)

