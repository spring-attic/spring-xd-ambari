# Apache Ambari integration for Spring XD

To compile with different stacks:

```text
$ mvn clean package -P phd
$ mvn clean package -P hdp
```

Depending on which profile was used to build the rpm package, under
`target/rpm/springxd-plugin-hdp/RPMS/noarch/` you'll find either
`springxd-plugin-phd-1.2-1.noarch.rpm` or `springxd-plugin-hdp-1.2-1.noarch.rpm`
which can be used with `PHD` or `HDP` respectively.

More detailed instructions using Ambari with PHD and HDP:

[Preparing a CentOS single-node VM for use with Ambari](src/docs/asciidoc/PreparingVMforAmbari.asciidoc)

[Installing Pivotal HD 3.0 on single-node VM using Ambari](src/docs/asciidoc/InstallingPHDwithAmbari.asciidoc)

[Installing Hortonworks HDP 2.2 on single-node VM using Ambari](src/docs/asciidoc/InstallingHDPwithAmbari.asciidoc)

[Installing Spring XD using Ambari](src/docs/asciidoc/InstallingXDwithAmbari.asciidoc)

